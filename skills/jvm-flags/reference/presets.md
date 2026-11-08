# Flag sets

Exact flags, in order, for each set. Conditions use the environment from SKILL.md:
`java` (feature release), `graal` (Oracle GraalVM or not), `os`, `arch`, `heap` (the `-Xmx`
value). Emit a conditional flag only when its condition holds.

Shared building blocks:

- **vector**: `--add-modules=jdk.incubator.vector` (Java 17+).
- **unlock**: `-XX:+UnlockExperimentalVMOptions -XX:+UnlockDiagnosticVMOptions`.
- **largePages**: `-XX:+UseTransparentHugePages` *(Linux only)*, then
  `-XX:LargePageSizeInBytes=2M -XX:+UseLargePages`.
- **graal(name, value)**: `-Djdk.graal.<name>=<value>` on Java 23+, `-Dgraal.<name>=<value>`
  before it. The old prefix is ignored silently on 23+.
- **x86 intrinsics** *(x86_64 only; an aarch64 JVM refuses to start on any of them)*:
  `-XX:+UseFPUForSpilling -XX:+UseFastStosb -XX:+UseNewLongLShift -XX:+UseVectorCmov
  -XX:+UseXMMForArrayCopy -XX:+UseXmmI2D -XX:+UseXmmI2F -XX:+UseXmmLoadAndClearUpper
  -XX:+UseXmmRegToRegMoveAll`.

## Aikar's flags

By Aikar, https://docs.papermc.io/paper/aikars-flags/. G1, the long-standing default for
Paper and its forks. "Big" means a heap of 12 GB or more.

```
-XX:+UseG1GC
-XX:+ParallelRefProcEnabled
-XX:MaxGCPauseMillis=200
-XX:+UnlockExperimentalVMOptions
-XX:+DisableExplicitGC
-XX:+AlwaysPreTouch
-XX:G1NewSizePercent=30            (40 when big)
-XX:G1MaxNewSizePercent=40         (50 when big)
-XX:G1HeapRegionSize=8M            (16M when big)
-XX:G1ReservePercent=20            (15 when big)
-XX:G1HeapWastePercent=5
-XX:G1MixedGCCountTarget=4
-XX:InitiatingHeapOccupancyPercent=15   (20 when big)
-XX:G1MixedGCLiveThresholdPercent=90
-XX:G1RSetUpdatingPauseTimePercent=5
-XX:SurvivorRatio=32
-XX:+PerfDisableSharedMem
-XX:MaxTenuringThreshold=1
-Dusing.aikars.flags=https://mcflags.emc.gs
-Daikars.new.flags=true
```

## MeowIce's flags, G1

By MeowIce, https://github.com/MeowIce/meowice-flags. Aikar's G1 plus modern JIT and
intrinsic tuning; best on GraalVM.

```
vector
unlock
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:+DisableExplicitGC
-XX:+AlwaysPreTouch
-XX:G1NewSizePercent=28
-XX:G1MaxNewSizePercent=50
-XX:G1HeapRegionSize=16M
-XX:G1ReservePercent=15
-XX:G1MixedGCCountTarget=3
-XX:InitiatingHeapOccupancyPercent=20
-XX:G1MixedGCLiveThresholdPercent=90
-XX:SurvivorRatio=32
-XX:G1HeapWastePercent=5
-XX:+PerfDisableSharedMem
-XX:G1SATBBufferEnqueueingThresholdPercent=30
-XX:G1ConcMarkStepDurationMillis=5
-XX:G1RSetUpdatingPauseTimePercent=0
-XX:AllocatePrefetchStyle=3
meowice common
```

## MeowIce's flags, ZGC

Same author. For 32 GB+ heaps on 10+ cores only.

```
vector
unlock
-XX:+UseZGC
-XX:-ZProactive
-XX:+DisableExplicitGC
-XX:+AlwaysPreTouch
-XX:+PerfDisableSharedMem
-XX:SoftMaxHeapSize=<heap − 2048>M     (only when heap > 2048 MB)
-XX:AllocatePrefetchStyle=1
meowice common
```

### meowice common

