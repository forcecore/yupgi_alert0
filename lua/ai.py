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

# Tick, in this script
TICKS = 0



###
### Mod variables
###

AUTO_BUILD = False



###
### Team actions (not constant but need to be here before team definition)
### Team action can't take parameters so, we do this.
###

def LoadHumvee(actors):
    UTIL_LoadOnto("jeep", actors, None, None)


def LoadTran(actors):
    UTIL_LoadOnto("tran", actors, None, None)



###
### Mod constants
###

ANYPOWER = "ANYPOWER"

# In build order, if you need to expand, write it as MCV.
MCVS = ["gamcv", "namcv", "qant"]

# And when we count buildings, we count them as MCVs to prevent
# computer from producing multiple MCVs when it deploys.
COUNT_BUILDING_AS_MCV = {
    "gafact": "gamcv",
    "nafact": "namcv",
    "qnest": "qant"
}

# Lua supports list or dict so...
HELI_TRANSPORT = {
    "tran": True
}

AMMO_POOLED_AIRCRAFTS = ["nmig", "mig", "yak", "hind", "heli"]

# Lua supports list or dict so...
FIXABLE = {
    "2tnk": True,
    "3tnk": True,
    "4tnk": True
}

# Ground static defense
STATIC_DEFENSES = ["pbox", "hbox", "gun", "ftur", "tsla"]

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
        "gaweap",
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
        "qant",
        "anthill",
        "anthill",
        "qant",
        "tibtree",
        "vein",
        "qant",
        "tibtree",
        "anthill",
        "evo"
    ]
}

BO_MUTANT_BOS = [ BO_MUTANT_NORMAL ]

TASKFORCES = {
    # Allied taskforces.
    # These are basic units of production. They may be merged into a big team.
    "6_heli": {
        "units": ["heli", "heli", "heli", "heli"],
    },
    "2_hind": {
        "units": ["hind", "hind"],
    },
    "5_e1": {
        "units": ["e1","e1","e1","e1","e1"],
    },
    "2_e3": {
        "units": ["e3", "e3"],
    },
    "2_jeep": {
        "units": ["jeep", "jeep"],
    },
    "4_1tnk": {
        "units": ["1tnk", "1tnk", "1tnk", "1tnk"],
    },
    "4_2tnk": {
        "units": ["2tnk", "2tnk", "2tnk", "2tnk"],
    },
    "arty": {
        "units": ["arty", "arty", "2tnk", "2tnk"],
    },
    "humvee": {
        "units": ["jeep", "e1", "e3", "e3"],
    },
    "tran": {
        "units": ["tran", "e1", "e1", "e3", "e3", "e3"],
    },

    # Soviet taskforces
    "2_e2": {
        "units": ["e2", "e2"],
    },
    "4_dog": {
        "units": ["dog", "dog", "dog", "dog"],
    },
    "2_e4": {
        "units": ["e4", "e4"],
    },
    "2_shok": {
        "units": ["shok", "shok"],
    },
    "2_ftrk": {
        "units": ["ftrk", "ftrk"],
    },
    "4_3tnk": {
        "units": ["3tnk", "3tnk", "3tnk", "3tnk"],
    },
    "2_4tnk": {
        "units": ["4tnk", "4tnk"],
    },
    "ttnk": {
        "units": ["ttnk"],
    },
    "v2rl": {
        "units": ["v2rl", "v2rl", "3tnk", "3tnk"],
    },
    "4_mig": {
        "units": ["mig", "mig", "mig", "mig"],
    },
    "2_yak": {
        "units": ["yak", "yak"],
    },

    # Mutant TFs
    "2_want": {
        "units": ["want", "want"],
    },
    "2_fant": {
        "units": ["fant", "fant"],
    },
    "1_sant": {
        "units": ["sant"],
    },
    "1_hant": {
        "units": ["hant"],
    },
    "1_inft": {
        "units": ["inft"],
    },
    "3_doggie": {
        "units": ["doggie", "doggie", "doggie"],
    }
}

