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
BUILD_TICK_FUNC = None
BELONGS_TO_A_TEAM = {}



###
### Team actions (not constant but need to be here before team definition)
### Team action can't take parameters so, we do this.
###

def LoadHumvee(actors):
    #UTIL_LoadOnto("jeep", actors, None, None)
    UTIL_LoadOnto("jeep", actors, ACT_AttackPower, actors)


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
STATIC_DEFENSES = ["pbox", "hbox", "gun", "ftur", "tsla", "agun", "sam", "minihive"]

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
        "evo", # BUILD 2 to evolve want and fant
        "evo"
    ]
}

BO_MUTANT_BOS = [ BO_MUTANT_NORMAL ]



###
### Teams and actions
###

def ACT_AttackTypes(actors, types):
    # Find a powerplant.
    enemy = UTIL_GetAnEnemyPlayer()
    targets = []
    for ty in types:
        tmp = enemy.GetActorsByType(ty)
        if len(tmp) > 0:
            for t in tmp:
                targets.append(t)

    UTIL_SetOccupied(actors, True)
    Utils.Shuffle(targets)

    for a in actors:
        for t in targets:
            a.Attack(t)
            # Just attack one target. Others won't be so close mostly.
            break
        a.Hunt()

def ACT_AttackPower(actors):
    ACT_AttackTypes(actors, ['apwr', 'powr', 'anthill'])

def ACT_AttackRef(actors):
    ACT_AttackTypes(actors, ['proc', 'anthill'])

def ACT_AttackFactory(actors):
    ACT_AttackTypes(actors, ['gaweap', 'naweap', 'evo', 'qnest'])

def ACT_AttackBarracks(actors):
    ACT_AttackTypes(actors, ['tent', 'barr', 'qnest'])

def ACT_AttackCY(actors):
    ACT_AttackTypes(actors, ['gafact', 'nafact', 'qnest'])

def ACT_Hunt(actors):
    UTIL_SetOccupied(actors, True)
    for a in actors:
        a.Hunt()

def ACT_AttackStaticDefenses(actors):
    ACT_AttackTypes(actors, STATIC_DEFENSES)


