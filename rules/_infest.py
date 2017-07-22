#!/usr/bin/python3
import pprint
import yaml



def process(fname):
    config = yaml.load_from_file(fname)

    names = list(config.children.keys())
    names.sort()

    for name in names:
        item = config[name]
        if not "TransformOnCapture" in item:
            continue

        print("{}_INFESTED:".format(name))

        print("\tInherits@1: ^Building")
        print("\tInherits@2: ^Infested")

        if "RenderSprites" in item:
            item["RenderSprites"].print()
        else:
            print("\tRenderSprites:")
            print("\t\tImage: " + name.upper())

        if "Valued" in item:
            item["Valued"].print()

        print("\tSelectable:")
        print("\t\tClass: infested_building")

        if "Tooltip" in item:
            print("\tTooltip:")
            print("\t\tName:", "Infested " + item["Tooltip"]["Name"].value)
        else:
            print("\tTooltip:")
            print("\t\tName:", "Infested Civilian Building")

        item["Building"].print()

        if "WithBuildingBib" in item:
            item["WithBuildingBib"].print()

        if "Health" in item:
            item["Health"].print()
        else:
            print("\tHealth:")
            print("\t\tHP: 400")

        if "Armor" in item:
            item["Armor"].print()
        else:
            print("\tArmor:")
            print("\t\tType: Wood")

        if "RevealsShroud" in item:
            item["RevealsShroud"].print()
        else:
            print("\tRevealsShroud:")
            print("\t\tRange: 4c0")

        if "Explodes" in item:
            item["Explodes"].print()

        for key in item.children.keys():
            if key.startswith("HitShape"):
                item[key].print()

        if "WithProductionDoorOverlay" in item:
            item["WithProductionDoorOverlay"].print()

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
