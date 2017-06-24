FACTION = nil
PLAYER_NAME = nil
PLAYER = nil
BUILD_ORDER = nil
ANYPOWER = 'ANYPOWER'
BO_ALLIES_NORMAL = { name='allies_normal', bo={ANYPOWER, 'tent', 'proc', 'proc', ANYPOWER, 'gaweap', 'fix', 'dome', ANYPOWER, 'proc', 'hpad', 'hpad', 'atek', ANYPOWER}, }
BO_ALLIES_FAST_WEAP = { name='allies_weap', bo={ANYPOWER, 'tent', 'proc', 'naweap', ANYPOWER, 'proc', 'fix', 'proc', 'dome', ANYPOWER, 'atek', ANYPOWER}, }
BO_ALLIES_FAST_AIR = { name='allies_air', bo={ANYPOWER, 'tent', 'proc', 'proc', 'dome', 'hpad', ANYPOWER, 'proc', 'gaweap', 'atek', ANYPOWER, 'hpad', 'hpad', 'hpad', 'proc', 'fix'}, }
BO_ALLIES_ECO = { name='allies_eco', bo={ANYPOWER, 'tent', 'proc', 'proc', ANYPOWER, 'proc', 'gaweap', 'fix', ANYPOWER, 'dome', ANYPOWER, 'atek'}, }
BO_ALLIES_BOS = {BO_ALLIES_NORMAL, BO_ALLIES_ECO, BO_ALLIES_FAST_WEAP, BO_ALLIES_FAST_AIR}
BO_SOVIET_NORMAL = { name='soviet_normal', bo={ANYPOWER, 'barr', 'kenn', 'proc', 'proc', ANYPOWER, 'naweap', 'fix', 'dome', ANYPOWER, 'proc', 'afld', 'afld', 'stek', ANYPOWER}, }
BO_SOVIET_FAST_WEAP = { name='soviet_weap', bo={ANYPOWER, 'kenn', 'proc', 'naweap', ANYPOWER, 'barr', 'proc', 'fix', 'proc', 'dome', ANYPOWER, 'stek', ANYPOWER}, }
BO_SOVIET_FAST_AIR = { name='soviet_air', bo={ANYPOWER, 'barr', 'proc', 'proc', 'dome', 'afld', ANYPOWER, 'proc', 'naweap', 'stek', ANYPOWER, 'afld', 'afld', 'afld', 'fix'}, }
BO_SOVIET_ECO = { name='soviet_eco', bo={ANYPOWER, 'kenn', 'barr', 'proc', 'proc', ANYPOWER, 'proc', 'naweap', 'fix', ANYPOWER, 'dome', ANYPOWER, 'stek'}, }
BO_SOVIET_BOS = {BO_SOVIET_NORMAL, BO_SOVIET_ECO, BO_SOVIET_FAST_WEAP, BO_SOVIET_FAST_AIR}
BO_MUTANT_NORMAL = { name='mutant_normal', bo={'qnest', 'anthill', 'anthill', 'qnest', 'tibtree', 'vein', 'qnest', 'tibtree', 'anthill', 'evo'}, }
BO_MUTANT_BOS = {BO_MUTANT_NORMAL}

MOD_is_anypower = function(name)
  if name=='powr' then
    return true
  elseif name=='apwr' then
    return true
  end
  return false
end

UTIL_hist = function(stuff)
  -- 
  --     Given a list of things that AI has, count it.
  --     
  local cnts = { }
  for _, v in ipairs(stuff) do
    if MOD_is_anypower(v) then
      v = ANYPOWER
    end
    if cnts[v] == nil then
      cnts[v] = 1
    else
      cnts[v] = cnts[v]+1
    end
  end
  return cnts
end

UTIL_get_unbuilt = function(build_order, building_count)
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

chooseBuildOrder = function(faction)
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
  local building_count = UTIL_hist(tab['player_buildings'])
  if tab['queue_type']=='defense' then
    return HACKY_FALLBACK
  end
  if FACTION~='mutants' and tab['excess_power']<tab['minimum_excess_power'] then
    if tab['power_gen']>0 then
      return tab['power']
    end
  end
  local unbuilt = UTIL_get_unbuilt(BUILD_ORDER['bo'], building_count)
  Media.DisplayMessage('Unbuilt: ' .. unbuilt, 'BB Warning')
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
  BUILD_ORDER = chooseBuildOrder(FACTION)
end

Tick = function()
  -- 
  --     Tick the AI thinking. Called by Tick() in Scripted AI.
  --     
end
