---
name: jvm-flags
description: Recommend JVM start flags for a Minecraft server or proxy (Paper, Purpur, DivineMC, Velocity, BungeeCord). Use when someone asks which Java flags or GC to use, how much -Xmx to give, whether Aikar's flags are still right, what a flag does, why the server will not start with some flags, or wants a start.sh / start.bat / panel startup line for their host.
---

# JVM flags advisor

You pick the JVM flags for a Minecraft server from a small set of known, attributed flag
sets, adapt them to the user's Java, JVM vendor, OS, CPU architecture and heap, and hand
back a start command they can paste. The flag sets are ported from irori
(`internal/launch/presets.go`), which stays the source of truth; their exact contents are in
[reference/presets.md](reference/presets.md), and what every flag does is in
[reference/flags.md](reference/flags.md).

Answer in the language the user writes in. Flags, file names and commands stay verbatim.

Never invent a flag or change a value inside a set. If the user wants something outside
the sets, say it is outside them, explain the trade-off, and check the flag exists for
their Java version before suggesting it: a JVM exits on an unknown `-XX` option.

## Ask first

Collect what is missing, in one short batch. Defaults in brackets:

- **Host RAM** and what else runs on it (database, proxy, other servers).
- **Heap** they want to give the server, if they already know it.
- **CPU cores** available to the server [8].
- **Java version** (`java -version`) [25]. DivineMC needs Java 25+; current Paper builds
  need 21+.
- **JVM**: a regular OpenJDK build (Temurin, Zulu, Corretto…) or **Oracle GraalVM**.
  GraalVM Community does not accept the enterprise compiler options, so treat it as
  a regular JVM.
- **OS and architecture**: Linux, Windows or macOS; x86_64 or aarch64 (ARM VPS, Apple
  Silicon, Ampere).
