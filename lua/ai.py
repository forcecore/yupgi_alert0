###
### Setup
###

# Faction of the AI
FACTION = None

# internal name, such as multi0
PLAYER_NAME = None

# Player object
PLAYER = None

# The governing BO.
BUILD_ORDER = None



###
### Mod constants
###

ANYPOWER = "ANYPOWER"

BO_ALLIES_NORMAL = {
    "name": "allies_normal",
    "bo": [
        ANYPOWER,
        "tent",
        "proc",
        "proc",
        ANYPOWER,
        "gaweap",
        "fix",
        "dome",
        ANYPOWER,
        "proc",
        "hpad",
        "hpad",
        "atek",
        ANYPOWER
    ]
}

BO_ALLIES_FAST_WEAP = {
    "name": "allies_weap",
    "bo": [
        ANYPOWER,
        "tent",
        "proc",
        "naweap",
        ANYPOWER,
        "proc",
        "fix",
        "proc",
        "dome",
        ANYPOWER,
        "atek",
        ANYPOWER
    ]
}

BO_ALLIES_FAST_AIR = {
    "name": "allies_air",
    "bo": [
        ANYPOWER,
        "tent",
        "proc",
        "proc",
        "dome",
        "hpad",
        ANYPOWER,
        "proc",
        "gaweap",
        "atek",
        ANYPOWER,
        "hpad",
        "hpad",
        "hpad",
        "proc",
        "fix"
    ]
}

BO_ALLIES_ECO = {
    "name": "allies_eco",
    "bo": [
        ANYPOWER,
        "tent",
        "proc",
        "proc",
        ANYPOWER,
        "proc",
        "gaweap",
        "fix",
        ANYPOWER,
        "dome",
        ANYPOWER,
        "atek"
    ]
}

BO_ALLIES_BOS = [BO_ALLIES_NORMAL, BO_ALLIES_ECO, BO_ALLIES_FAST_WEAP, BO_ALLIES_FAST_AIR]

BO_SOVIET_NORMAL = {
    "name": "soviet_normal",
    "bo": [
        ANYPOWER,
        "barr",
        "kenn",
        "proc",
        "proc",
        ANYPOWER,
        "naweap",
        "fix",
        "dome",
        ANYPOWER,
        "proc",
        "afld",
        "afld",
        "stek",
        ANYPOWER
    ]
}

BO_SOVIET_FAST_WEAP = {
    "name": "soviet_weap",
    "bo": [
        ANYPOWER,
        "kenn",
        "proc",
        "naweap",
        ANYPOWER,
        "barr",
        "proc",
        "fix",
        "proc",
        "dome",
        ANYPOWER,
        "stek",
        ANYPOWER
    ]
}

BO_SOVIET_FAST_AIR = {
    "name": "soviet_air",
    "bo": [
        ANYPOWER,
        "barr",
        "proc",
        "proc",
        "dome",
        "afld",
        ANYPOWER,
        "proc",
        "naweap",
        "stek",
        ANYPOWER,
        "afld",
        "afld",
        "afld",
        "fix"
    ]
}

BO_SOVIET_ECO = {
    "name": "soviet_eco",
    "bo": [
        ANYPOWER,
        "kenn",
        "barr",
        "proc",
        "proc",
        ANYPOWER,
        "proc",
        "naweap",
        "fix",
        ANYPOWER,
        "dome",
        ANYPOWER,
        "stek"
    ]
}

BO_SOVIET_BOS = [
    BO_SOVIET_NORMAL, BO_SOVIET_ECO, BO_SOVIET_FAST_WEAP, BO_SOVIET_FAST_AIR
]

BO_MUTANT_NORMAL = {
    "name": "mutant_normal",
    "bo": [
        "qnest",
        "anthill",
        "anthill",
        "qnest",
        "tibtree",
        "vein",
        "qnest",
        "tibtree",
        "anthill",
        "evo"
    ]
}

BO_MUTANT_BOS = [ BO_MUTANT_NORMAL ]


def MOD_is_anypower(name):
    if name == "powr":
        return True
    elif name == "apwr":
        return True
    return False



