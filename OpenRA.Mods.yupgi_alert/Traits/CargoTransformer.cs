#region Copyright & License Information
/*
 * Modded by Boolbada of Over Powered Mod.
 * Contains some copy and paste code from OpenRA base mod.
 * (Erm... hardly any by now but using OpenRA API ofcourse)
 * 
 * Copyright 2007-2017 The OpenRA Developers (see AUTHORS)
 * This file is part of OpenRA, which is free software. It is made
 * available to you under the terms of the GNU General Public License
 * as published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version. For more
 * information, see COPYING.
 */
#endregion

using System.Collections.Generic;
using System.Linq;
using OpenRA.Traits;
using OpenRA.Mods.Common.Traits;

namespace OpenRA.Mods.yupgi_alert.Traits
{
	[Desc("Transforms cargo inside when some predefined combination is met.")]
	public class CargoTransformerInfo : ITraitInfo, Requires<CargoInfo>, Requires<ProductionInfo>
	{
		//[FieldLoader.LoadUsing("LoadSpeeds", true)]
		[Desc("Unit type to emit when the combination is met")]
		public readonly Dictionary<string, string[]> Combinations;

		public object Create(ActorInitializer init) { return new CargoTransformer(init.Self, this); }
	}

	public class CargoTransformer : INotifyPassengerEntered
	{
		public readonly CargoTransformerInfo Info;
		Cargo Cargo;

		public CargoTransformer(Actor self, CargoTransformerInfo info)
		{
			Info = info;
			Cargo = self.Trait<Cargo>(); // I required CargoInfo so this will always work.
		}

		void SpawnUnit(Actor self, string unit)
		{
			// Kill cargo and spawn new unit

			// For dramatic cargo, lets have those ejected and killed!
			// From chrono kill cargo haha.
			while (!Cargo.IsEmpty(self))
			{
				var a = Cargo.Unload(self);
				// Kill all the units that are unloaded into the void
				// Kill() handles kill and death statistics
				a.Kill(self);
			}

			// Now lets "produce" new unit given by name.
			var pd = self.Trait<Production>();
			var ai = self.World.Map.Rules.Actors[unit];
			var faction = self.Owner.Faction.InternalName;
			pd.Produce(self, ai, faction);
		}

		void INotifyPassengerEntered.OnPassengerEntered(Actor self, Actor passenger)
		{
			// get rules entry name for each passenger.
			var names = Cargo.Passengers.Select(x => x.Info.Name).ToArray();

			// Lets examine the contents.
			foreach(var kv in Info.Combinations)
			{
				if (Enumerable.SequenceEqual(names, kv.Value))
				{
					SpawnUnit(self, kv.Key);
					return; // no need to examine any other combination.
				}
			}
		}
	}
}