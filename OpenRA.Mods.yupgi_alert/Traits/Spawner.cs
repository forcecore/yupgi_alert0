#region Copyright & License Information
/*
 * Modded by Boolbada of OP Mod.
 * Modded from cargo.cs but a lot changed.
 * 
 * Copyright 2007-2017 The OpenRA Developers (see AUTHORS)
 * This file is part of OpenRA, which is free software. It is made
 * available to you under the terms of the GNU General Public License
 * as published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version. For more
 * information, see COPYING.
 */
#endregion

using System;
using System.Drawing;
using System.Collections.Generic;
using System.Linq;
using OpenRA.Mods.Common.Activities;
using OpenRA.Mods.yupgi_alert.Activities;
using OpenRA.Mods.Common.Orders;
using OpenRA.Mods.Common.Traits;
using OpenRA.Mods.Common;
using OpenRA.Primitives;
using OpenRA.Traits;

namespace OpenRA.Mods.yupgi_alert.Traits
{
	[Desc("This actor can transport slave actors.")]
	public class SpawnerInfo : ITraitInfo, Requires<IOccupySpaceInfo>, Requires<UpgradeManagerInfo>
	{
		[Desc("Number of slave units")]
		public readonly int Count = 0;

		[Desc("Slave unit type")]
		public readonly string SlaveUnit;

		[Desc("Slave regen delay, in ticks")]
		public readonly int RegenTicks = 150;

		[Desc("Slave rearm delay, in ticks")]
		public readonly int RearmTicks = 150;

		[Desc("Pip color of the slaved unit.")]
		public readonly PipType PipType = PipType.Yellow;

		[Desc("Terrain types that this actor is allowed to eject actors onto. Leave empty for all terrain types.")]
		public readonly HashSet<string> UnloadTerrainTypes = new HashSet<string>();

		[Desc("Which direction the passenger will face (relative to the spawner) when unloading.")]
		public readonly int PassengerFacing = 0;

		[Desc("Insta-repair spawners when they return?")]
		public readonly bool InstaRepair = true;

		[UpgradeGrantedReference]
		[Desc("The upgrades to grant to self while loading slaves.")]
		public readonly string[] LoadingUpgrades = { };

		public object Create(ActorInitializer init) { return new Spawner(init, this); }
	}

	class SlaveEntry
	{
		public Actor s;
		public int RearmTicks;
	}

