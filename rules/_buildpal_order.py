#!/usr/bin/python3
'''
Python YAML parsers don't work on OpenRA YAML files ugh...
'''
import glob
import io
import poyo

for fname in glob.glob("structures.yaml"):
    with open(fname) as f:
        print(fname)

        stuff = []

        # Read info
        for line in f :
            line = line.rstrip()
            if line == "":
                pass
            elif not line.startswith(" ") and not line.startswith("\t"):
                actor = line.replace(":", "")
            elif line.find("BuildPaletteOrder") >= 0:
                data = line.split(": ")
                order = int(data[1])
                stuff.append((actor, order))

        stuff.sort(key=lambda x: x[1])
        for actor, order in stuff:
            print(actor, order)