TEAMS = {
    # Allies Teams
    "6_heli": {
        "faction": "allies",
        "tf": "6_heli",
        "trigger": None
    },
    "2_hind": {
        "faction": "allies",
        "tf": "2_hind",
        "trigger": None
    },
    "5_e1": {
        "faction": "allies",
        "tf": "5_e1",
        "trigger": None
    },
    "2_e3": {
        "faction": "allies",
        "tf": "2_e3",
        "trigger": None
    },
    "2_jeep": {
        "faction": "allies",
        "tf": "2_jeep",
        "trigger": None
    },
    #"4_1tnk": {
    #    "faction": "allies",
    #    "tf": "4_1tnk",
    #    "trigger": None
    #},
    "4_2tnk": {
        "faction": "allies",
        "tf": "4_2tnk",
        "trigger": None
    },
    "arty": {
        "faction": "allies",
        "tf": "arty",
        "trigger": None
    },
    "humvee": {
        "faction": "allies",
        "tf": "humvee",
        "trigger": LoadHumvee
    },
    "tran": {
        "faction": "allies",
        "tf": "tran",
        "trigger": LoadTran
    },

    # Soviet Teams
    "2_e2": {
        "faction": "soviet",
        "tf": "2_e2",
        "queue": "inf",
        "trigger": None
    },
    "4_dog": {
        "faction": "soviet",
        "tf": "4_dog",
        "trigger": None
    },
    "2_e4": {
        "faction": "soviet",
        "tf": "2_e4",
        "trigger": None
    },
    "2_shok": {
        "faction": "soviet",
        "tf": "2_shok",
        "trigger": None
    },
    "2_ftrk": {
        "faction": "soviet",
        "tf": "2_ftrk",
        "trigger": None
    },
    "4_3tnk": {
        "faction": "soviet",
        "tf": "4_3tnk",
        "trigger": None
    },
    "2_4tnk": {
        "faction": "soviet",
        "tf": "2_4tnk",
        "trigger": None
    },
    "ttnk": {
        "faction": "soviet",
        "tf": "ttnk",
        "trigger": None
    },
    "v2rl": {
        "faction": "soviet",
        "tf": "v2rl",
        "trigger": None
    },
    "4_mig": {
        "faction": "soviet",
        "tf": "4_mig",
        "trigger": None
    },
    "2_yak": {
        "faction": "soviet",
        "tf": "2_yak",
        "trigger": None
    },
    "1_zep": {
        "faction": "soviet",
        "tf": "1_zep",
        "trigger": None
    },

    # Ant teams
    "2_want": {
        "faction": "mutants",
        "tf": "2_want",
        "trigger": None
    },
    "2_fant": {
        "faction": "mutants",
        "tf": "2_fant",
        "trigger": None
    },
    "1_sant": {
        "faction": "mutants",
        "tf": "1_sant",
        "trigger": None
    },
    "1_hant": {
        "faction": "mutants",
        "tf": "1_hant",
        "trigger": None
    },
    "1_inft": {
        "faction": "mutants",
        "tf": "1_inft",
        "trigger": None
    },
    "3_doggie": {
        "faction": "mutants",
        "tf": "3_doggie",
        "trigger": None
    }
}

ALLIES_TEAMS_KEYS = []
for key, team in TEAMS.items():
    if team["faction"] == "allies":
        ALLIES_TEAMS_KEYS.append(key)

SOVIET_TEAMS_KEYS = []
for key, team in TEAMS.items():
    if team["faction"] == "soviet":
        SOVIET_TEAMS_KEYS.append(key)

MUTANT_TEAMS_KEYS = []
for key, team in TEAMS.items():
    if team["faction"] == "mutants":
        MUTANT_TEAMS_KEYS.append(key)



###
### Mod functions
###


def IsAnypower(name):
    if name == "powr":
        return True
    elif name == "apwr":
        return True
    return False


def ChooseBuildOrder(faction):
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


def NeedToRebuildMCV(faction):
    if faction == "allies":
        return UTIL_Count('gamcv') == 0 and UTIL_Count('gafact') == 0
    if faction == "soviet":
        return UTIL_Count('namcv') == 0 and UTIL_Count('nafact') == 0

    # For mutants.
    # If you Have QNEST or QANT you are find.
    # If you have no QNEST, you can't build QANT anyway.
    # Just return False.
    return False


def CanRebuildMCV(faction):
    if faction == "allies":
        return PLAYER.HasPrerequisites(["gaweap"])
    if faction == "soviet":
        return PLAYER.HasPrerequisites(["naweap"])
    if faction == "mutants":
        return PLAYER.HasPrerequisites(["qnest"])

    Media.DisplayMessage("CanRebuildMCV() has reached invalid execution path")
    return False


