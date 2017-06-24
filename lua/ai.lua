FACTION = nil
PLAYER_NAME = nil
PLAYER = nil
BUILD_ORDER = nil
TICKS = 0
AUTO_BUILD = false
ANYPOWER = 'ANYPOWER'
MCVS = {'gamcv', 'namcv', 'qant'}
COUNT_BUILDING_AS_MCV = { gafact='gamcv', nafact='namcv', qnest='qant', }
AMMO_POOLED_AIRCRAFTS = {'nmig', 'mig', 'yak', 'hind', 'heli'}
STATIC_DEFENSES = {'pbox', 'hbox', 'gun', 'ftur', 'tsla'}
BO_ALLIES_NORMAL = { name='allies_normal', bo={ANYPOWER, 'tent', 'proc', 'proc', ANYPOWER, 'gaweap', 'fix', 'dome', ANYPOWER, 'proc', 'hpad', 'hpad', 'atek', ANYPOWER}, }
BO_ALLIES_FAST_WEAP = { name='allies_weap', bo={ANYPOWER, 'tent', 'proc', 'gaweap', ANYPOWER, 'proc', 'fix', 'proc', 'dome', ANYPOWER, 'atek', ANYPOWER}, }
BO_ALLIES_FAST_AIR = { name='allies_air', bo={ANYPOWER, 'tent', 'proc', 'proc', 'dome', 'hpad', ANYPOWER, 'proc', 'gaweap', 'atek', ANYPOWER, 'hpad', 'hpad', 'hpad', 'proc', 'fix'}, }
BO_ALLIES_ECO = { name='allies_eco', bo={ANYPOWER, 'tent', 'proc', 'proc', ANYPOWER, 'proc', 'gaweap', 'fix', ANYPOWER, 'dome', ANYPOWER, 'atek'}, }
BO_ALLIES_BOS = {BO_ALLIES_NORMAL, BO_ALLIES_ECO, BO_ALLIES_FAST_WEAP, BO_ALLIES_FAST_AIR}
BO_SOVIET_NORMAL = { name='soviet_normal', bo={ANYPOWER, 'barr', 'kenn', 'proc', 'proc', ANYPOWER, 'naweap', 'fix', 'dome', ANYPOWER, 'proc', 'afld', 'afld', 'stek', ANYPOWER}, }
BO_SOVIET_FAST_WEAP = { name='soviet_weap', bo={ANYPOWER, 'kenn', 'proc', 'naweap', ANYPOWER, 'barr', 'proc', 'fix', 'proc', 'dome', ANYPOWER, 'stek', ANYPOWER}, }
BO_SOVIET_FAST_AIR = { name='soviet_air', bo={ANYPOWER, 'barr', 'proc', 'proc', 'dome', 'afld', ANYPOWER, 'proc', 'naweap', 'stek', ANYPOWER, 'afld', 'afld', 'afld', 'fix'}, }
BO_SOVIET_ECO = { name='soviet_eco', bo={ANYPOWER, 'kenn', 'barr', 'proc', 'proc', ANYPOWER, 'proc', 'naweap', 'fix', ANYPOWER, 'dome', ANYPOWER, 'stek'}, }
BO_SOVIET_BOS = {BO_SOVIET_NORMAL, BO_SOVIET_ECO, BO_SOVIET_FAST_WEAP, BO_SOVIET_FAST_AIR}
BO_MUTANT_NORMAL = { name='mutant_normal', bo={'qant', 'anthill', 'anthill', 'qant', 'tibtree', 'vein', 'qant', 'tibtree', 'anthill', 'evo'}, }
BO_MUTANT_BOS = {BO_MUTANT_NORMAL}
TASKFORCES = { ['6_heli']={ units={'heli', 'heli', 'heli', 'heli'}, queues={'air'}, }, ['2_hind']={ units={'hind', 'hind'}, queues={'air'}, }, ['5_e1']={ units={'e1', 'e1', 'e1', 'e1', 'e1'}, queues={'inf'}, }, ['2_e3']={ units={'e3', 'e3'}, queues={'inf'}, }, ['2_jeep']={ units={'jeep', 'jeep'}, queues={'weap'}, }, ['4_1tnk']={ units={'1tnk', '1tnk', '1tnk', '1tnk'}, queues={'weap'}, }, ['4_2tnk']={ units={'2tnk', '2tnk', '2tnk', '2tnk'}, queues={'weap'}, }, arty={ units={'arty', 'arty', '2tnk', '2tnk'}, queues={'weap'}, }, humvee={ units={'jeep', 'e1', 'e3', 'e3'}, queues={'weap', 'inf'}, }, ['2_e2']={ units={'e2', 'e2'}, queues={'inf'}, }, ['4_dog']={ units={'dog', 'dog', 'dog', 'dog'}, queues={'inf'}, }, ['2_e4']={ units={'e4', 'e4'}, queues={'inf'}, }, ['2_shok']={ units={'shok', 'shok'}, queues={'inf'}, }, ['2_ftrk']={ units={'ftrk', 'ftrk'}, queues={'weap'}, }, ['4_3tnk']={ units={'3tnk', '3tnk', '3tnk', '3tnk'}, queues={'weap'}, }, ['2_4tnk']={ units={'4tnk', '4tnk'}, queues={'weap'}, }, ttnk={ units={'ttnk'}, queues={'weap'}, }, v2rl={ units={'v2rl', 'v2rl', '3tnk', '3tnk'}, queues={'weap'}, }, ['4_mig']={ units={'mig', 'mig', 'mig', 'mig'}, queues={'air'}, }, ['2_yak']={ units={'yak', 'yak'}, queues={'air'}, }, ['2_want']={ units={'want', 'want'}, queues={'weap'}, }, ['2_fant']={ units={'fant', 'fant'}, queues={'weap'}, }, ['1_sant']={ units={'sant'}, queues={'weap'}, }, ['1_hant']={ units={'hant'}, queues={'weap'}, }, ['1_inft']={ units={'inft'}, queues={'inf'}, }, ['3_doggie']={ units={'doggie', 'doggie', 'doggie'}, queues={'inf'}, }, }
TEAMS = { ['6_heli']={ faction='allies', tf='6_heli', trigger=nil, }, ['2_hind']={ faction='allies', tf='2_hind', trigger=nil, }, ['5_e1']={ faction='allies', tf='5_e1', trigger=nil, }, ['2_e3']={ faction='allies', tf='2_e3', trigger=nil, }, ['2_jeep']={ faction='allies', tf='2_jeep', trigger=nil, }, ['4_1tnk']={ faction='allies', tf='4_1tnk', trigger=nil, }, ['4_2tnk']={ faction='allies', tf='4_2tnk', trigger=nil, }, arty={ faction='allies', tf='arty', trigger=nil, }, humvee={ faction='allies', tf='humvee', trigger=nil, }, ['2_e2']={ faction='soviet', tf='2_e2', queue='inf', trigger=nil, }, ['4_dog']={ faction='soviet', tf='4_dog', trigger=nil, }, ['2_e4']={ faction='soviet', tf='2_e4', trigger=nil, }, ['2_shok']={ faction='soviet', tf='2_shok', trigger=nil, }, ['2_ftrk']={ faction='soviet', tf='2_ftrk', trigger=nil, }, ['4_3tnk']={ faction='soviet', tf='4_3tnk', trigger=nil, }, ['2_4tnk']={ faction='soviet', tf='2_4tnk', trigger=nil, }, ttnk={ faction='soviet', tf='ttnk', trigger=nil, }, v2rl={ faction='soviet', tf='v2rl', trigger=nil, }, ['4_mig']={ faction='soviet', tf='4_mig', trigger=nil, }, ['2_yak']={ faction='soviet', tf='2_yak', trigger=nil, }, ['1_zep']={ faction='soviet', tf='1_zep', trigger=nil, }, ['2_want']={ faction='mutants', tf='2_want', trigger=nil, }, ['2_fant']={ faction='mutants', tf='2_fant', trigger=nil, }, ['1_sant']={ faction='mutants', tf='1_sant', trigger=nil, }, ['1_hant']={ faction='mutants', tf='1_hant', trigger=nil, }, ['1_inft']={ faction='mutants', tf='1_inft', trigger=nil, }, ['3_doggie']={ faction='mutants', tf='3_doggie', trigger=nil, }, }
ALLIES_TEAMS_KEYS = {}
for key, team in pairs(TEAMS) do
  if team['faction']=='allies' then
    table.insert(ALLIES_TEAMS_KEYS, key)
  end
