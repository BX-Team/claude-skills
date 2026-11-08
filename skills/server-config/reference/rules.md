# Rules

Every key the optimiser writes, grouped by file. Columns:

- **Value**: what to write, using the derived numbers from SKILL.md. "—" in a condition
  means the key is left alone.
- **Flags**: *G* gameplay (players can notice; skipped when the profile is vanilla-only),
  *A* aggressive only, *Pu* needs Purpur or DivineMC, *D* needs DivineMC.

Skip any key whose value equals the default shipped by the chosen software
([defaults.md](defaults.md)).

## server.properties

| Key | Value | Flags | Why |
| --- | --- | --- | --- |
| `network-compression-threshold` | `256` without a proxy, `-1` behind one | | Behind a proxy the hop is local, so compression only burns CPU; on a public port 256 keeps bandwidth down. |
| `simulation-distance` | simulation | G | Chunks this close to a player tick: mobs, crops, furnaces. The single most expensive number on the server. |
| `view-distance` | view | G | Chunks sent but not ticked. Players still see far, the server does not pay for it. |
| `entity-broadcast-range-percentage` | `75` | G A | How close a player must be before entities are sent. Less packet traffic on a crowded server. |
| `online-mode` | `false` behind a proxy or in offline mode | | A backend behind a proxy must not authenticate; the proxy already did. |
| `enforce-secure-profile` | `false` in offline mode | | No Mojang chat signatures exist to enforce, and the check rejects those players. |
| `allow-flight` | `true` with an anti-cheat | | The vanilla flight check false-flags movement on a laggy tick; let the anti-cheat do it. |

## bukkit.yml

| Key | Value | Flags | Why |
| --- | --- | --- | --- |
| `settings.query-plugins` | `false` | | Stops the server listing its plugins to anyone who queries the port. Already the default on DivineMC. |
| `chunk-gc.period-in-ticks` | `300` | | Sweeps unreferenced chunks twice as often. |
| `spawn-limits.monsters`, `.animals`, `.water-animals`, `.water-ambient`, `.water-underground-creature`, `.axolotls`, `.ambient` | derived caps | G | The cap is per player, so on a busy server the default means thousands of mobs. |
| `ticks-per.monster-spawns` | 10 (15 on Aggressive) | G | Ticks between spawn attempts. |
| `ticks-per.animal-spawns`, `.water-spawns`, `.water-ambient-spawns`, `.water-underground-creature-spawns`, `.axolotl-spawns`, `.ambient-spawns` | `400` | G | Water and ambient mobs don't need an attempt every tick. |

## spigot.yml

| Key | Value | Flags | Why |
| --- | --- | --- | --- |
| `settings.save-user-cache-on-stop-only` | `true` | | The user cache is rebuildable; rewriting it on every disconnect is disk traffic for nothing. Already the default on DivineMC. |
| `settings.netty-threads` | `clamp(cores / 4, 1, 8)` | | Network threads, about a quarter of the cores. The main tick needs the rest. |
| `settings.bungeecord` | `true` with BungeeCord | | Reads the identity BungeeCord forwards. |
| `settings.log-villager-deaths`, `settings.log-named-deaths` | `false` | | Console and disk noise, constant on a farm server. |
| `world-settings.default.mob-spawn-range` | derived | G | Keep it at or below simulation distance, or mobs spawn in chunks that never tick. |
| `world-settings.default.entity-activation-range.{animals,monsters,raiders,misc,water,villagers,flying-monsters}` | activation table | G | Distance past which the group stops being fully ticked. The biggest single win with many entities. |
| `world-settings.default.entity-activation-range.tick-inactive-villagers` | `false` | G | Villagers outside the range stop thinking; that is most of the villager cost. |
| `world-settings.default.entity-activation-range.ignore-spectators` | `true` | | A spectator should not keep entities awake. |
| `world-settings.default.entity-tracking-range.{players,animals,monsters,misc,other}` | tracking values | G | Distance at which entities are sent. Keep it above activation or mobs appear from nowhere. |
| `world-settings.default.entity-activation-range.wake-up-inactive.{animals,villagers}-max-per-tick` | `2` | G A | How many inactive entities wake per tick; halving smooths the cost of a big herd. |
| `world-settings.default.entity-activation-range.wake-up-inactive.{monsters,flying-monsters}-max-per-tick` | `4` | G A | Same. |
| `world-settings.default.entity-activation-range.wake-up-inactive.{animals,monsters,villagers,flying-monsters}-for` | `60` | G A | How long a woken entity stays awake. |
| `world-settings.default.nerf-spawner-mobs` | `true` | G | Spawner mobs get no AI. They still drop loot. |
| `world-settings.default.merge-radius.item` | 3.5 (4 on Aggressive) | G | Nearby dropped items stack into one entity. |
| `world-settings.default.merge-radius.exp` | 4 (8 on Aggressive) | G | Same for XP orbs, where grinders make thousands of entities. |
| `world-settings.default.ticks-per.hopper-transfer` | 8 (20 on Aggressive) | G | Hoppers are the most expensive block entity in the game. |
| `world-settings.default.ticks-per.hopper-check` | 8 (10 on Aggressive) | G | Ticks between a hopper looking for an item above it. |
| `world-settings.default.hanging-tick-frequency` | `250` | G A | Item frames, paintings and leads almost never change. |
| `world-settings.default.max-tnt-per-tick` | per type | G | One TNT cannon cannot stall the server. |
| `world-settings.default.arrow-despawn-rate` | `300` | G A | Arrows on the ground vanish after 15 s instead of a minute. |

