ticks = 0
facing = 0

Tick = function()
	-- 4 x 4 grid.
	-- 10, 14 -- 38, 14
	-- 14, 14 -- ...
	-- 10, 18 -- ...
	
	if ticks % 50 == 0 then
		name = "Actor" .. 0
		Media.DisplayMessage("facing: " .. facing)
		a = Map.NamedActor(name)
		Camera.Position = a.CenterPosition
		a.Turn(facing)

		facing = (facing + 8) % 256
	end

	ticks = ticks + 1
end
