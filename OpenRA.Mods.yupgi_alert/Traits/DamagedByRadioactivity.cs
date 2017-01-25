#region Copyright & License Information
/*
 * Copyright 2007-2016 The OpenRA Developers (see AUTHORS)
 * This file is part of OpenRA, which is free software. It is made
 * available to you under the terms of the GNU General Public License
 * as published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version. For more
 * information, see COPYING.
 */
#endregion

using System.Collections.Generic;
using System.Linq;
using OpenRA.GameRules;
using OpenRA.Traits;
using OpenRA.Mods.Common.Traits;

namespace OpenRA.Mods.yupgi_alert.Traits
{
	[Desc("This actor receives damage from the given weapon when in radioactive area.")]
	class DamagedByRadioactivityInfo : UpgradableTraitInfo, Requires<HealthInfo>
	{
		[Desc("Related to amount of damage received per DamageInterval ticks. (Damage = DamageCoeff * RadioactivityLevel")]
		[FieldLoader.Require] public readonly float DamageCoeff = 0.0f;

		[Desc("Delay between receiving damage.")]
		public readonly int DamageInterval = 16;

		[Desc("Apply the damage using these damagetypes.")]
		public readonly HashSet<string> DamageTypes = new HashSet<string>();

		public override object Create(ActorInitializer init) { return new DamagedByRadioactivity(init.Self, this); }
	}

	class DamagedByRadioactivity : UpgradableTrait<DamagedByRadioactivityInfo>, ITick, ISync
	{
		readonly Health health;
		readonly RadioactivityLayer raLayer;

		[Sync] int damageTicks;

		public DamagedByRadioactivity(Actor self, DamagedByRadioactivityInfo info) : base(info)
		{
			health = self.Trait<Health>();
			raLayer = self.World.WorldActor.Trait<RadioactivityLayer>();
		}

		public void Tick(Actor self)
		{
			if (IsTraitDisabled || --damageTicks > 0)
				return;

			// Prevents harming cargo.
			if (!self.IsInWorld)
				return;

			var level = raLayer.GetLevel(self.Location);
			if (level <= 0)
				return;

			float dmg = Info.DamageCoeff * level;
			if (dmg < 1.0f)
				dmg = 1.0f; // cos we will be rounding this as int.

			self.InflictDamage(self.World.WorldActor, new Damage((int) dmg, Info.DamageTypes));
			damageTicks = Info.DamageInterval;
		}
	}
}
