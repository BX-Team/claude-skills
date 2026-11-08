---
name: server-config
description: Optimise a Minecraft server's configuration on Paper, Purpur or DivineMC. Use when someone asks how to make their server run better, why it lags, which settings to change for a kind of server (survival, SMP, anarchy, minigames, PvP, creative, plots, technical, redstone), or asks for optimised server.properties, bukkit.yml, spigot.yml, paper-global.yml, paper-world-defaults.yml, purpur.yml or divinemc.yml, or wants an existing config reviewed.
---

# Server config optimiser

You advise on, and write, optimised configuration for a Minecraft server running Paper,
Purpur or DivineMC. The fork chain matters: Purpur is downstream of Paper and DivineMC
of Purpur, so a server always has every file of the software above it.

| File | Location | Exists on |
| --- | --- | --- |
| `server.properties` | server root | all |
| `bukkit.yml` | server root | all |
| `spigot.yml` | server root | all |
| `paper-global.yml` | `config/` | all |
| `paper-world-defaults.yml` | `config/` | all |
| `purpur.yml` | server root | Purpur, DivineMC |
| `divinemc.yml` | server root | DivineMC |

Answer in the language the user writes in. Keep keys, file names and values exactly as
they appear in the files.

## The two rules that are never broken

1. **Overrides, not whole files.** Write only the keys that change, as a snippet the user
   merges into the file they already have. Never produce a complete file: upstream owns
   the defaults and they move every release, and a stale full file silently resets
   everything the user had changed. A missing key is filled in with its default when the
   server starts, so a partial file is fine on a fresh install too.
