import os
from pylua.pylua import run_file

run_file("ai.py")
os.replace("_pylua_temp.lua", "ai.lua")
