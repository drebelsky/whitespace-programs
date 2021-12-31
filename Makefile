WSA_FILES=$(wildcard asm/*.wsa)
WS_FILES=$(patsubst asm/%.wsa, ws/%.ws, $(WSA_FILES))

default: $(WS_FILES)

clean:
	rm ws/*.ws

ws/%.ws: asm/%.wsa
	python3 assemble.py $^ > $@ || rm $@

.PHONY: default