	public class Spawner : IPips, INotifyCreated, INotifyKilled,
		INotifyOwnerChanged, INotifyAddedToWorld, ITick, INotifySold, INotifyActorDisposing,
		INotifyAttack, INotifyBecomingIdle
	{
		public readonly SpawnerInfo Info;
		readonly Actor self;
		readonly UpgradeManager upgradeManager;
		readonly List<SlaveEntry> slaves = new List<SlaveEntry>(); // contained
														   // keep track of launched ones so spawner can call them in or designate another target.
		readonly HashSet<Actor> launched = new HashSet<Actor>();
		readonly Lazy<IFacing> facing;
		readonly bool checkTerrainType;

		//Aircraft aircraft;
		// Carriers don't need to land to spawn stuff!
		// I want to make this like Protoss Carrier.

		CPos currentCell;
		public IEnumerable<CPos> CurrentAdjacentCells { get; private set; }
		public bool Unloading { get; internal set; }
		//public IEnumerable<Actor> Slaves { get { return slaves; } }
		public int SlaveCount { get { return slaves.Count; } }

		int regen_ticks = -1; // -1: ticking disabled.

		public Spawner(ActorInitializer init, SpawnerInfo info)
		{
			self = init.Self;
			Info = info;
			Unloading = false;
			checkTerrainType = info.UnloadTerrainTypes.Count > 0;
			upgradeManager = self.Trait<UpgradeManager>();

			// Fill slaves.
			for (var i = 0; i < info.Count; i++)
			{
				Replenish(self);
			}

			facing = Exts.Lazy(self.TraitOrDefault<IFacing>);
		}

		void Replenish(Actor self)
		{
			var unit = self.World.CreateActor(false, Info.SlaveUnit.ToLowerInvariant(),
				new TypeDictionary { new OwnerInit(self.Owner) });
			var spawned = unit.Trait<Spawned>();
			spawned.Master = self; // let the spawned unit return to me for reloading and repair.

			var se = new SlaveEntry();
			se.s = unit;
			se.RearmTicks = 0;
			slaves.Add(se);
		}

		public void Created(Actor self)
		{
			//aircraft = self.TraitOrDefault<Aircraft>();
			// If I want the airbourne spawner to land, I need to revive this logic (as was in cargo.cs)
		}

		IEnumerable<CPos> GetAdjacentCells()
		{
			return Util.AdjacentCells(self.World, Target.FromActor(self)).Where(c => self.Location != c);
		}

		public bool CanLoad(Actor self, Actor a)
		{
			return true; // can always load slaves, unless the airbourne carrier has to land (not implemented)
		}

		void INotifyAttack.PreparingAttack(Actor self, Target target, Armament a, Barrel barrel) { }

		void MakeSlaveAttack(Actor self, Actor s, Target t)
		{
			s.CancelActivity();
			// Make the spawned actor attack my target.
			if (s.TraitOrDefault<AttackPlane>() != null)
				s.QueueActivity(new SpawnedFlyAttack(s, t));
			else if (s.TraitOrDefault<AttackHeli>() != null)
			{
				Game.Debug("Warning: AttackHeli's are not ready for spawned slave.");
				s.QueueActivity(new HeliAttack(s, t)); // not ready for helis...
			}
			else
				s.QueueActivity(new Attack(s, t, false, false));
		}

		// Tell my slaves to attack what I'm attacking.
		void INotifyAttack.Attacking(Actor self, Target target, Armament a, Barrel barrel)
		{
			// The rate of fire of the dummy weapon determines the launch cycle.
			if (slaves.Count == 0)
				return;

			var s = Launch(self);
			if (s == null)
				return;
			if (s.Disposed)
				return;

			self.World.AddFrameEndTask(w =>
			{
				var move = s.Trait<IMove>();
				var pos = s.Trait<IPositionable>();
				var spawn = self.CenterPosition;

				pos.SetVisualPosition(s, spawn);
				MakeSlaveAttack(self, s, target);
				w.Add(s);
			});

			// Also, make launched ones attack, too.
			foreach(var launched in launched)
			{
				MakeSlaveAttack(self, launched, target);
			}
		}

		public virtual void OnBecomingIdle(Actor self)
		{
			Recall(self);
		}

		void Recall(Actor self)
		{
			// Tell launched slaves to come back and enter me.
			foreach (var s in launched)
			{
				s.Trait<Spawned>().EnterSpawner(s);
			}
		}

		public void SlaveKilled(Actor self, Actor slave)
		{
			if (self.IsDead)
				return;

			if (launched.Contains(slave))
				launched.Remove(slave);

			regen_ticks = Info.RegenTicks; // set clock so that regen happens.
		}

		Actor PopLaunchable(Actor self)
		{
			SlaveEntry result = null;
			foreach (var se in slaves)
			{
				if (se.RearmTicks <= 0)
				{
					result = se;
					break;
				}
			}

			if (result != null)
			{
				slaves.Remove(result);
				return result.s;
			}
			return null;
		}

		public Actor Launch(Actor self)
		{
			var a = PopLaunchable(self);
			if (a == null)
				return null;
			SetPassengerFacing(a);
			launched.Add(a);
			return a;
		}

		void SetPassengerFacing(Actor passenger)
		{
			if (facing.Value == null)
				return;

			var passengerFacing = passenger.TraitOrDefault<IFacing>();
			if (passengerFacing != null)
				passengerFacing.Facing = facing.Value.Facing + Info.PassengerFacing;

			foreach (var t in passenger.TraitsImplementing<Turreted>())
				t.TurretFacing = facing.Value.Facing + Info.PassengerFacing;
		}

		public IEnumerable<PipType> GetPips(Actor self)
		{
			var numPips = Info.Count;

			for (var i = 0; i < numPips; i++)
				yield return GetPipAt(i);
		}

		PipType GetPipAt(int i)
		{
			if (i < slaves.Count)
				return Info.PipType;
			else
				return PipType.Transparent;
		}

		public void Load(Actor self, Actor a)
		{
			if (launched.Contains(a))
				launched.Remove(a);
			foreach (var u in Info.LoadingUpgrades)
				upgradeManager.RevokeUpgrade(self, u, this);

			// Set up rearm.
			var se = new SlaveEntry();
			se.s = a;
			se.RearmTicks = Info.RearmTicks;
			slaves.Add(se);
		}

		public void Killed(Actor self, AttackInfo e)
		{
			foreach (var c in slaves)
				c.s.Kill(e.Attacker);
			foreach (var c in launched)
			{
				if (!c.IsDead)
					c.Kill(e.Attacker);
			}

			slaves.Clear();
			launched.Clear();
		}

		public void Disposing(Actor self)
		{
			foreach (var c in slaves)
				c.s.Dispose();
			foreach (var c in launched)
				c.Dispose();

			slaves.Clear();
			launched.Clear();
		}

		public void Selling(Actor self) { }
		public void Sold(Actor self)
		{
			// Dispose slaved.
			foreach (var c in slaves)
				c.s.Dispose();
			slaves.Clear();

			// Kill launched.
			foreach (var c in launched)
				c.Kill(self);
			launched.Clear();
		}

		void SpawnSlave(Actor s)
		{
			self.World.AddFrameEndTask(w =>
			{
				w.Add(s);
				s.Trait<IPositionable>().SetPosition(s, self.Location);

				// TODO: this won't work well for >1 actor as they should move towards the next enterable (sub) cell instead
			});
		}

		public void OnOwnerChanged(Actor self, Player oldOwner, Player newOwner)
		{
			self.World.AddFrameEndTask(w =>
			{
				foreach (var s in slaves)
					s.s.Owner = newOwner; // Under influence of mind control.
				foreach (var s in launched) // Kill launched, they are not under influence.
					s.Kill(self);
			});
		}

		public void AddedToWorld(Actor self)
		{
			// Force location update to avoid issues when initial spawn is outside map
			currentCell = self.Location;
			CurrentAdjacentCells = GetAdjacentCells();
		}

		public void Tick(Actor self)
		{
			var cell = self.World.Map.CellContaining(self.CenterPosition);
			if (currentCell != cell)
			{
				currentCell = cell;
				CurrentAdjacentCells = GetAdjacentCells();
			}

			// Regeneration
			if (regen_ticks > 0)
				regen_ticks--;
			if (regen_ticks == 0)
			{
				regen_ticks = -1;

				while (slaves.Count + launched.Count < Info.Count)
					Replenish(self);
			}

			// Rearm
			foreach (var se in slaves)
			{
				if (se.RearmTicks > 0)
					se.RearmTicks--;
			}
		}
	}

