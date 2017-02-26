#region Copyright & License Information
/*
 * Modded by Boolbada of OP mod, from Engineer repair enter activity.
 * 
 * Copyright 2007-2017 The OpenRA Developers (see AUTHORS)
 * This file is part of OpenRA, which is free software. It is made
 * available to you under the terms of the GNU General Public License
 * as published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version. For more
 * information, see COPYING.
 */
#endregion

using OpenRA.Mods.Common.Traits;
using OpenRA.Mods.yupgi_alert.Traits;
using OpenRA.Traits;
using System.Linq;
using System.Collections.Generic;
using System.Drawing;
using OpenRA.Mods.Common.Activities;

namespace OpenRA.Mods.yupgi_alert.Activities
{
	class EnterSpawner : Enter
	{
		readonly Actor target; // remember spawner.
		readonly Spawner spawner;
		readonly AmmoPool[] ammoPools;
		//readonly Dictionary<AmmoPool, int> ammoPoolsReloadTimes;

		public EnterSpawner(Actor self, Actor target, EnterBehaviour enterBehaviour)
			: base(self, target, enterBehaviour)
		{
			this.target = target;
			spawner = target.Trait<Spawner>();

			ammoPools = self.TraitsImplementing<AmmoPool>().Where(p => !p.Info.SelfReloads).ToArray();

			if (ammoPools == null)
				return;

			//ammoPoolsReloadTimes = ammoPools.ToDictionary(x => x, y => y.Info.ReloadDelay);
		}

		protected override bool CanReserve(Actor self)
		{
			return true;
		}

		protected override void OnInside(Actor self)
		{
			if (target.IsDead)
				// entered the nydus canal but the entrance is dead immediately. haha;;
				return;

			Done(self); // no exit shit.

			// Load this thingy.
			// Issue attack move to the rally point.
			self.World.AddFrameEndTask(w =>
			{
				if (self.IsDead || target.IsDead || !spawner.CanLoad(target, self))
					return;

				spawner.Load(target, self);
				w.Remove(self);

				// Insta repair.
				var info = target.Info.TraitInfo<SpawnerInfo>();
				if (info.InstaRepair)
				{
					var health = self.Trait<Health>();
					self.InflictDamage(self, new Damage(-health.MaxHP));
				}

				// Insta re-arm. (Delayed launching is handled at spawner.)
				foreach (var pool in ammoPools)
				{
					while (pool.GiveAmmo()); // fill 'er up.
				}
			});
		}
	}
}