## config/paper-global.yml

| Key | Value | Flags | Why |
| --- | --- | --- | --- |
| `misc.max-joins-per-tick` | `2` at 60+ players | | Spreads a reconnect storm after a restart over more ticks. |
| `proxies.velocity.enabled`, `proxies.velocity.online-mode` | `true` with Velocity | | Accept Velocity forwarding and keep online-mode UUIDs. The `secret` is filled in by hand. |
| `proxies.bungee-cord.online-mode` | `!offlineMode` with BungeeCord | | Which UUID shape the backend trusts. |
| `unsupported-settings.allow-headless-pistons`, `.allow-permanent-block-break-exploits`, `.allow-piston-duplication` | `true` on anarchy | G | Exploits an anarchy server is expected to keep. |
| `item-validation.book.author` / `.book.page` / `.book.title` | 4096 / 8192 / 4096 | hardening | Book and item limits; the defaults allow payloads that lock up clients and the server relaying them. |
| `item-validation.book-size.page-max` / `.total-multiplier` | 2048 / 0.92 | hardening | Same. |
| `item-validation.display-name` / `.lore-line` | 2048 / 4096 | hardening | Same. |
| `item-validation.resolve-selectors-in-books` | `false` | hardening | Same. |
| `packet-limiter.all-packets.{action,interval,max-packet-rate}` | `KICK`, `6.0`, `500.0` | hardening | Anything above this rate is not a client playing the game. |
| `packet-limiter.overrides.<packet>.{action,interval,max-packet-rate}` | table below | hardening | Caps one packet type; without it one modified client can hang the main thread. |

Packet overrides (from the SpigotMC optimisation guide):

| Packet | Action | Interval | Max rate |
| --- | --- | --- | --- |
| `minecraft:command_suggestion` | DROP | 1.0 | 10.0 |
| `minecraft:container_button_click` | KICK | 1.5 | 15.0 |
| `minecraft:container_click` | KICK | 3.0 | 32.0 |
| `minecraft:custom_payload` | DROP | 1.5 | 25.0 |
| `minecraft:interact` | KICK | 2.0 | 30.0 |
| `minecraft:place_recipe` | DROP | 3.0 | 6.0 |
| `minecraft:player_action` | KICK | 3.0 | 240.0 |
| `minecraft:set_creative_mode_slot` | DROP | 2.5 | 20.0 |
| `minecraft:use_item_on` | KICK | 2.0 | 26.0 |

## config/paper-world-defaults.yml