end
SOVIET_TEAMS_KEYS = {}
for key, team in pairs(TEAMS) do
  if team['faction']=='soviet' then
    table.insert(SOVIET_TEAMS_KEYS, key)
  end
end
MUTANT_TEAMS_KEYS = {}
for key, team in pairs(TEAMS) do
  if team['faction']=='mutants' then
    table.insert(MUTANT_TEAMS_KEYS, key)
  end
end

IsAnypower = function(name)
  if name=='powr' then
    return true
  elseif name=='apwr' then
    return true
  end
  return false
end

ChooseBuildOrder = function(faction)
  -- 
  --     Given faction, choose a build order.
  --     Currently, random.
  --     
  if faction=='soviet' then
    return Utils.Random(BO_SOVIET_BOS)
  elseif faction=='allies' then
    return Utils.Random(BO_ALLIES_BOS)
  elseif faction=='mutants' then
    return Utils.Random(BO_MUTANT_BOS)
  else
    return nil
  end
end

NeedToRebuildMCV = function(faction)
  if faction=='allies' then
    return UTIL_Count('gamcv')==0 and UTIL_Count('gafact')==0
  end
  if faction=='soviet' then
    return UTIL_Count('namcv')==0 and UTIL_Count('nafact')==0
  end
  return false
end