TEAMS = {
    # Allies Teams
    "1_e1": {
        "faction": "allies",
        "tf": "1_e1",
        "trigger": None
    },
    "1_e3": {
        "faction": "allies",
        "tf": "1_e3",
        "trigger": None
    },
    "1_jeep": {
        "faction": "allies",
        "tf": "1_jeep",
        "trigger": None
    },
    #"1_1tnk": {
    #    "faction": "allies",
    #    "tf": "1_1tnk",
    #    "trigger": None
    #},
    "1_2tnk": {
        "faction": "allies",
        "tf": "1_2tnk",
        "trigger": None
    },
    "arty": {
        "faction": "allies",
        "tf": "arty",
        "trigger": None
    },
    "humvee": {
        "faction": "allies",
        "units": ["jeep", "e1", "e3"],
        "cnts" : [2, 2, 4],
        "trigger": LoadHumvee
    },
    "tran": {
        "faction": "allies",
        "units": ["tran", "e1", "e3"],
        "cnts" : [1, 2, 3],
        "trigger": LoadTran
    },

    # Soviet Teams
    "1_e2": {
        "faction": "soviet",
        "tf": "1_e2",
        "trigger": None
    },
    "1_deso": {
        "faction": "soviet",
        "tf": "1_deso",
        "trigger": None
    },
    "1_e4": {
        "faction": "soviet",
        "tf": "1_e4",
        "trigger": None
    },
    "1_shok": {
        "faction": "soviet",
        "tf": "1_shok",
        "trigger": None
    },
    "1_ftrk": {
        "faction": "soviet",
        "tf": "1_ftrk",
        "trigger": None
    },
    "1_qtnk": {
        "faction": "soviet",
        "tf": "1_qtnk",
        "trigger": None
    },
    "1_3tnk": {
        "faction": "soviet",
        "tf": "1_3tnk",
        "trigger": None
    },
    "1_4tnk": {
        "faction": "soviet",
        "tf": "1_4tnk",
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
    "1_zep": {
        "faction": "soviet",
        "tf": "1_zep",
        "trigger": None
    },

    # Ant teams
    "5_want": {
        "faction": "mutants",
        "tf": "5_want",
        "trigger": None
    },
    "2_fant": {
        "faction": "mutants",
        "tf": "4_fant",
        "trigger": None
    },
    "2_doggie": {
        "faction": "mutants",
        "tf": "2_doggie",
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
            if Utils.RandomInteger(0, 4) == 0:
                PLAYER.Build(['harv'], None)
        elif UTIL_Count("marv") < 2 and PLAYER.HasPrerequisites(["gaweap", "proc", "atek"]):
            if Utils.RandomInteger(0, 4) == 0:
                PLAYER.Build(['marv'], None)

        if UTIL_Count("wangchang") < 3 and PLAYER.HasPrerequisites(["gaweap", "atek"]):
            if Utils.RandomInteger(0, 4) == 0:
                PLAYER.Build(['wangchang'], None)

        if UTIL_Count("e7") < 2 and PLAYER.HasPrerequisites(["gaweap", "tent", "atek"]):
            if Utils.RandomInteger(0, 4) == 0:
                PLAYER.Build(['e7'], None)

        if UTIL_Count("tran") < 4 and PLAYER.HasPrerequisites(["hpad", "tent"]):
            if Utils.RandomInteger(0, 4) == 0:
                UTIL_BuildTeam("tran")
        elif UTIL_Count("heli") < 4 * UTIL_Count("hpad") and \
                PLAYER.HasPrerequisites(["hpad", "atek"]):
            if Utils.RandomInteger(0, 2) == 0:
                PLAYER.Build(['heli'], None)
        elif UTIL_Count("hind") < 4 * UTIL_Count("hpad") and \
                PLAYER.HasPrerequisites(["hpad"]):
            if Utils.RandomInteger(0, 4) == 0:
                PLAYER.Build(['hind'], None)

        enemy = UTIL_GetAnEnemyPlayer()
        defense_cnt = UTIL_CountUnits(enemy, STATIC_DEFENSES)
        if defense_cnt >= 4:
            if UTIL_Count("msam") < 2 and PLAYER.HasPrerequisites(["gaweap", "atek"]):
                PLAYER.Build(['msam'], None)
            if UTIL_Count("arty") < 4 and PLAYER.HasPrerequisites(["gaweap", "dome"]):
                PLAYER.Build(['arty'], None)

        if PLAYER.Cash > 500:
            UTIL_BuildRandomTeam(ALLIES_TEAMS_KEYS)


def SovietBuildUnitTick(faction):
    harvs = PLAYER.GetActorsByType('harv')

    if not AUTO_BUILD:
        e1s = PLAYER.GetActorsByType('e1')
        if len(e1s) < 10 and PLAYER.HasPrerequisites(["barr"]):
            PLAYER.Build(['e1'], None)

        if UTIL_Count("dog") < 4 and PLAYER.HasPrerequisites(["kenn"]):
            PLAYER.Build(['dog'], None)

        if len(harvs) < 3 and PLAYER.HasPrerequisites(["naweap", "proc"]):
            PLAYER.Build(['harv'], None)

        if len(harvs) >= 3 and len(e1s) >= 10:
            AUTO_BUILD = True

    else:
        if len(harvs) < 1 and PLAYER.HasPrerequisites(["naweap", "proc"]):
            PLAYER.Build(['harv'], None)
            return

        if NeedToRebuildMCV(faction) and CanRebuildMCV(faction):
            PLAYER.Build(['namcv'], None)
            return

        if len(harvs) < 3 and PLAYER.HasPrerequisites(["naweap", "proc"]):
            PLAYER.Build(['harv'], None)
            return

        if UTIL_Count("dog") < 4 and PLAYER.HasPrerequisites(["kenn"]):
            PLAYER.Build(['dog'], None)

        if len(harvs) < 5 and PLAYER.HasPrerequisites(["naweap", "proc", "fix"]):
            PLAYER.Build(['harv'], None)
        elif len(harvs) < 7 and PLAYER.HasPrerequisites(["naweap", "proc", "stek"]):
            if Utils.RandomInteger(0, 4) == 0:
                PLAYER.Build(['harv'], None)
        elif UTIL_Count("smin") < 2 and PLAYER.HasPrerequisites(["naweap", "proc", "stek"]):
            if Utils.RandomInteger(0, 4) == 0:
                PLAYER.Build(['smin'], None)

        if UTIL_Count("5tnk") == 0 and PLAYER.HasPrerequisites(["naweap", "fix", "stek"]):
            if Utils.RandomInteger(0, 4) == 0:
                PLAYER.Build(['5tnk'], None)

        if UTIL_Count("nmig") == 0 and PLAYER.HasPrerequisites(["afld", "stek", "mslo"]):
            if Utils.RandomInteger(0, 2) == 0:
                PLAYER.Build(['nmig'], None)
        elif UTIL_Count("mig") < 4 * UTIL_Count("afld") and \
                PLAYER.HasPrerequisites(["afld", "stek"]):
            if Utils.RandomInteger(0, 2) == 0:
                PLAYER.Build(['mig'], None)
        elif UTIL_Count("yak") < 4 * UTIL_Count("afld") and \
                PLAYER.HasPrerequisites(["afld"]):
            if Utils.RandomInteger(0, 4) == 0:
                PLAYER.Build(['yak'], None)

        if UTIL_Count("volkov") == 0 and PLAYER.HasPrerequisites(["barr", "stek"]):
            if Utils.RandomInteger(0, 2) == 0:
                PLAYER.Build(['volkov'], None)
        elif UTIL_Count("chitz") == 0 and PLAYER.HasPrerequisites(["kenn", "stek"]):
            if Utils.RandomInteger(0, 4) == 0:
                PLAYER.Build(['chitz'], None)

        # Not that much need for V2RL, chitz, volkov are all good for killing def
        #enemy = UTIL_GetAnEnemyPlayer()
        #defense_cnt = UTIL_CountUnits(enemy, STATIC_DEFENSES)
        #if defense_cnt >= 4:
        #    if UTIL_Count("v2rl") < 4 and PLAYER.HasPrerequisites(["naweap", "dome"]):
        #        PLAYER.Build(['v2rl'], None)

        if PLAYER.Cash > 500:
            UTIL_BuildRandomTeam(SOVIET_TEAMS_KEYS)


def Evolve(name, evoIndex):
    evos = PLAYER.GetActorsByType('evo')
    if len(evos) == 1 and evoIndex == 1:
        return
    # lua indexing convention.
    evo = evos[evoIndex + 1]

    victims = PLAYER.GetActorsByType(name)
    for a in victims:
        if a.IsIdle:
            a.HackyAIOccupied = True
            a.Move(evo.Location, 2)
            # When full, tell them to get out.
            if evo.PassengerCount == 5:
                evo.UnloadPassengers()
            a.CallFunc(lambda: UTIL_LoadPassengers(evo, [a], None, None))
            return


def MutantBuildUnitTick(faction):
    dants = PLAYER.GetActorsByType('dant')

    if not AUTO_BUILD:
        if len(dants) < 10 and PLAYER.HasPrerequisites(["qnest"]):
            PLAYER.Build(['dant'], None)
        else:
            AUTO_BUILD = True
    else:
        if len(dants) < 20 and PLAYER.HasPrerequisites(["vein"]):
            PLAYER.Build(['dant'], None)

        if NeedToRebuildMCV(faction) and CanRebuildMCV(faction):
            PLAYER.Build(['qant'], None)
            return

        if len(dants) < 30 and PLAYER.HasPrerequisites(["evo"]):
            PLAYER.Build(['dant'], None)

        # Evolve stuff
        if PLAYER.HasPrerequisites(["evo"]):
            if UTIL_Count("inft") < 6:
                PLAYER.Build(['inft'], None)
            if UTIL_Count("want") > 10:
                Evolve("want", 0)
            if UTIL_Count("fant") > 10:
                Evolve("fant", 1)

        if PLAYER.Cash > 500:
            UTIL_BuildRandomTeam(MUTANT_TEAMS_KEYS)



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

    tran = []
    load = []
    for a in actors:
        if a.Type == transportName:
            tran.append(a)
        else:
            load.append(a)

    UTIL_LoadTransports(tran, load, afterLoadFunc, afterLoadParams)


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


def UTIL_LoadTransports(transports, passengers, afterLoadFunc, afterLoadParams):
    passengerss = []

    for i, p in enumerate(passengers):
        index = i % len(transports) + 1 # +1 for lua convention.
        if passengerss[index] == None:
            passengerss[index] = [p]
        else:
            passengerss[index].append(p)

    for i, ps in enumerate(passengerss):
        UTIL_MoveTransportToPassengers(transports[i], ps, afterLoadFunc, afterLoadParams)


def UTIL_MoveTransportToPassengers(transport, passengers, afterLoadFunc, afterLoadParams):
    # Find a suitable cell.
    guest = passengers[0]

    for cell in Map.FindTilesInAnnulus(guest.Location, 1, 4):
        # Don't use transport.CanEnter. transport might not have mobile property.
        if guest.CanEnter(cell):
            transport.Wait(50)
            transport.Stop() # Make it stop wandering around, if heli
            transport.Move(cell, 2)
            if HELI_TRANSPORT[transport.Type] == True:
                transport.HeliLand(transport, True)
            transport.CallFunc(lambda:
                    UTIL_LoadPassengers(transport, passengers,
                        afterLoadFunc, afterLoadParams))
            break


def UTIL_LoadPassengers(transport, passengers, afterLoadFunc, afterLoadParams):
    '''
    Order just once, or else it will bug.
    '''
    if transport.IsDead:
        UTIL_SetOccupied(passengers, False)
        return

    for a in passengers:
        if not a.IsDead:
            a.EnterTransport(transport)

    UTIL_WaitLoad(transport, passengers, afterLoadFunc, afterLoadParams)


def UTIL_BuildRandomTeam(keys):
    '''
    Given teams, and its keys, build a random team and return success/fail
    '''

    # Get teams that can be built using unoccupied queue.
    #avail = []
    #for key in keys:
    #    tf = TASKFORCES[TEAMS[key]["tf"]]
    #    if UTIL_CanQueue(tf):
    #        avail.append(key)

    #if len(avail) == 0:
    #    return False

    #key = Utils.Random(avail)
    key = 'humvee'
    #Media.DisplayMessage(key)
    return UTIL_BuildTeam(key)


# teams_in_production[teamName] == TEAMS[teamName], that are in production.
TEAMS_IN_PRODUCTION = {}

# produced[teamName] == list of actors produced so far.
PRODUCED = {}

def QueueProduction(teamName):
    TEAMS_IN_PRODUCTION[teamName] = TEAMS[teamName]
    PRODUCED[teamName] = []

def CheckLiveness(produced, checkList):
    '''
    Remove dead ones in produced list.
    '''
    result = {}
    for teamName, actors in produced.items():
        alive = []
        for a in actors:
            if not a.IsDead:
                alive.append(a)
                checkList[teamName][a.Type] -= 1
        result[teamName] = alive
    return result

def CanBeBuiltInParallel(teams_in_production, teamName):
    '''
    Awww too complex, with C&C's mult-factory in mind.
    Relatively easier with classic production queue but damn...
    This is a TODO.
    '''

    # Already in production.
    if teams_in_production[teamName] != None:
        return False

    # Setting the value to nil is the standard way to delete an entry of Lua table.
    cnt = 0
    for _, val in teams_in_production.items():
        if val != None:
            cnt += 1

    return cnt <= 2

def MakeCheckList(teams_in_production):
    '''
    Create a "histogram" so that we can subtract what is built and
    able to see how many more units to build.
    '''
    checkList = {}
    for teamName, team in teams_in_production.items():
        if team != None:
            checkList[teamName] = {}
            names = team["units"]
            for i, name in enumerate(names):
                checkList[teamName][name] = team["cnts"][i]

    '''
    for tn, cl in checkList.items():
        Media.DisplayMessage("MakeCL: " + tn)
        for typ, cnt in cl.items():
            Media.DisplayMessage("MakeCL:   " + typ)
            Media.DisplayMessage("MakeCL:   " + cnt)
    '''

    return checkList

def IsRecruitable(a):
    if not a.IsIdle or a.IsDead:
        return False
    if a.HackyAIOccupied:
        return False
    if BELONGS_TO_A_TEAM[a.ActorID] == True:
        return False
    return True

def Recruit(produced, checkList):
    '''
    Go through the check list and see if we can recruit anyone.
    INOUT: produced
    INOUT: checkList
    '''
    for teamName, population in checkList.items():
        for name, _ in population.items():
            actors = PLAYER.GetActorsByType(name)
            for a in actors:
                if IsRecruitable(a):
                    if population[name] == 0:
                        break
                    # Idle and not some other team. Recruit this guy.
                    #Media.DisplayMessage("Recruiting:" + a.UID)
                    produced[teamName].append(a)
                    a.HackyAIOccupied = True
                    population[name] -= 1

def CheckBuilt(checkList):
    '''
    Check produced list and return teamNames of the ones that are done.
    INOUT: checkList. After checking, we have what we need to build more by
           subtracting the number of this we have right now.
    '''
    complete = []
    for teamName, population in checkList.items():
        if Utils.All(population, lambda p: p == 0):
            complete.append(teamName)
    return complete

def ReleaseTeams(teamNames, disband):
    for teamName in teamNames:
        TEAMS_IN_PRODUCTION[teamName] = None
        actors = PRODUCED[teamName]

        if not disband:
            for a in actors:
                BELONGS_TO_A_TEAM[a.ActorID] = True

        # Run the functions on the actors.
        func = TEAMS[teamName]['trigger']
        if not disband and func != None:
            func(actors)
        else:
            # Let these be used freely by hacky AI.
            UTIL_SetOccupied(actors, False)

        PRODUCED[teamName] = None

def BuildFromCheckList(checkList):
    '''
    Go through the check list. Build anything it first sees.
    '''
    teamName = None
    def JoinTeam(actors):
        UTIL_SetOccupied(actors, True)
        for a in actors:
            PRODUCED[teamName].append(a)

    for tn, population in checkList.items():
        for name, cnt in population.items():
            if cnt > 0 and not PLAYER.IsProducing(name):
                teamName = tn
                return PLAYER.Build([name], JoinTeam)
    # All done so not an assertion error.
    #Media.DisplayMessage("BuildFromCheckList: Assertion failed haha")
    #return False

def RemoveNil(teams_in_production):
    result = {}

    for teamName, team in teams_in_production.items():
        if team != None:
            result[teamName] = team

    return result

def HasAllPrerequisites(types):
    for ty in types:
        if not PLAYER.HasPrerequisitesForActorType(ty):
            return False
    return True

def RemoveUnableToBuild(teams_in_production):
    result = {}

    for teamName, team in teams_in_production.items():
        if HasAllPrerequisites(team["units"]):
            result[teamName] = team
        else:
            # Disband these guys.
            ReleaseTeams([teamName], True)

    return result

def UTIL_BuildTeam(teamName):
    '''
    Alright, this will be very difficult.
    Even if we get teamName to produce,
    we ignore it and continue what we were doing if it can't be done in parallel.
    We do need this function to be called from time to time otherwise
    production will not work.
    That's because we need to prerequisites check from time to time.

    Generally I'm assuming teams aren't BIG. < 20 members per team.
    Otherwise these will run slowly :)
    '''

    if not HasAllPrerequisites(TEAMS[teamName]["units"]):
        return False

    TEAMS_IN_PRODUCTION = RemoveUnableToBuild(TEAMS_IN_PRODUCTION)
    TEAMS_IN_PRODUCTION = RemoveNil(TEAMS_IN_PRODUCTION)

    if CanBeBuiltInParallel(TEAMS_IN_PRODUCTION, teamName):
        QueueProduction(teamName)
        #Media.DisplayMessage("Build start: " + teamName)

    # checkList[teamName] = xxx
    # xxx[actorType] == count of actorType, to completely build a taskforce of the team.
    # e.g., to build a TF = [e1 e1 e3 e3 e3], then
    # xxx = {e1: 2, e3: 3}.
    checkList = MakeCheckList(TEAMS_IN_PRODUCTION)
    PRODUCED = CheckLiveness(PRODUCED, checkList)
    Recruit(PRODUCED, checkList)

    '''
    Media.DisplayMessage("--------------------------")
    for tn, actorz in PRODUCED.items():
        Media.DisplayMessage("PRO.teamname: " + tn)
        for actr in actorz:
            Media.DisplayMessage("PRO: " + actr.Type)
    Media.DisplayMessage("            ")
    '''

    # Is any team complete?
    # By now, checkList should have how many unit to build more.
    completeTeams = CheckBuilt(checkList)
    ReleaseTeams(completeTeams, False)

    # Check list has what to build.
    return BuildFromCheckList(checkList)


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
            elif unit.AmmoCount() == unit.MaximumAmmoCount():
                # Mark as recruitable
                unit.HackyAIOccupied = False


def UTIL_RepairUnits():
    if not PLAYER.HasPrerequisites(["fix"]):
        return

    fix = PLAYER.GetActorsByType("fix")[0]

    actors = PLAYER.GetActors()
    for a in actors:
        if FIXABLE[a.Type] == True and a.Health < a.MaxHealth / 10 and not a.HackyAIOccupied:
            a.HackyAIOccupied = True
            a.Stop() # Cancel whatever it was doing
            a.RepairAt(fix)
        elif FIXABLE[a.Type] == True and a.Health >= 0.8 * a.MaxHealth and a.HackyAIOccupied:
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

    if FACTION == "allies":
        BUILD_TICK_FUNC = AlliesBuildUnitTick
    elif FACTION == "soviet":
        BUILD_TICK_FUNC = SovietBuildUnitTick
    elif FACTION == "mutants":
        BUILD_TICK_FUNC = MutantBuildUnitTick


def Tick():
    '''
    Tick the AI thinking. Called by Tick() in Scripted AI.
    '''

    TICKS += 1
    # Make sure nothing runs at the first tick.
    # (tick == 1)

    # In once a second or so,
    if TICKS % 31 == 0:
        BUILD_TICK_FUNC(FACTION)
    elif TICKS % 37 == 0:
        UTIL_ReloadAircraft(AMMO_POOLED_AIRCRAFTS)
    elif TICKS % 127 == 0:
        UTIL_RepairUnits()
