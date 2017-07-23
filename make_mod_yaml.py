#!/usr/bin/python3
import sys

ENGINE_VERSION = "playtest-20170722"



ifname = sys.argv[1]
rev = sys.argv[2]

with open(ifname) as f:
    for line in f:
        line = line.rstrip()

        if line.find("DEV-Release") >= 0:
            line = line.replace("DEV", rev)
        elif line.find("{DEV_VERSION}") >= 0:
            line = line.replace("{DEV_VERSION}", ENGINE_VERSION)

        print(line)
