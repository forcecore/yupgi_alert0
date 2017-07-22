#!/usr/bin/python3
import yaml



def process(fname):
    config = yaml.load_from_file(fname)

    names = list(config.children.keys())

    for name in names:
        if name.find("soviet") < 0:
            continue

        key = config[name].key.replace('soviet', 'creepies')
        value = config[name].value
        children = config[name].children

        print("{}: {}".format(key, value))
        for value in children.values():
            value.print()
        print()

if __name__ == "__main__":
    print("# Emitted by _ant_chrome.py, don't edit by hand :)")
    print()
    process("../chrome.yaml")
