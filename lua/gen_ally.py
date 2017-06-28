#!/usr/bin/python3
import random
import pprint

SERIAL = 0
PREFIX = "ally"
FACTION = "allies"

def make_combis(teams, cnt, pool, action_pool):
    global SERIAL
    global PREFIX

    for i in range(cnt):
        team_name = "{}{:03d}".format(PREFIX, SERIAL)
        SERIAL += 1
        team = make_combi(pool, action_pool)
        teams[team_name] = team

def make_combi(pool, action_pool):
    trigger = None
    if random.choice([False, True]) == True:
        trigger = random.choice(action_pool)
        
    team = {}
    team["faction"] = FACTION
    team["units"] = pick_units(pool)
    team["cnts"] = pick_counts(team["units"])
    team["trigger"] = trigger
    return team

def pick_units(pool):
    u1 = random.choice(pool)
    u2 = random.choice(pool)
    if u1 == u2:
        return [u1]
    else:
        return [u1, u2]

def pick_counts(units):
    return [random.randint(1, 8) for i in range(len(units))]

def make_trans(teams, cnt, pool, action_pool):
    global SERIAL
    global PREFIX

    for i in range(cnt):
        team_name = "{}{:03d}".format(PREFIX, SERIAL)
        SERIAL += 1
        team = make_tran(pool, action_pool)
        teams[team_name] = team

def make_tran(pool, action_pool):
    pool = random.choice(pool)

    trigger = None
    if random.choice([False, True]) == True:
        trigger = random.choice(action_pool)
        trigger = trigger.replace("ACT_", "ACT_Load")

    transport, cap, passengers = pool
    tran_cnt = random.randint(1, 4)
    cap = cap * tran_cnt
    passengers = pick_units(passengers)
    if len(passengers) == 2:
        p1_cnt = random.randint(1, cap-1)
        p2_cnt = random.randint(1, cap - p1_cnt)
        cnts = [tran_cnt, p1_cnt, p2_cnt]
    else:
        p1_cnt = random.randint(1, cap)
        cnts = [tran_cnt, p1_cnt]
        
    team = {}
    team["faction"] = FACTION
    team["units"] = [transport] + passengers
    team["cnts"] = cnts
    team["trigger"] = trigger
    return team

def make_hero(teams, cnt, pool, action_pool):
    global SERIAL
    global PREFIX

    for i in range(cnt):
        team_name = "{}{:03d}".format(PREFIX, SERIAL)
        SERIAL += 1

        unit = random.choice(pool)
        team = make_combi([unit], action_pool)
        team["cnts"] = [1]
        teams[team_name] = team



###
### main
###

actions = ["ACT_AttackPower", "ACT_AttackRef", "ACT_AttackFactory", "ACT_AttackBarracks", "ACT_AttackCY", "ACT_Hunt", "ACT_AttackStaticDefenses", "ACT_AttackHarv"]
# None is queued by 50%, not listed here.

airs = ['hind', 'heli']

heros = ['e7']

transports = [
    ('tran', 6, ['e1', 'e3']),
    ('jeep', 3, ['e1', 'e3'])
]

grounds = [
    'jeep', '1tnk', 'arty', 'msam',
    '2tnk', 'stnk', 'wangchang', 'e1', 'e3'
]

teams = {}
make_combis(teams, 12, airs, actions)
make_combis(teams, 48, grounds, actions)
make_trans(teams, 12, transports, actions)

# make hero is almost useless and duplicate but
# this determines the frequency of heros being built.
make_hero(teams, 12, heros, actions)

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(teams)

keys = list(teams.keys())
keys.sort()

for tn in keys:
    team = teams[tn]
    print("    '{}': ".format(tn) + "{")
    print("        'faction': '{}',".format(team["faction"]))
    print("        'units': {},".format(str(team["units"])))
    print("        'cnts': {},".format(str(team["cnts"])))
    print("        'trigger': {},".format(team["trigger"]))

    if tn == keys[-1]:
        print("    }")
    else:
        print("    },")