	[Desc("Can be slaved to a spawner.")]
	class SpawnedInfo : ITraitInfo
	{
		public readonly string EnterCursor = "enter";

		[Desc("Move this close to the spawner, before entering it.")]
		public readonly WDist LandingDistance = new WDist(5*1024);

		public object Create(ActorInitializer init) { return new Spawned(init, this); }
	}

	class Spawned : IIssueOrder, IResolveOrder, INotifyKilled, INotifyBecomingIdle
	{
		readonly SpawnedInfo info;
		public Actor Master = null;

		public Spawned(ActorInitializer init, SpawnedInfo info)
		{
			this.info = info;
		}

		public IEnumerable<IOrderTargeter> Orders
		{
			get { yield return new SpawnedReturnOrderTargeter(info); }
		}

		void INotifyKilled.Killed(Actor self, AttackInfo e)
		{
			// If killed, I tell my master that I'm gone.
			var spawner = Master.Trait<Spawner>();
			spawner.SlaveKilled(Master, self);
		}

		public Order IssueOrder(Actor self, IOrderTargeter order, Target target, bool queued)
		{
			// don't mind too much about this part.
			// Everything is (or, should be.) automatically ordered properly by the master.

			if (order.OrderID != "SpawnedReturn")
				return null;

			if (target.Type == TargetType.FrozenActor)
				return null;

			return new Order(order.OrderID, self, queued) { TargetActor = target.Actor };
		}

		static bool IsValidOrder(Actor self, Order order)
		{
			// Not targeting a frozen actor
			if (order.ExtraData == 0 && order.TargetActor == null)
				return false;

			var spawned = self.Trait<Spawned>();
			return order.TargetActor == spawned.Master;
		}

		public void ResolveOrder(Actor self, Order order)
		{
			if (order.OrderString != "SpawnedReturn" || !IsValidOrder(self, order))
				return;

			var target = self.ResolveFrozenActorOrder(order, Color.Green);
			if (target.Type != TargetType.Actor)
				return;

			if (!order.Queued)
				self.CancelActivity();

			self.SetTargetLine(target, Color.Green);
			EnterSpawner(self);
		}

		public void EnterSpawner(Actor self)
		{
			if (Master == null)
				self.Kill(self); // No master == death.
			else
			{
				var tgt = Target.FromActor(Master);
				self.CancelActivity();
				if (self.TraitOrDefault<AttackPlane>() != null) // Let attack planes approach me first, before landing.
					self.QueueActivity(new Fly(self, tgt, WDist.Zero, info.LandingDistance));
				self.QueueActivity(new EnterSpawner(self, Master, EnterBehaviour.Exit));
			}
		}

		public virtual void OnBecomingIdle(Actor self)
		{
			// Return when nothing to attack.
			// Don't let myself to circle around the player's construction yard.
			EnterSpawner(self);
		}

		class SpawnedReturnOrderTargeter : UnitOrderTargeter
		{
			SpawnedInfo info;

			public SpawnedReturnOrderTargeter(SpawnedInfo info)
				: base("SpawnedReturn", 6, info.EnterCursor, false, true)
			{
				this.info = info;
			}

			public override bool CanTargetActor(Actor self, Actor target, TargetModifiers modifiers, ref string cursor)
			{
				if (!target.Info.HasTraitInfo<SpawnerInfo>())
					return false;

				if (self.Owner != target.Owner)
					// can only enter player owned one.
					return false;

				var spawned = self.Trait<Spawned>();

				if (target != spawned.Master)
					return false;

				return true;
			}

			public override bool CanTargetFrozenActor(Actor self, FrozenActor target, TargetModifiers modifiers, ref string cursor)
			{
				// You can't enter frozen actor.
				return false;
			}
		}
	}
}
