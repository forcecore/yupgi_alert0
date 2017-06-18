#!/usr/bin/python3
import pprint
import poyo



def emit(key, config, level):
    val = config[key]

    if type(val) is dict:
        print("{}{}:".format("\t" * level, key))
        for k in val.keys():
            emit(k, val, level + 1)
    else:
        print("{}{}: {}".format("\t" * level, key, val))



def process(fname):
    with open(fname) as f:
        slurp = f.read()
        slurp = slurp.replace("\t", "    ")

    config = poyo.parse_string(slurp)

    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(config)

    names = list(config.keys())
    names.sort()

    for name in names:
        item = config[name]
        if not "TransformOnCapture" in item:
            continue

        print("{}_INFESTED:".format(name))

        print("\tInherits@1: ^Building")
        print("\tInherits@2: ^Infested")

        if "RenderSprites" in item:
            emit("RenderSprites", item, 1)
        else:
            print("\tRenderSprites:")
            print("\t\tImage: " + name.upper())

        if "Valued" in item:
            emit("Valued", item, 1)

        print("\tSelectable:")
        print("\t\tClass: infested_building")

        if "Tooltip" in item:
            print("\tTooltip:")
            print("\t\tName:", "Infested " + item["Tooltip"]["Name"])
        else:
            print("\tTooltip:")
            print("\t\tName:", "Infested Civilian Building")

        emit("Building", item, 1)

        if "Bib" in item:
            emit("Bib", item, 1)

        if "Health" in item:
            emit("Health", item, 1)
        else:
            print("\tHealth:")
            print("\t\tHP: 400")

        if "Armor" in item:
            emit("Armor", item, 1)
        else:
            print("\tArmor:")
            print("\t\tType: Wood")

        if "RevealsShroud" in item:
            emit("RevealsShroud", item, 1)
        else:
            print("\tRevealsShroud:")
            print("\t\tRange: 4c0")

        if "Explodes" in item:
            emit("Explodes", item, 1)

        if "WithProductionDoorOverlay" in item:
            emit("WithProductionDoorOverlay", item, 1)

        print("\tMustBeDestroyed:")
        print("\t\tRequiredForShortGame: true")

        print("\t-EmitInfantryOnSell:")
        print("\t-Sellable:")

        print()

if __name__ == "__main__":
    print("# Emitted by infest.py, don't edit by hand :)")
    print()
    process("structures.yaml")
    process("fakes.yaml")
    process("civilian.yaml")
