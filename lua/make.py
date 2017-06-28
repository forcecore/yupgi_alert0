#!/usr/bin/python3
import os
from pylua.pylua import run_file

run_file("evo.py")
os.replace("_pylua_temp.lua", "evo.lua")
