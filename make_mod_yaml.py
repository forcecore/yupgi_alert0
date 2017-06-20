#!/usr/bin/python3
import sys

MOD_CHOOSER = "release-20170527"



ifname = sys.argv[1]
rev = sys.argv[2]

with open(ifname) as f:
    for line in f:
        line = line.rstrip()

        if line.find("DEV-Release") >= 0:
            line = line.replace("DEV", rev)
        elif line.find("{DEV_VERSION}") >= 0:
            line = line.replace("{DEV_VERSION}", MOD_CHOOSER)
        elif line.find("Mods.Common.dll") >= 0:
            line = "\tyupgi_alert|OpenRA.Mods.Uncommon.dll"

        print(line)
