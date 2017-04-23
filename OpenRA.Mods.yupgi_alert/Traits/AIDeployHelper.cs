#region Copyright & License Information
/*
 * Copyright 2007-2017 The OpenRA Developers (see AUTHORS)
 * This file is part of OpenRA, which is free software. It is made
 * available to you under the terms of the GNU General Public License
 * as published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version. For more
 * information, see COPYING.
 */
#endregion

using System;
using OpenRA.Mods.Common.Traits;
using OpenRA.Traits;

namespace OpenRA.Mods.yupgi_alert.Traits
{
	[Flags]
	public enum DeployTriggers
	{
		None = 0,
		Attack = 1,
		Damage = 2,
		Heal = 4
	}

	[Desc("If this unit is owned by an AI, issue a deploy order automatically.")]
	public class AIDeployHelperInfo : ITraitInfo
	{
		[Desc("Events leading to the actor getting uncloaked. Possible values are: None, Attack, Damage, Heal.")]
		public readonly DeployTriggers DeployTrigger = DeployTriggers.Attack | DeployTriggers.Damage;

		[Desc("Chance of deploying when the trigger activates.")]
		public readonly int DeployChance = 100;

		[Desc("Delay between two successful deploy orders.")]
		public readonly int DeployTicks = 2500;

		[Desc("Delay to wait for the actor to undeploy (if capable to) after a successful deploy.")]
		public readonly int UndeployTicks = 450;

		public object Create(ActorInitializer init) { return new AIDeployHelper(this); }
	}

	public class AIDeployHelper : INotifyAttack, ITick, INotifyDamage, INotifyCreated, ISync
	{
		readonly AIDeployHelperInfo info;

		[Sync] int undeployTicks, deployTicks;
		bool undeployable;

		public AIDeployHelper(AIDeployHelperInfo info)
		{
			this.info = info;
		}

		void INotifyCreated.Created(Actor self)
		{
			undeployable = self.Info.HasTraitInfo<GrantConditionOnDeployInfo>();
		}

		void TryDeploy(Actor self)
		{
			if (deployTicks > 0)
				return;

			if (self.World.SharedRandom.Next(100) > info.DeployChance)
				return;

			self.World.IssueOrder(new Order("DeployTransform", self, false));
			self.World.IssueOrder(new Order("Unload", self, false));
			self.World.IssueOrder(new Order("Detonate", self, false));
			self.World.IssueOrder(new Order("GrantConditionOnDeploy", self, false));

			if (undeployable)
				undeployTicks = info.UndeployTicks;

			deployTicks = info.DeployTicks;
		}

		void Undeploy(Actor self)
		{
			self.World.IssueOrder(new Order("GrantConditionOnDeploy", self, false));
		}

		void INotifyAttack.Attacking(Actor self, Target target, Armament a, Barrel barrel)
		{
			if (!self.Owner.IsBot)
				return;

			if (info.DeployTrigger.HasFlag(DeployTriggers.Attack))
				TryDeploy(self);
		}

		void INotifyAttack.PreparingAttack(Actor self, Target target, Armament a, Barrel barrel) { }

		void ITick.Tick(Actor self)
		{
			if (!self.Owner.IsBot)
				return;

			if (undeployable && --undeployTicks < 0)
			{
				Undeploy(self);
			}

			if (deployTicks > 0)
				deployTicks--;
		}

		void INotifyDamage.Damaged(Actor self, AttackInfo e)
		{
			if (!self.Owner.IsBot)
				return;

			if (e.Damage.Value > 0 && info.DeployTrigger.HasFlag(DeployTriggers.Damage))
				TryDeploy(self);

			if (e.Damage.Value < 0 && info.DeployTrigger.HasFlag(DeployTriggers.Heal))
				TryDeploy(self);
		}
	}
}