CanRebuildMCV = function(faction)
  if faction=='allies' then
    return PLAYER.HasPrerequisites({'gaweap'})
  end
  if faction=='soviet' then
    return PLAYER.HasPrerequisites({'naweap'})
  end
  if faction=='mutants' then
    return PLAYER.HasPrerequisites({'qnest'})
  end
  Media.DisplayMessage('CanRebuildMCV() has reached invalid execution path')
  return false
end

AlliesBuildUnitTick = function(faction)
  local harvs = PLAYER.GetActorsByType('harv')
  if  not AUTO_BUILD then
    local e1s = PLAYER.GetActorsByType('e1')
    if #e1s<10 and PLAYER.HasPrerequisites({'tent'}) then
      PLAYER.Build({'e1'}, nil)
    end
    if #harvs<3 and PLAYER.HasPrerequisites({'gaweap', 'proc'}) then
      PLAYER.Build({'harv'}, nil)
    end
    if #harvs>=3 and #e1s>=10 then
      AUTO_BUILD = true
    end
  else
    local occupied = { }
    if #harvs<1 and PLAYER.HasPrerequisites({'gaweap', 'proc'}) then
      PLAYER.Build({'harv'}, nil)
      return 
    end
    if NeedToRebuildMCV(faction) and CanRebuildMCV(faction) then
      PLAYER.Build({'gamcv'}, nil)
      return 
    end
    if #harvs<3 and PLAYER.HasPrerequisites({'gaweap', 'proc'}) then
      PLAYER.Build({'harv'}, nil)
      return 
    end
    if #harvs<5 and PLAYER.HasPrerequisites({'gaweap', 'proc', 'fix'}) then
      PLAYER.Build({'harv'}, nil)
    elseif #harvs<7 and PLAYER.HasPrerequisites({'gaweap', 'proc', 'atek'}) then
      PLAYER.Build({'harv'}, nil)
    elseif UTIL_Count('marv')<2 and PLAYER.HasPrerequisites({'gaweap', 'proc', 'atek'}) then
      PLAYER.Build({'marv'}, nil)
    end
    local enemy = UTIL_GetAnEnemyPlayer()
    local defense_cnt = UTIL_CountUnits(enemy, STATIC_DEFENSES)
    if defense_cnt>=4 then
      if UTIL_Count('msam')<2 and PLAYER.HasPrerequisites({'gaweap', 'atek'}) then
        PLAYER.Build({'msam'}, nil)
        occupied['weap'] = true
      end
      if UTIL_Count('arty')<4 and PLAYER.HasPrerequisites({'gaweap', 'dome'}) then
        PLAYER.Build({'arty'}, nil)
        occupied['weap'] = true
      end
    end
    local success
    success, occupied = unpack(UTIL_BuildRandomTeam(ALLIES_TEAMS_KEYS, occupied))
    success, occupied = unpack(UTIL_BuildRandomTeam(ALLIES_TEAMS_KEYS, occupied))
  end