```
-XX:+UseNUMA
-XX:-DontCompileHugeMethods
-XX:MaxNodeLimit=240000
-XX:NodeLimitFudgeFactor=8000
-XX:ReservedCodeCacheSize=400M
-XX:NonNMethodCodeHeapSize=12M
-XX:ProfiledCodeHeapSize=194M
-XX:NonProfiledCodeHeapSize=194M
-XX:NmethodSweepActivity=1
-XX:+UseCriticalJavaThreadPriority
-XX:+AlwaysActAsServerClassMachine
largePages
-XX:+EagerJVMCI
-XX:+UseStringDeduplication
-XX:+UseAES
-XX:+UseAESIntrinsics
-XX:+UseFMA
-XX:+UseLoopPredicate
-XX:+RangeCheckElimination
-XX:+OptimizeStringConcat
-XX:+UseCompressedOops
-XX:+UseThreadPriorities
-XX:+OmitStackTraceInFastThrow
-XX:+RewriteBytecodes
-XX:+RewriteFrequentPairs
-XX:+EliminateLocks
-XX:+DoEscapeAnalysis
-XX:+AlignVector
-XX:+OptimizeFill
-XX:+EnableVectorSupport
-XX:+UseCharacterCompareIntrinsics
-XX:+UseCopySignIntrinsic
-XX:+UseFastJNIAccessors
-XX:+UseInlineCaches
-XX:+SegmentedCodeCache
x86 intrinsics                        (x86_64 only)
-XX:+UseVectorStubs                   (x86_64 only)
-XX:+UseCompactObjectHeaders          (Java 24+)
-Djdk.nio.maxCachedBufferSize=262144
Oracle GraalVM only, each through graal(name, value):
  UsePriorityInlining=true, Vectorization=true, OptDuplication=true,
  DetectInvertedLoopsAsCounted=true, LoopInversion=true, VectorizeHashes=true,
  EnterprisePartialUnroll=true, VectorizeSIMD=true, StripMineNonCountedLoops=true,
  SpeculativeGuardMovement=true, TuneInlinerExploration=1, LoopRotation=true,
  CompilerConfiguration=enterprise
```

## brucethemoose's flags

By brucethemoose, https://github.com/brucethemoose/Minecraft-Performance-Flags-Benchmarks.
Individually benchmarked base flags with the server G1 set.

```
unlock
-XX:+AlwaysActAsServerClassMachine
-XX:+AlwaysPreTouch
-XX:+DisableExplicitGC
-XX:+UseNUMA
-XX:NmethodSweepActivity=1
-XX:ReservedCodeCacheSize=400M
-XX:NonNMethodCodeHeapSize=12M
-XX:ProfiledCodeHeapSize=194M
-XX:NonProfiledCodeHeapSize=194M
-XX:-DontCompileHugeMethods
-XX:MaxNodeLimit=240000
-XX:NodeLimitFudgeFactor=8000
-XX:+PerfDisableSharedMem
-XX:+UseFastUnorderedTimeStamps
-XX:+UseCriticalJavaThreadPriority
-XX:ThreadPriorityPolicy=1
-XX:AllocatePrefetchStyle=3
-XX:+UseVectorCmov                    (x86_64 only)
-XX:+UseG1GC
-XX:MaxGCPauseMillis=130
-XX:G1NewSizePercent=28
-XX:G1HeapRegionSize=16M
-XX:G1ReservePercent=20
-XX:G1MixedGCCountTarget=3
-XX:InitiatingHeapOccupancyPercent=10
-XX:G1MixedGCLiveThresholdPercent=90
-XX:G1RSetUpdatingPauseTimePercent=0
-XX:SurvivorRatio=32
-XX:MaxTenuringThreshold=1
-XX:G1SATBBufferEnqueueingThresholdPercent=30
-XX:G1ConcMarkStepDurationMillis=5
-XX:G1ConcRSHotCardLimit=16                     (before Java 24)
-XX:G1ConcRefinementServiceIntervalMillis=150   (before Java 24)
largePages
Oracle GraalVM only: -XX:+EagerJVMCI, graal(TuneInlinerExploration, 1),
  graal(CompilerConfiguration, enterprise)
```

## hilltty's flags

By hilltty, https://github.com/hilltty/hilltty-flags. Shenandoah: short pauses at the cost
of CPU; a small set.

```
-XX:+UnlockExperimentalVMOptions
largePages
-XX:+UseShenandoahGC
-XX:ShenandoahGCMode=iu               (before Java 24; the mode was removed in 24)
-XX:+UseNUMA
-XX:+AlwaysPreTouch
-XX:+DisableExplicitGC
-XX:-UseBiasedLocking                 (before Java 18; rejected from 18 on)
-Dfile.encoding=UTF-8
```

## Sets that were deliberately dropped

- **etil2jz's flags**: unmaintained; Aikar plus intrinsics that MeowIce covers more
  carefully, and it hard-codes `-XX:UseAVX=3` without checking the CPU supports it.
- **Obydux's flags**: G1 for GraalVM, the niche MeowIce G1 already covers, Linux only.

If a user already runs one of these, it works; suggest moving to MeowIce G1.
