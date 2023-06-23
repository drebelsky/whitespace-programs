# Whitespace Programs

A series of programs written in [Whitespace](https://esolangs.org/wiki/Whitespace). Also see my [Whitespace compiler](https://github.com/drebelsky/whitespace-jit). 

## Structure
* `assemble.py` supports assembling a basic Whitespace assembly language into the actual Whitespace characters.
* `asm/` contains whitespace-assembly versions of the programs.
* `ws/` contains the Whitespace equivalents of the programs.

## Assembly Language
The assembly language supports one command per line. The 24 basic commands are

Command name|Type      |Arguments (empty if none)
:-----------|:---------|:------------------------
rchar       |I/O       |
rnum        |I/O       |
wchar       |I/O       |
wnum        |I/O       |
push        |Stack     |integer
dup         |Stack     |
swap        |Stack     |
pop         |Stack     |
copy        |Stack     |integer
slide       |Stack     |integer
add         |Arithmetic|
sub         |Arithmetic|
mul         |Arithmetic|
div         |Arithmetic|
mod         |Arithmetic|
call        |Flow      |label
jump        |Flow      |label
jz          |Flow      |label
jn          |Flow      |label
ret         |Flow      |
end         |Flow      |
store       |Heap      |
load        |Heap      |

Arguments should be preceded by at least one space.

### Labels
Labels can be made by ending a line with a `:`. To refer to a label as an argument, enter the part of the line before the `:`.

### Numbers
Numbers can be written either in decimal (e.g., `10`, `123`, etc...) or as a character constant (e.g., `'a'`, `"B"`, `'\n'`, or `"\t"`).

### Commenting
`;` can be used for commenting--all characters starting at the `;` and going to the end of the line will be ignored

### Other Miscellaneous Notes
Except for at least one space separating arguments and instructions being separated by newlines, (ironically) white space is ignored.