end

BuildUnitTick = function(faction)
  if faction=='allies' then
    AlliesBuildUnitTick(faction)
  elseif faction=='soviets' then
    SovietBuildUnitTick(faction)
  elseif faction=='mutants' then
    MutantBuildUnitTick(faction)
  end
end

CanQueue = function(tf, occupied)
  for _, queue in ipairs(tf['queues']) do
    if occupied[queue] ~= nil then
      return false
    end
  end
  return true
end

UTIL_BuildRandomTeam = function(keys, occupied)
  -- 
  --     Given teams, and its keys, build a random team and return success/fail
  --     occupied: currently occupied queue
  --     
  local avail = {}
  for _, key in ipairs(keys) do
    local tf = TASKFORCES[TEAMS[key]['tf']]
    if CanQueue(tf, occupied) then
      table.insert(avail, key)
    end
  end
  if #avail==0 then
    return {false, occupied}
  end
  local key = Utils.Random(avail)
  return UTIL_BuildTeam(key, occupied)
end

UTIL_BuildTeam = function(key, occupied)
  local team = TEAMS[key]
  local taskforce = TASKFORCES[team['tf']]
  for _, queue in ipairs(taskforce['queues']) do
    occupied[queue] = true
  end
  return {PLAYER.Build(taskforce['units'], team['trigger']), occupied}
end

UTIL_CountBuildings = function(stuff)
  -- 
  --     Given a list of things that AI has, count it.
  --     
  local cnts = { }
  for _, name in ipairs(MCVS) do
    local actors = PLAYER.GetActorsByType(name)
    cnts[name] = #actors
  end
  for _, v in ipairs(stuff) do
    if IsAnypower(v) then
      v = ANYPOWER
    elseif COUNT_BUILDING_AS_MCV[v] ~= nil then
      v = COUNT_BUILDING_AS_MCV[v]
    end
    if cnts[v] == nil then
      cnts[v] = 1
    else
      cnts[v] = cnts[v]+1
    end
  end
  return cnts
end

UTIL_GetUnbuilt = function(build_order, building_count)
  -- 
  --     Examine what we have and the build order to see if anything is missing.
  --     If multiple things are missing, return the one that
  --     occurs early in build_order.
  --     Returns None when everything in BO is built.
  --     
  local cnts = { }
  for _, name in ipairs(build_order) do
    if building_count[name] == nil then
      return name
    else
      if cnts[name] == nil then
        cnts[name] = 1
      else
        cnts[name] = cnts[name]+1
      end
      if building_count[name]<cnts[name] then
        return name
      end
    end
  end
  return nil
end