###
### Python-lua glue
###
#def random(arr):
#    return Utils.Random(arr)



###
### Util functions
###

# All Lua scripts are moddable to fit modder's needs.
# However, things that definitely need modding are prefixed mod_.
# What can be recycled for other mods aren't.

def UTIL_hist(stuff):
    '''
    Given a list of things that AI has, count it.
    '''

    cnts = {}
    for v in stuff:
        if MOD_is_anypower(v):
            v = ANYPOWER

        if v not in cnts:
            cnts[v] = 1
        else:
            cnts[v] += 1

    #for key, val in cnts.items():
    #    Media.DisplayMessage(key)
    #    Media.DisplayMessage(tostring(val))

    return cnts


def UTIL_get_unbuilt(build_order, building_count):
    '''
    Examine what we have and the build order to see if anything is missing.
    If multiple things are missing, return the one that
    occurs early in build_order.
    Returns None when everything in BO is built.
    '''
    cnts = {}

    for name in build_order:
        if name not in building_count:
            return name
        else:
            # count upto this point.
            # now we know how many buildings we should have
            # when BO went well.
            if name not in cnts:
                cnts[name] = 1
            else:
                cnts[name] += 1

            # if we have less buildings than BO orders us to have, then build one.
            if building_count[name] < cnts[name]:
                return name

    return None


###
### Code
###

def chooseBuildOrder(faction):
    '''
    Given faction, choose a build order.
    Currently, random.
    '''

    if faction == "soviet":
        return Utils.Random(BO_SOVIET_BOS)
    elif faction == "allies":
        return Utils.Random(BO_ALLIES_BOS)
    elif faction == "mutants":
        return Utils.Random(BO_MUTANT_BOS)
    else:
        # Fall back to default hacky build-anything mode.
        return None



###
### C# to lua binding functions
###

# Don't touch this! This is a hard-coded constant in C# !!
HACKY_FALLBACK = "hacky_fallback"

def BB_choose_building_to_build(tab):
    '''
    Called by ChooseBuildingToBuild in BaseBuilder.cs
    Thinking process exported to Lua.
    Input: tab: table containing all the parameters from BaseBuilder.cs
    Returns: a rules name of structures to build.
    Modders may return nil on purpose to choose not to build anything.
    '''

    if BUILD_ORDER == None:
        Media.DisplayMessage("No build order for " + FACTION, "BB Warning")
        return HACKY_FALLBACK

    tab = tab[0] # Sandbox quirks
    building_count = UTIL_hist(tab["player_buildings"])

    # Base defenses aren't current focus now.
    # Fall back to hacky behavior.
    if tab["queue_type"] == "defense":
        return HACKY_FALLBACK

    if FACTION != "mutants" and tab["excess_power"] < tab["minimum_excess_power"]:
        # Build power, as we don't have enough excess power.
        if tab["power_gen"] > 0:
            # Media.DisplayMessage("Low power. Building power.", "BB")
            return tab["power"]

    unbuilt = UTIL_get_unbuilt(BUILD_ORDER["bo"], building_count)
    Media.DisplayMessage("Unbuilt: " + unbuilt, "BB Warning")

    if unbuilt == None:
        # If everything is built as BO, fall back to hacky AI builder.
        return HACKY_FALLBACK
    elif unbuilt == ANYPOWER:
        return tab["power"]

    return unbuilt # Build, as in bulid order.


def ActivateAI(params):
    '''
    Initialize stuff. Called by Activate() in HackyAI.
    '''
    # First, I have to know, what I'm playing.
    # Trigger.AfterDelay(DateTime.Seconds(1), Periodic)
    # test(faction)
    FACTION = params[0].lower() # faction of the bot player
    PLAYER_NAME = params[1] # internal name of the bot player. dont lower case this.
    PLAYER = Player.GetPlayer(PLAYER_NAME)
    BUILD_ORDER = chooseBuildOrder(FACTION) # and its attached opener too.


def Tick():
    '''
    Tick the AI thinking. Called by Tick() in Scripted AI.
    '''
    pass