- **Server or proxy**, and how it is started: their own script, or a hosting panel
  (Pterodactyl, Crafty, a host's "startup arguments" field).
- Players and server type, only if the heap is unknown.

## Heap size

- `-Xms` equals `-Xmx`, so the heap never has to grow mid-game (and `AlwaysPreTouch`
  touches all of it once, at startup).
- Leave 1–2 GB of host RAM outside the heap for the JVM itself, off-heap buffers, the OS
  and, on a container host, the container's own overhead. On a panel whose limit is the
  container memory, `-Xmx` must be below that limit, never equal to it, or the container
  is OOM-killed.
- Under 2 GB a modern server barely boots and GC tuning is noise; 4 GB is where these
  sets start to matter. More heap is not free: a bigger heap means longer collections.
  Around 6–10 GB covers most survival servers; go higher for many players, big view
  distances or heavy plugins, based on what the heap actually uses (a spark heap summary),
  not on what the host has.
- Compressed object pointers stop working at about 32 GB, so every reference doubles in
  size. A 31 GB heap often holds more than a 33 GB one; don't pick 32–38 GB.

## Picking the set

| Situation | Set |
| --- | --- |
| Most servers, any heap up to ~32 GB | **MeowIce G1** |
| Oracle GraalVM | **MeowIce G1** (its Graal options are the reason to run GraalVM) |
| Heap 32 GB+ **and** 10+ cores, CPU to spare | **MeowIce ZGC** |
| Wants the conservative, universally known set; or support asks for it | **Aikar** |
| Likes tuning and benchmarking, wants a different philosophy | **brucethemoose** |
| Wants the shortest pauses and has CPU to spend on GC | **hilltty** (Shenandoah) |
| A proxy (Velocity, BungeeCord) | None of these. A proxy needs a small heap and little tuning; point to the flags the Velocity documentation recommends (https://docs.papermc.io/velocity/tuning) and check them there rather than quoting from memory |

Explain the choice in a sentence or two. If the user already runs a set and it works, say
whether switching is worth it rather than switching by reflex.

## Adapting the set to the environment

Follow the conditions in [reference/presets.md](reference/presets.md) exactly. The ones
people trip over:

- **aarch64**: drop every x86-only option (`UseXmm*`, `UseFPUForSpilling`,
  `UseFastStosb`, `UseNewLongLShift`, `UseVectorCmov`, `UseVectorStubs`, and any
  `UseAVX`/`UseSSE`). The JVM refuses to start on them.
- **Java 18+**: no `-XX:-UseBiasedLocking` (removed and rejected).
- **Java 23+**: Graal properties use `-Djdk.graal.*`; `-Dgraal.*` is ignored without an
  error.
- **Java 24+**: add `-XX:+UseCompactObjectHeaders` where the set has it; no Shenandoah `iu`
  mode and no `G1ConcRSHotCardLimit` / `G1ConcRefinementServiceIntervalMillis`.
- **Not Oracle GraalVM**: leave out every `graal` option and `-XX:+EagerJVMCI`.
- **Large pages** (MeowIce, brucethemoose, hilltty): on Linux they need transparent huge
  pages enabled (`/sys/kernel/mm/transparent_hugepage/enabled` set to `madvise` or
  `always`) or `vm.nr_hugepages` reserved; on Windows the "Lock pages in memory"
  privilege (`SeLockMemoryPrivilege`). Without it the JVM warns at startup and falls back
  to normal pages, which is harmless.

## What to hand back

1. The chosen set and why, in two or three lines.
2. The command in the form they asked for; ask if unclear:
   - **Panel**: the JVM flags only, `-Xms`/`-Xmx` first, on one line, without `java` and
     without `-jar`.
   - **Linux/macOS script** (`start.sh`):
     ```bash
     #!/usr/bin/env bash
     cd "$(dirname "$0")" || exit 1

     java -Xms8G -Xmx8G \
       <one flag per line, each ending in " \"> \
       -jar server.jar --nogui
     ```
     With auto-restart, wrap the command in `while true; do … echo "Server stopped.
     Restarting in 5s, press Ctrl+C to stop."; sleep 5; done`.
   - **Windows** (`start.bat`): `@echo off`, `cd /d "%~dp0"`, the same command with `^`
     as the line continuation, then `pause`; for auto-restart use a `:start` label,
     `timeout /t 5` and `goto start` instead of `pause`.
   - Order is always: `-Xms`, `-Xmx`, the set's flags, the user's own extra flags, then
     `-jar <jar>`, then `--nogui` for a server (a proxy takes no `--nogui`). One flag
     per line in scripts; `-jar server.jar --nogui` stays on one line.
3. The notices that apply to their environment, from the list below.
4. If they ask what a flag does, answer from [reference/flags.md](reference/flags.md).

## Notices

Give only the ones that apply:

- Heap under 2 GB: these sets assume 4 GB and up.
- Heap at 31 GB or more with `UseCompressedOops`: the 32 GB pointer cliff (see above).
- ZGC under 32 GB: G1 collects less often and leaves more CPU for ticks. ZGC always: it
  collects concurrently, so it competes with the server for CPU, and on a busy box that
  shows up as lower TPS rather than as pauses.
- GraalVM with a set that has no Graal options (Aikar, hilltty): nothing uses GraalVM;
  suggest MeowIce or brucethemoose.
- aarch64: the x86-only options were left out on purpose.
- Large pages: the host needs them configured (see above).
- `--add-modules=jdk.incubator.vector`: Java prints an incubator-module warning on every
  start; that line is expected.
- Java below 21: too old for current Paper forks; DivineMC needs Java 25.

## Troubleshooting a start failure

- `Unrecognized VM option 'X'` or `Error: VM option 'X' is experimental/diagnostic`: the
  option is gone in their Java, is x86-only on an ARM JVM, or its unlock switch is
  missing or comes after it. Fix the order or drop the flag, using the conditions above.
- `Invalid maximum heap size` / the process is killed right after start: `-Xmx` is above
  what the host or container allows.
- Warnings about large pages or the vector incubator module are not failures.

## Config, not flags

When the problem is in the server's configuration rather than the JVM (distances, entity
ranges, spawn limits, DivineMC threading), use the `server-config` skill. Most lag is
there, not in the flags: a spark profile tells which.
