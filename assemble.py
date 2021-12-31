#!/usr/bin/env python3.9
import re

def sub_backslash(match):
    char = match.group(1)
    if char == "n": return str(ord("\n"))
    if char == "t": return str(ord("\t"))
    if char == "r": return str(ord("\r"))
    if char == "b": return str(ord("\b"))
    if char == "\\": return str(ord("\\"))
    raise ValueError(f"No backslash escape sequence known for {char}")

def convert_number(x: int):
    if x < 0:
        begin = "\t"
        x = -x
    else:
        begin = " "
    return f"{begin}{x:b}\n".replace("0", " ").replace("1", "\t")

_id = 0
def next_label():
    global _id
    res = convert_number(_id)
    _id += 1
    return res

operations = {
    # IO
    "rchar": ("\t\n\t ",),
    "rnum": ("\t\n\t\t",),
    "wchar": ("\t\n  ",),
    "wnum": ("\t\n \t",),
    #  tack
    "push": ("  ", int),
    "dup": (" \n ",),
    "swap": (" \n\t",),
    "pop": (" \n\n",),
    "copy": (" \t ", int),
    "slide": (" \t\n", int),
    # Arith
    "add": ("\t   ",),
    "sub": ("\t  \t",),
    "mul": ("\t  \n",),
    "div": ("\t \t ",),
    "mod": ("\t \t\t",),
    # Flow
    "mark": ("\n  ", str),
    "call": ("\n \t", str),
    "jump": ("\n \n", str),
    "jz": ("\n\t ", str),
    "jn": ("\n\t\t", str),
    "ret": ("\n\t\n",),
    "end": ("\n\n\n",),
    # Heap
    "store": ("\t\t ",),
    "load": ("\t\t\t",),
}

def main():
    from sys import argv, stderr
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <filename>")
        return 1

    return_code = 0
    def print_error(lineno, message):
        nonlocal return_code
        print(f"Error on line {lineno + 1}:", message, file=stderr)
        return_code = 2

    labels = {}
    instructions = []
    with open(argv[1]) as f:
        for lineno, line in enumerate(f):
            line = re.sub(r"'(.)'|\"(.)\"", lambda match: str(ord(match.group(1) or match.group(2))), line)
            line = re.sub(r"'\\(.)'", sub_backslash, line)
            line = re.sub(r";.*", "", line.strip())
            if not line:
                continue
            if line.endswith(":"):
                line = line.rstrip(":")
                labels[line] = next_label()
                instructions.append((lineno, ["mark", line]))
                continue
            instructions.append((lineno, line.split()))

    for lineno, inst in instructions:
        if inst[0] not in operations:
            print_error(lineno, "Don't know how to assemble `{inst[0]}'")
            continue

        signature = operations[inst[0]]
        if len(inst) != len(signature):
            print_error(lineno, f"Incorrect number of arguments ({len(inst) - 1}) for operation `{inst[0]}'")
            continue

        if len(signature) == 1:
            print(signature[0], end="")
        elif signature[1] == int:
            num = 0
            try:
                num = int(inst[1])
            except ValueError:
                print_error(lineno, "Couldn't coerce argument into integer")
            print(signature[0], convert_number(num), sep="", end="")
        elif signature[1] == str:
            label = inst[1]
            if label not in labels:
                print_error(lineno, f"Unknown target `{label}'")
                continue
            print(signature[0], labels[label], sep="", end="")

    return return_code

if __name__ == "__main__":
    from sys import exit
    exit(main())