2. **No key path from memory.** Paper, Spigot and Purpur ignore an unknown key without an
   error, so a wrong path is worse than no advice. Every key the rules below write is
   verified in [reference/defaults.md](reference/defaults.md), together with the value it
   ships with. For a `divinemc.yml` key outside that list, read
   `apps/web/app/lib/divinemc/defaults.ts` and `descriptions.ts` in
   [BX-Team/code](https://github.com/BX-Team/code):
   they are the source of the published configuration reference. For anything else, check
   the upstream reference (links at the end) before writing it, and say plainly when you
   could not verify a key.

Also: do not write a key whose recommended value equals what the chosen software already
ships (the defaults file lists the three defaults DivineMC changes). If the user asks why
a well-known guide tip is missing, say that it is already the default.

## Work out the profile first

Everything is derived from a handful of answers. Ask for the ones the user has not given,
in one short batch, and assume the defaults in brackets when they don't care:

- **Software**: Paper, Purpur or DivineMC [DivineMC], and the Minecraft version.
- **Server type**: survival/SMP, anarchy, minigames/PvP, creative/plots, technical/redstone [survival].
- **Peak concurrent players**, not registered players [40].
- **CPU cores** the server may really use [8]. Every thread count comes from this.
- **Populated worlds**: one, a few, many [a few].
- **How far to go**: safe, balanced, aggressive [balanced].
  - *Safe*: only changes nobody can observe in game.
  - *Balanced*: the usual trade, mobs think less far away.
  - *Aggressive*: everything, including settings that break farms and some plugins.
- **Proxy**: none, Velocity, BungeeCord [none].
- Yes/no: offline (cracked) mode; an anti-cheat plugin; ItemsAdder / ModelEngine / Oraxen
  (custom entities on armour stands and markers); world pregenerated and fenced by a
  vanilla border; add crash-exploit hardening (packet and book limits) [yes].

A profile is **vanilla-only** when intensity is Safe or the type is technical: then skip
every rule marked *gameplay* in [reference/rules.md](reference/rules.md). Rules marked
*aggressive* apply only on Aggressive.

## Derived numbers

Compute these, don't copy numbers from a guide. `clamp` rounds, then limits.

**Distances.** Base simulation / view distance per type: survival 5/8, anarchy 5/8,
minigames 4/6, creative 3/8, technical 8/10. Let `step` = +1 on Safe, −1 on Aggressive,
0 on Balanced.

- `simulation = base.sim + step`; `view = base.view + 2·step`
- more than 80 players: both −1; 2 cores or fewer: simulation −1, view −2
- `simulation = clamp(simulation, 3, 12)`; `view = clamp(max(view, simulation + 1), 4, 16)`

**Spawning.** Base per-player mob caps (monsters / animals / water / ambient): survival
20/5/2/1, anarchy 20/5/2/1, minigames 4/2/1/1, creative 5/2/1/1, technical 40/10/3/2.
Multiply by 1.6 on Safe and 0.7 on Aggressive, clamp to 1–200. `water-animals` and
`water-ambient` use the water value, `water-underground-creature` and `axolotls` water+1.

- `ticks-per.monster-spawns`: 10 (15 on Aggressive); every other spawn group: 400.
- `mob-spawn-range = clamp(min(Aggressive ? 3 : 4, simulation), 1, 8)`: never above the
  simulation distance, or mobs spawn in chunks that never tick.
- Despawn ranges (every category): `hard = simulation·16 + 8` so mobs never vanish inside
  ticking chunks; `soft = 30`.

**Entity activation range** (spigot.yml), per intensity:

| | animals | monsters | raiders | misc | water | villagers | flying-monsters |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Safe | 24 | 32 | 48 | 12 | 12 | 24 | 48 |
| Balanced | 16 | 24 | 48 | 8 | 8 | 16 | 48 |
| Aggressive | 12 | 20 | 32 | 6 | 6 | 12 | 32 |

**Entity tracking range**: players 48, misc 32, other 64, animals and monsters
`max(48, max(activation.animals, activation.monsters))`. Tracking must stay at or above
activation, or mobs pop into view already moving.

**Other numbers.**

- `netty-threads = clamp(cores / 4, 1, 8)`
- `max-auto-save-chunks-per-tick = clamp(max(24, players / 2), 24, 64)`
- hopper transfer / check: 8/8 (20/10 on Aggressive)
- merge radius item / exp: 3.5/4 (4/8 on Aggressive)
- `max-tnt-per-tick`: survival 60, anarchy 100, minigames 30, creative 60, technical 100
- `entity-broadcast-range-percentage`: 75, Aggressive only

**DivineMC threading.**

- *DAB* on when DivineMC, not vanilla-only and not anarchy. `start-distance` 12 and
  `activation-distance-mod` 8, or 8 and 7 above 100 players.
- *Parallel world ticking* on when DivineMC, more than one world, 6+ cores and not
  technical. On one world there is nothing to run in parallel, only the sync cost.
- *Regionized chunk ticking* on when DivineMC, 6+ cores and not technical.
- The two pools share one budget: `budget = max(2, floor(cores / 2))`, halved when both
  are on. `parallel-world-ticking.thread-count = clamp(budget, 2, 8)`,
  `regionized-chunk-ticking.executor-thread-count = clamp(budget, 1, 12)`. Sized apart,
  each looks fine and together they take every core.
- `region-settings.thread-count = clamp(cores / 2, 1, 8)`;
  `async.pathfinding.max-threads` and `async.chunk-sending.max-threads = clamp(cores / 4, 1, 4)`.
- Chunk data cache soft/hard: 4096/16384 on 4 cores or fewer, 16384/65536 above 60
  players, otherwise 8192/32678.

The full list of keys, their values per profile and the reason for each is in
[reference/rules.md](reference/rules.md). Read it before writing a config.

## Interactions to respect

- **DAB replaces Paper's villager tick rates.** With DAB on, do not write the
  `tick-rates.behavior.villager.*` / `tick-rates.sensor.villager.*` keys: doing both
  makes villagers visibly stupid up close.
- **Custom entity plugins.** With ItemsAdder, ModelEngine or Oraxen, leave armour stand
  and marker ticking alone in both Paper and Purpur.
- **Proxy.** Behind a proxy: `online-mode=false`, compression threshold `-1`, the
  forwarding switch for that proxy, and the backend port firewalled. Velocity's
  `proxies.velocity.secret` is never generated: it is copied from `forwarding.secret` on
  the proxy.
- **Protection plugins.** `hopper.disable-move-event: true` (Aggressive only) skips
  `InventoryMoveItemEvent`, which most protection plugins use to stop hopper theft. Never
  set it when one is installed.
- **Unpregenerated worlds.** Turn treasure maps off: the structure search can hang the
  server in ungenerated terrain. Recommend pregenerating with Chunky inside a vanilla
  world border.
- **Anarchy.** Keep the exploits (headless pistons, permanent block break, piston and
  tripwire duplication), close the crash surfaces instead. Secure seed only affects
  chunks generated after it is enabled.
- **Technical.** Keep vanilla redstone (`misc.redstone-implementation: VANILLA`) and turn
  off DivineMC's two non-vanilla defaults (`performance.optimizations.enable-suffocation-optimization`
  and `misc.lag-compensation.enabled`).