def AlliesBuildUnitTick(faction):
    harvs = PLAYER.GetActorsByType('harv')

    if not AUTO_BUILD:
        e1s = PLAYER.GetActorsByType('e1')
        if len(e1s) < 10 and PLAYER.HasPrerequisites(["tent"]):
            PLAYER.Build(['e1'], None)

        if len(harvs) < 3 and PLAYER.HasPrerequisites(["gaweap", "proc"]):
            PLAYER.Build(['harv'], None)

        if len(harvs) >= 3 and len(e1s) >= 10:
            AUTO_BUILD = True

    else:
        if len(harvs) < 1 and PLAYER.HasPrerequisites(["gaweap", "proc"]):
            PLAYER.Build(['harv'], None)
            return

        if NeedToRebuildMCV(faction) and CanRebuildMCV(faction):
            PLAYER.Build(['gamcv'], None)
            return

        if len(harvs) < 3 and PLAYER.HasPrerequisites(["gaweap", "proc"]):
            PLAYER.Build(['harv'], None)
            return

        if len(harvs) < 5 and PLAYER.HasPrerequisites(["gaweap", "proc", "fix"]):
            PLAYER.Build(['harv'], None)
        elif len(harvs) < 7 and PLAYER.HasPrerequisites(["gaweap", "proc", "atek"]):
            PLAYER.Build(['harv'], None)
        elif UTIL_Count("marv") < 2 and PLAYER.HasPrerequisites(["gaweap", "proc", "atek"]):
            PLAYER.Build(['marv'], None)

        enemy = UTIL_GetAnEnemyPlayer()
        defense_cnt = UTIL_CountUnits(enemy, STATIC_DEFENSES)
        if defense_cnt >= 4:
            if UTIL_Count("msam") < 2 and PLAYER.HasPrerequisites(["gaweap", "atek"]):
                PLAYER.Build(['msam'], None)
            if UTIL_Count("arty") < 4 and PLAYER.HasPrerequisites(["gaweap", "dome"]):
                PLAYER.Build(['arty'], None)

        UTIL_BuildRandomTeam(ALLIES_TEAMS_KEYS)


def BuildUnitTick(faction):
    if faction == "allies":
        AlliesBuildUnitTick(faction)
    elif faction == "soviets":
        SovietBuildUnitTick(faction)
    elif faction == "mutants":
        MutantBuildUnitTick(faction)



###
### Util functions
###

# All Lua scripts are moddable to fit modder's needs.
# However, things that definitely need modding are prefixed mod_.
# What can be recycled for other mods aren't.


def UTIL_CanQueue(tf):
    for name in tf["units"]:
        if PLAYER.IsProducing(name):
            return False
    return True


def UTIL_LoadOnto(transportName, actors, afterLoadFunc, afterLoadParams):
    UTIL_SetOccupied(actors, True)

    tran = None
    load = []
    for a in actors:
        if a.Type == transportName:
            tran = a
        else:
            load.append(a)

    UTIL_MoveTransportToPassengers(tran, load, afterLoadFunc, afterLoadParams)


def UTIL_SetOccupied(actors, isOccupied):
    for a in actors:
        if not a.IsDead:
            a.HackyAIOccupied = isOccupied


def UTIL_CountAlive(actors):
    cnt = 0
    for a in actors:
        if not a.IsDead:
            cnt += 1
    return cnt


def UTIL_WaitLoad(transport, passengers, afterLoadFunc, afterLoadParams):
    if transport.IsDead:
        UTIL_SetOccupied(passengers, False)
        return

    if transport.PassengerCount >= UTIL_CountAlive(passengers):
        if afterLoadFunc == None:
            transport.HackyAIOccupied = False
            UTIL_SetOccupied(passengers, False)
        else:
            afterLoadFunc(afterLoadParams)
    else:
        Trigger.AfterDelay(30, lambda:
            # invoke self again to implement "wait load".
            # If you use something else, game hangs haha
            UTIL_WaitLoad(transport, passengers, afterLoadFunc, afterLoadParams)
        )


def UTIL_MoveTransportToPassengers(transport, passengers, afterLoadFunc, afterLoadParams):
    # Find a suitable cell.
    guest = passengers[0]

    for cell in Map.FindTilesInAnnulus(guest.Location, 1, 4):
        # Don't use transport.CanEnter. transport might not have mobile property.
        if guest.CanEnter(cell):
            transport.Wait(50)
            transport.Stop() # Make it stop wandering around, if heli
            transport.Move(cell, 2048)
            if HELI_TRANSPORT[transport.Type] == True:
                transport.HeliLand(transport, True)
            transport.CallFunc(lambda:
                    UTIL_LoadPassengers(transport, passengers,
                        afterLoadFunc, afterLoadParams))


def UTIL_LoadPassengers(transport, passengers, afterLoadFunc, afterLoadParams):
    '''
    Order just once, or else it will bug.
    '''
    for a in passengers:
        a.EnterTransport(transport)
    UTIL_WaitLoad(transport, passengers, afterLoadFunc, afterLoadParams)


def UTIL_BuildRandomTeam(keys):
    '''
    Given teams, and its keys, build a random team and return success/fail
    '''

    # Get teams that can be built using unoccupied queue.
    avail = []
    for key in keys:
        tf = TASKFORCES[TEAMS[key]["tf"]]
        if UTIL_CanQueue(tf):
            avail.append(key)

    if len(avail) == 0:
        return False

    key = Utils.Random(avail)
    return UTIL_BuildTeam(key)


def UTIL_BuildTeam(key):
    team = TEAMS[key]
    taskforce = TASKFORCES[team["tf"]]
    return PLAYER.Build(taskforce["units"], team["trigger"])


