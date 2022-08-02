.PHONY: all run clean

all: clean compilation pprinter interpreter

pprinter: 
	python3 src/prettyMain.py
compilation: 
	python3 src/compMain.py 
interpreter: 
	python3 src/interpreterMain.py 
clean:
	rm -rf __pycache__