- **Parallel features need thread-safe plugins.** Before recommending regionized chunk
  ticking or parallel world ticking, read the caveats in
  `apps/web/content/docs/divinemc/02.features/` in BX-Team/code (published at
  [bxteam.org/docs/divinemc](https://bxteam.org/docs/divinemc)) and pass them on.

## What to answer with

**Advice questions** ("my server lags with 60 players, what should I change?"): ask for a
spark profile (`/spark profiler`, link to the report) if the cause is unknown, since the
right fix depends on what is actually hot. Then give the few changes with the largest
effect for their situation, in this order of impact: view and simulation distance, entity
activation ranges, spawn limits and ranges, hoppers and redstone, DivineMC threading.
Explain what each costs the players.

**Generate requests**: one fenced block per file that changes, labelled with its path, in
its own format (`properties` or `yaml`), each key preceded by a one-line comment with the
reason. Nest YAML properly, don't write dotted keys. Then:

- the notices that apply (see below),
- what the user still has to do by hand (Velocity secret, firewall, pregeneration),
- one line on merging: paste into the existing file, don't replace it; for YAML, merge
  into the existing sections.

**Review requests** (the user pastes a config): compare against the shipped defaults and
the profile's rules. Point out wrong or outdated paths, values that contradict each other
(tracking below activation, spawn range above simulation distance, both parallel pools at
full size), settings that are already the default, and what their profile would change.

## Notices worth giving

Give only the ones that apply:

- 2 cores or fewer: no config makes that a big server; the answer is a better host.
- Regionized ticking on fewer than 8 cores: watch MSPT after enabling it and lower the
  thread count if it got worse.
- Vanilla-only profile: the config is small on purpose.
- Aggressive: item despawn, hopper events and the nether ceiling are changed; read each
  reason before pasting into a live server.
- Packet limits: `minecraft:custom_payload` also covers plugin messaging; raise that one
  entry if a plugin needs more, rather than dropping the block.
- 100+ players with view distance 8 or more: view distance is the next lever if the
  network, not the tick, is the bottleneck.
- Always: these settings land in the defaults for every world. A nether nobody uses can
  get its own cheaper per-world file under `world/dimensions/`.

## JVM flags

Start flags are a separate question with their own skill, `jvm-flags`. Point the user to
it rather than improvising flags here.

## Sources

- PaperMC configuration reference: https://docs.papermc.io/paper/reference/configuration
  (the sources behind it: https://github.com/PaperMC/docs/tree/main/src/config/paper)
- Purpur configuration: https://purpurmc.org/docs/Configuration/
- YouHaveTrouble's optimisation guide: https://github.com/YouHaveTrouble/minecraft-optimization
- DivineMC configuration reference: https://bxteam.org/docs/divinemc/reference/configuration
- DivineMC features and their caveats: https://bxteam.org/docs/divinemc/features/regionized-chunk-ticking

The verified defaults were read at Minecraft 26.2. For another version, say so and check
any key whose path you are not sure still exists.