| Key | Value | Flags | Why |
| --- | --- | --- | --- |
| `chunks.prevent-moving-into-unloaded-chunks` | `true` | | Stops a synchronous chunk load on the main thread when a player walks into one. |
| `chunks.max-auto-save-chunks-per-tick` | derived | | Too low and the leftovers land in one tick as a freeze. |
| `chunks.entity-per-chunk-save-limit.<type>` | table below | | Without it an arrow farm produces a chunk the server cannot load again. |
| `collisions.max-entity-collisions` | `2` | G | Cramming a thousand mobs in a block stops being a server-wide cost. |
| `collisions.fix-climbing-bypassing-cramming-rule` | `true` | G | Climbing mobs stop being exempt from cramming (one-block spider farms). |
| `entities.armor-stands.tick`, `entities.armor-stands.do-collision-entity-lookups` | `false`, unless custom entities | G | Armour stands stop being pushed and scanning for collisions. |
| `entities.markers.tick` | `false`, unless custom entities | | Markers hold data and never move. |
| `entities.behavior.disable-chest-cat-detection` | `true` | G | Chests stop scanning for a sitting cat. |
| `entities.behavior.parrots-are-unaffected-by-player-movement` | `true` | G | Parrots stay on the shoulder. |
| `entities.behavior.zombies-target-turtle-eggs` | `false` | G A | Zombies stop pathfinding to turtle eggs across the map; breaks farms built on it. |
| `entities.spawning.non-player-arrow-despawn-rate`, `.creative-arrow-despawn-rate` | `20` | | Nobody can pick those arrows up anyway. |
| `entities.spawning.despawn-ranges.<category>.hard` | `simulation·16 + 8` | G | For every category: ambient, axolotls, creature, misc, monster, underground_water_creature, water_ambient, water_creature. |
| `entities.spawning.despawn-ranges.<category>.soft` | `30` | G | Between soft and hard a mob may despawn each tick. |
| `entities.spawning.alt-item-despawn-rate.enabled` | `true` | G A | Per-item despawn times; replaces ground-item clearing plugins. |
| `entities.spawning.alt-item-despawn-rate.items.<item>` | `300` (scaffolding `600`) | G A | Bulk items despawn in 15 s: cobblestone, netherrack, sand, red_sand, gravel, dirt, short_grass, pumpkin, melon_slice, kelp, bamboo, sugar_cane, twisting_vines, weeping_vines, the eight leaf types (oak, spruce, birch, jungle, acacia, dark_oak, mangrove, cherry), cactus, diorite, granite, andesite. |
| `environment.optimize-explosions` | `true` | | Faster explosion algorithm, differences nobody notices. |
| `environment.treasure-maps.enabled` | `false` unless pregenerated | G | The structure search hangs the server in ungenerated terrain. |
| `environment.treasure-maps.find-already-discovered.loot-tables`, `.villager-trade` | `true` | | New maps can point at already found structures. |
| `environment.nether-ceiling-void-damage-height` | `127` on survival and minigames | G A | Stops nether-roof highways and the chunk loading they cause. |
| `environment.max-block-ticks`, `environment.max-fluid-ticks` | `40960` | G A | One water flood cannot take the server down. |
| `fixes.fix-items-merging-through-walls` | `true` | G | A duplication vector and a source of teleporting items. |
| `hopper.ignore-occluding-blocks` | `true` | G | Hoppers stop looking into containers buried in full blocks. |
| `hopper.disable-move-event` | `true` | G A | Only when no plugin listens to `InventoryMoveItemEvent`; most protection plugins do. |
| `maps.item-frame-cursor-limit` / `.item-frame-cursor-update-interval` | 32 / 20 | G | Item-frame maps are a surprisingly large packet cost. |
| `misc.redstone-implementation` | `ALTERNATE_CURRENT`, `VANILLA` on technical | G | Alternate Current removes redundant block updates. |
| `misc.update-pathfinding-on-block-update` | `false` | G | Mobs repath on a timer, not on every block change. |
| `misc.disable-relative-projectile-velocity` | `true` | G A | Projectiles stop inheriting the shooter's movement. |
| `tick-rates.grass-spread` / `tick-rates.mob-spawner` | 4 / 2 | G | Background world processes nobody watches. |
| `tick-rates.dry-farmland`, `tick-rates.wet-farmland` | `2` | G A | Farmland checked half as often. |
| `tick-rates.behavior.villager.validatenearbypoi` / `.acquirepoi` | 60 / 120, not with DAB | G | Acquiring a workstation is the heaviest thing a villager does. |
| `tick-rates.sensor.villager.secondarypoisensor` / `.nearestbedsensor` | 80 / 80, not with DAB | G | Same. |
| `tick-rates.sensor.villager.villagerbabiessensor` / `.playersensor` / `.nearestlivingentitysensor` | 40 each, not with DAB | G | Same. |
| `anticheat.anti-xray.enabled` | `true` on survival and anarchy | | Cheaper than any anti-xray plugin, and it works on the chunk packet itself. |

Entity save limits per chunk: area_effect_cloud 8, arrow 16, breeze_wind_charge 8,
dragon_fireball 3, egg 8, ender_pearl 8, experience_bottle 3, experience_orb 16,
eye_of_ender 8, fireball 8, firework_rocket 8, llama_spit 3, splash_potion 8,
lingering_potion 8, shulker_bullet 8, small_fireball 8, snowball 8, spectral_arrow 16,
trident 16, wind_charge 8, wither_skull 4.

## purpur.yml

All *Pu*.