def UTIL_CountBuildings(stuff):
    '''
    Given a list of things that AI has, count it.
    '''

    cnts = {}

    # Count MCVs first, because there's no need for "existence" check.
    for name in MCVS:
        actors = PLAYER.GetActorsByType(name)
        cnts[name] = len(actors)

    for v in stuff:
        if IsAnypower(v):
            v = ANYPOWER
        elif v in COUNT_BUILDING_AS_MCV:
            v = COUNT_BUILDING_AS_MCV[v]

        if v not in cnts:
            cnts[v] = 1
        else:
            cnts[v] += 1

    #for key, val in cnts.items():
    #    Media.DisplayMessage(key)
    #    Media.DisplayMessage(tostring(val))

    return cnts


def UTIL_GetUnbuilt(build_order, building_count):
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


def UTIL_Count(name):
    '''
    Given one actor type, count the number of it, owned by AI.
    Special case of UTIL_CountUnits but occurs very often so made a function.
    '''
    return len(PLAYER.GetActorsByType(name))


def UTIL_CountUnits(p, unit_types):
    '''
    Count unit types, owned by player
    Not histogram like UTIL_hist.
    Just count them and return integer.
    '''
    cnt = 0

    for name in unit_types:
        units = p.GetActorsByType(name)
        if units != None:
            cnt += len(units)

    return cnt


def UTIL_IsEnemyWithAI(p):
    if p.InternalName == "Neutral":
        return False
    if p.InternalName == "Creeps":
        return False
    if p.InternalName == "Everyone":
        return False
    if p.InternalName == PLAYER.InternalName:
        return False
    if p.IsAlliedWith(PLAYER):
        return False
    return True


def UTIL_GetAnEnemyPlayer():
    '''
    Currently we choose an enemy player by random.
    We may introduce policies in the future.
    '''

    enemies = []
    for p in Player.GetPlayers(None):
        if UTIL_IsEnemyWithAI(p):
            enemies.append(p)

    if len(enemies) == 0:
        return None

    return Utils.Random(enemies)


def UTIL_ReloadAircraft(ammo_pooled_aircrafts):
    for name in ammo_pooled_aircrafts:
        units = PLAYER.GetActorsByType(name)
        for unit in units:
            if unit.AmmoCount() == 0 and not unit.HackyAIOccupied:
                # Don't let this unit be recruited
                unit.HackyAIOccupied = True
            elif unit.AmmoCount() == unit.MaximumAmmoCount() and \
                    unit.Health == unit.MaxHealth and unit.HackyAIOccupied:
                # Mark as recruitable
                unit.HackyAIOccupied = False


def UTIL_RepairUnits():
    if not PLAYER.HasPrerequisites(["fix"]):
        return

    fix = PLAYER.GetActorsByType("fix")[0]

    actors = PLAYER.GetActors()
    for a in actors:
        if a.Type in FIXABLE and a.Health < a.MaxHealth / 10 and not a.HackyAIOccupied:
            a.HackyAIOccupied = True
            a.Stop() # Cancel whatever it was doing
            a.RepairAt(fix)
        elif a.Type in FIXABLE and a.Health == a.MaxHealth and a.HackyAIOccupied:
            a.HackyAIOccupied = False


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
    building_count = UTIL_CountBuildings(tab["player_buildings"])

    # Base defenses aren't current focus now.
    # Fall back to hacky behavior.
    if tab["queue_type"] == "defense":
        return HACKY_FALLBACK

    if FACTION != "mutants" and tab["excess_power"] < tab["minimum_excess_power"]:
        # Build power, as we don't have enough excess power.
        if tab["power_gen"] > 0:
            # Media.DisplayMessage("Low power. Building power.", "BB")
            return tab["power"]

    unbuilt = UTIL_GetUnbuilt(BUILD_ORDER["bo"], building_count)

    if unbuilt == None:
        # If everything is built as BO, fall back to hacky AI builder.
        return HACKY_FALLBACK
    elif unbuilt == ANYPOWER:
        return tab["power"]

    #Media.DisplayMessage("Unbuilt: " + unbuilt, "BB Warning")
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
    BUILD_ORDER = ChooseBuildOrder(FACTION) # and its attached opener too.


def Tick():
    '''
    Tick the AI thinking. Called by Tick() in Scripted AI.
    '''

    TICKS += 1
    # Make sure nothing runs at the first tick.
    # (tick == 1)

    # In once a second or so,
    if TICKS % 31 == 0:
        BuildUnitTick(FACTION)
    elif TICKS % 37 == 0:
        UTIL_ReloadAircraft(AMMO_POOLED_AIRCRAFTS)
    elif TICKS % 127 == 0:
        UTIL_RepairUnits()
