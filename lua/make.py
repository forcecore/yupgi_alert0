import os
from pylua.pylua import run_file

def include(g, fname):
    with open(fname) as f:
        for line in f:
            line = line.rstrip()
            print(line, file=g)

g = open("evo.py", "w")
with open("evo.src.py") as f:
    for line in f:
        line = line.rstrip()
        if line.startswith("#INCLUDE"):
            data = line.split(" ")
            fname = data[1]
            include(g, fname)
        else:
            print(line, file=g)

g.close()
run_file("evo.py")
os.replace("_pylua_temp.lua", "evo.lua")