| Key | Value | Flags | Why |
| --- | --- | --- | --- |
| `settings.use-alternate-keepalive` | `true` | | Bad connections stop being kicked for one dropped keepalive. Conflicts with TCPShield. Already the default on DivineMC. |
| `settings.lagging-threshold` | `17.0` | | TPS below which Purpur applies its own lag measures. |
| `settings.logger.suppress-init-legacy-material-errors`, `-ignored-advancement-warnings`, `-unrecognized-recipe-errors`, `-setblock-in-far-chunk-errors`, `-library-loader` | `true` | | Console noise nobody acts on. |
| `world-settings.default.mobs.dolphin.disable-treasure-searching` | `true` | G | The same expensive structure search treasure maps do. |
| `world-settings.default.mobs.villager.lobotomize.enabled` | `true` at 30+ players | G | A villager that cannot path anywhere only restocks. Only when villagers are the problem. |
| `world-settings.default.mobs.villager.search-radius.acquire-poi`, `.nearest-bed-sensor` | `16` | G | The vanilla 48-block scan runs over and over. |
| `world-settings.default.mobs.zombie.aggressive-towards-villager-when-lagging` | `false` | G | Below the lagging threshold zombies stop hunting villagers, the most expensive pathfinding in the game. |
| `world-settings.default.mobs.squid.immune-to-EAR` | `false` | G | Squid obey the activation range like everything else. |
| `world-settings.default.gameplay-mechanics.entities-can-use-portals` | `false`, not on technical | G A | Stops minecart chunk loaders through portals. |
| `world-settings.default.gameplay-mechanics.player.teleport-if-outside-border` | `true`, not on anarchy | G | The vanilla border is bypassable; this sends escapees back to spawn. |
| `world-settings.default.gameplay-mechanics.armorstand.can-movement-tick`, `.can-move-in-water`, `.can-move-in-water-over-fence` | `false`, unless custom entities | G A | The classic armour stand lag machine. |
| `world-settings.default.blocks.observer.disable-clock` | `true`, not on technical or anarchy | G A | Two facing observers stop making an endless signal. |

## divinemc.yml

All *D*.

| Key | Value | Flags | Why |
| --- | --- | --- | --- |
| `region-settings.thread-count` | `clamp(cores / 2, 1, 8)` | | Threads reading and writing region files. |
| `async.pathfinding.max-threads` | `clamp(cores / 4, 1, 4)` | | Pathfinding off the main thread; pinned so the number is visible instead of an implicit 0. |
| `async.parallel-sensors.enable` | `true` at 4+ cores | | The read-only half of mob AI (entity scans, line of sight) runs on a pool. |
| `async.chunk-sending.enable` / `.max-threads` | `true` / `clamp(cores / 4, 1, 4)` at 20+ players | | Chunk serialisation off the main thread; that is what a join storm costs. |
| `async.parallel-world-ticking.enable` / `.thread-count` | `true` / derived, when enabled | | Each world on its own thread. Needs thread-safe plugins. `thread-count` caps how many worlds tick at once. |
| `async.regionized-chunk-ticking.enable` / `.executor-thread-count` | `true` / derived, when enabled | | Regions of a world tick in parallel, like Folia. DivineMC's least conservative option. |
| `performance.dab.enabled` / `.start-distance` / `.activation-distance-mod` | `true` / derived, when DAB is on | G | Distant mobs think less often the further away they are. |
| `performance.optimizations.clump-orbs` | `true` | G | XP orbs merge into one entity carrying the total. |
| `performance.optimizations.use-compact-bit-storage`, `.equipment-tracking`, `.optimized-dragon-respawn` | `true` | | Cheaper internal representations, no game change. |
| `performance.optimizations.sleeping-block-entity` | `true` | G | Idle block entities stop ticking until woken. Changes hopper and furnace timing. |
| `performance.optimizations.hopper-throttle-when-full.enabled` / `.skip-ticks` | `true` / `20` | G A | A hopper into a full container stops retrying for a while. |
| `performance.optimizations.enable-suffocation-optimization`, `misc.lag-compensation.enabled` | `false` on technical | | The two non-vanilla behaviours DivineMC enables by default. |
| `performance.chunks.chunk-data-cache-soft-limit` / `.chunk-data-cache-limit` | derived | | Trade heap for fewer re-reads with many chunks in play. |
| `network.raytrace-entity-culling.enabled` | `true` at 30+ players, not technical | G | Entities a player provably cannot see are not sent. Saves bandwidth, blinds entity ESP. |
| `misc.secure-seed.enable` | `true` on anarchy | G | A seed that cannot be cracked from the world. Needs freshly generated chunks. |
| `world-settings.default.unsupported-features.allow-tripwire-dupe`, `misc.old-features.copper-bulb-1gt`, `misc.old-features.crafter-1gt` | `true` on anarchy | G | The old duplication and timing behaviour anarchy players expect. |
| `network.no-chat-reports.enabled` | `true` in offline mode | | Tells clients the server carries no signed chat. |
| `network.general.disable-disconnect-spam` | `true` on anarchy | | No console flood from deliberate connection abuse. |
