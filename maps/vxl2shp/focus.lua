ticks = 0

i = 0

Tick = function()
	-- 4 x 4 grid.
	-- 10, 14 -- 38, 14
	-- 14, 14 -- ...
	-- 10, 18 -- ...
	
	if ticks % 50 == 0 then
		name = "Actor" .. i
		Media.DisplayMessage(name)
		Camera.Position = Map.NamedActor(name).CenterPosition
		i = i + 1
	end

	ticks = ticks + 1
end