UTIL_Count = function(name)
  -- 
  --     Given one actor type, count the number of it, owned by AI.
  --     Special case of UTIL_CountUnits but occurs very often so made a function.
  --     
  return #(PLAYER.GetActorsByType(name))
end

UTIL_CountUnits = function(p, unit_types)
  -- 
  --     Count unit types, owned by player
  --     Not histogram like UTIL_hist.
  --     Just count them and return integer.
  --     
  local cnt = 0
  for _, name in ipairs(unit_types) do
    local units = p.GetActorsByType(name)
    if units~=nil then
      cnt = cnt+#units
    end
  end
  return cnt
end

UTIL_IsEnemyWithAI = function(p)
  if p.InternalName=='Neutral' then
    return false
  end
  if p.InternalName=='Creeps' then
    return false
  end
  if p.InternalName=='Everyone' then
    return false
  end
  if p.InternalName==PLAYER.InternalName then
    return false
  end
  if p.IsAlliedWith(PLAYER) then
    return false
  end
  return true
end

UTIL_GetAnEnemyPlayer = function()
  -- 
  --     Currently we choose an enemy player by random.
  --     We may introduce policies in the future.
  --     
  local enemies = {}
  for _, p in ipairs(Player.GetPlayers(nil)) do
    if UTIL_IsEnemyWithAI(p) then
      table.insert(enemies, p)
    end
  end
  if #enemies==0 then
    return nil
  end
  return Utils.Random(enemies)
end

UTIL_ReloadAircraft = function(ammo_pooled_aircrafts)
  for _, name in ipairs(ammo_pooled_aircrafts) do
    local units = PLAYER.GetActorsByType(name)
    for _, unit in ipairs(units) do
      if unit.AmmoCount()==0 and  not unit.HackyAIOccupied then
        unit.HackyAIOccupied = true
      elseif unit.AmmoCount()==unit.MaximumAmmoCount() and unit.Health==unit.MaxHealth and unit.HackyAIOccupied then
        unit.HackyAIOccupied = false
      end
    end
  end
end
HACKY_FALLBACK = 'hacky_fallback'

BB_choose_building_to_build = function(tab)
  -- 
  --     Called by ChooseBuildingToBuild in BaseBuilder.cs
  --     Thinking process exported to Lua.
  --     Input: tab: table containing all the parameters from BaseBuilder.cs
  --     Returns: a rules name of structures to build.
  --     Modders may return nil on purpose to choose not to build anything.
  --     
  if BUILD_ORDER==nil then
    Media.DisplayMessage('No build order for ' .. FACTION, 'BB Warning')
    return HACKY_FALLBACK
  end
  local tab = tab[1]
  local building_count = UTIL_CountBuildings(tab['player_buildings'])
  if tab['queue_type']=='defense' then
    return HACKY_FALLBACK
  end
  if FACTION~='mutants' and tab['excess_power']<tab['minimum_excess_power'] then
    if tab['power_gen']>0 then
      return tab['power']
    end
  end
  local unbuilt = UTIL_GetUnbuilt(BUILD_ORDER['bo'], building_count)
  if unbuilt==nil then
    return HACKY_FALLBACK
  elseif unbuilt==ANYPOWER then
    return tab['power']
  end
  return unbuilt
end

ActivateAI = function(params)
  -- 
  --     Initialize stuff. Called by Activate() in HackyAI.
  --     
  FACTION = string.lower(params[1])
  PLAYER_NAME = params[2]
  PLAYER = Player.GetPlayer(PLAYER_NAME)
  BUILD_ORDER = ChooseBuildOrder(FACTION)
end

Tick = function()
  -- 
  --     Tick the AI thinking. Called by Tick() in Scripted AI.
  --     
  TICKS = TICKS+1
  if (TICKS % 31)==0 then
    BuildUnitTick(FACTION)
  elseif (TICKS % 37)==0 then
    UTIL_ReloadAircraft(AMMO_POOLED_AIRCRAFTS)
  end
end
