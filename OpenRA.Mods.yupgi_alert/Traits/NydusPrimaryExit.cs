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
//using System.Linq;
using OpenRA.Traits;
using OpenRA.Mods.Common.Orders;
using OpenRA.Mods.Common.Traits;

namespace OpenRA.Mods.yupgi_alert.Traits
{
	static class NydusPrimaryExitExts
	{
		public static bool IsPrimaryNydusExit(this Actor a)
		{
			var pb = a.TraitOrDefault<NydusPrimaryExit>();
			return pb != null && pb.IsPrimary;
		}
	}

	[Desc("Used with Nydus trait for primary exit designation")]
	public class NydusPrimaryExitInfo : ITraitInfo, Requires<UpgradeManagerInfo>
	{
		[UpgradeGrantedReference, Desc("The upgrades to grant while the primary exit.")]
		public readonly string[] Upgrades = { "primary" };

		[Desc("The speech notification to play when selecting a primary exit.")]
		public readonly string SelectionNotification = "PrimaryBuildingSelected";

		public object Create(ActorInitializer init) { return new NydusPrimaryExit(init.Self, this); }
	}

	public class NydusPrimaryExit : IIssueOrder, IResolveOrder
	{
		readonly NydusPrimaryExitInfo info;
		readonly UpgradeManager manager;

		public bool IsPrimary { get; private set; }
		//public bool IsPrimary = false; // Better off as a public var. Promoting to primary revokes primaryness of previous one.

		public NydusPrimaryExit(Actor self, NydusPrimaryExitInfo info)
		{
			this.info = info;
			IsPrimary = false;
			manager = self.Trait<UpgradeManager>();
		}

		public IEnumerable<IOrderTargeter> Orders
		{
			get { yield return new DeployOrderTargeter("PrimaryExit", 1); }
		}

		public Order IssueOrder(Actor self, IOrderTargeter order, Target target, bool queued)
		{
			if (order.OrderID == "PrimaryExit")
				return new Order(order.OrderID, self, false);

			return null;
		}

		public void ResolveOrder(Actor self, Order order)
		{
			if (order.OrderString == "PrimaryExit")
				// You can NEVER unselect a primary building, unlike primary productions buildings in RA1.
				SetPrimary(self);
		}

		public void RevokePrimary(Actor self)
		{
			IsPrimary = false;
			foreach (var up in info.Upgrades)
			{
				var manager = self.Trait<UpgradeManager>();
				manager.RevokeUpgrade(self, up, this);
			}
		}

		public void SetPrimary(Actor self)
		{
			// revoke primary of previous primary actor.
			var counter = self.Owner.PlayerActor.Trait<NydusCounter>();
			var pri = counter.PrimaryActor;
			if (pri != null)
				// Well, initially, there is no tunnel at all. Need to check.
				pri.Trait<NydusPrimaryExit>().RevokePrimary(pri);

			IsPrimary = true;
			counter.PrimaryActor = self; // keep track of primary.
			foreach (var up in info.Upgrades)
				manager.GrantUpgrade(self, up, this);

			Game.Sound.PlayNotification(self.World.Map.Rules, self.Owner, "Speech", info.SelectionNotification, self.Owner.Faction.InternalName);
		}
	}
}
