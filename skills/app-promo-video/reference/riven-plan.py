"""Edit plan of the Riven Launcher teaser (1.1.0, long cut: takes a + b, BARS=36), read by render.py through PLAN.

The approved cut was shot with Russian captions; they are translated here. A plan sets TITLE, TAGLINE and LINK
for the intro and outro, and SEGMENTS — the scenes, built with take_seg() and B() from render.py.
"""

TITLE = "Riven Launcher"
TAGLINE = "The next-generation Minecraft launcher"
LINK = "github.com/BX-Team/Riven"

LATER = "≈ 1.5 minutes later"  # take A ends mid-download; VideCraft finished ~1.5 min later, off-camera
SEGMENTS = [
    take_seg(8, 16.5, [(B(8), 640, 360, 1.0), (B(9), 640, 360, 1.0), (B(10.2), 360, 250, 1.35), (B(11), 420, 220, 1.6),
                       (B(13.5), 430, 230, 1.6), (B(14.8), 470, 260, 1.45), (B(16), 900, 540, 1.35), (B(16.5), 880, 520, 1.3)],
             ("Modpacks from Modrinth", "thousands of ready-made packs for every taste")),
    take_seg(16.5, 26.5, [(B(17.5), 560, 630, 1.6), (B(23), 560, 630, 1.6), (B(24.5), 640, 370, 1.05), (B(26.5), 520, 320, 1.1)],
             ("Installed in seconds", "Vanilla Reimagined · 27 mods")),
    take_seg(26.5, 45, [(B(27.5), 640, 360, 1.0), (B(28.6), 420, 230, 1.35), (B(30.3), 500, 260, 1.3), (B(31.3), 880, 500, 1.2),
                        (B(32.5), 800, 300, 1.12), (B(33.4), 1000, 210, 1.35), (B(35), 390, 370, 1.35), (B(38), 400, 400, 1.35),
                        (B(39.3), 800, 560, 1.3), (B(41.3), 780, 560, 1.28), (B(42.8), 900, 230, 1.35), (B(44.3), 960, 240, 1.45),
                        (B(45), 900, 260, 1.3)],
             ("Your own pack", "any version and loader, mods from Modrinth — switch any of them off")),
    take_seg(45, 63.5, [(B(45.8), 640, 360, 1.0), (B(47), 420, 220, 1.4), (B(48), 420, 215, 1.6), (B(54), 480, 215, 1.6),
                        (B(56.5), 600, 240, 1.45), (B(59), 900, 300, 1.35), (B(61.3), 960, 320, 1.45), (B(62.6), 960, 450, 1.25)],
             ("Import a pack", "by link or from a file: Modrinth, GitHub, .mrpack, packwiz, Prism Launcher")),
    take_seg(63.5, 72, [(B(64.5), 680, 400, 1.15), (B(66.5), 760, 420, 1.6), (B(72), 760, 420, 1.65)],
             ("Everything downloads itself", "mods, resource packs and shaders — no fiddling with files")),
    take_seg(72, 76, [(B(72), 740, 410, 1.45), (B(73.5), 720, 380, 1.15), (B(75.5), 720, 400, 1.15), (B(76), 720, 400, 1.2)],
             ("Hundreds of mods in one list", "VideCraft: Create · 335 mods"),
             take=1, first=72, skip_label=LATER),
    take_seg(76, 82, [(B(76.7), 920, 240, 1.6), (B(80.8), 980, 240, 1.6), (B(82), 640, 370, 1.05)],
             ("All in one window", "resource packs · shaders · configs · logs"), take=1, first=72),
    take_seg(82, 98, [(B(83), 640, 370, 1.02), (B(87.8), 660, 380, 1.1), (B(89.3), 800, 280, 1.35), (B(91.5), 760, 330, 1.2),
                       (B(93.5), 800, 280, 1.35), (B(95.5), 680, 380, 1.12), (B(98), 640, 360, 1.0)],
             ("A theme for every taste", "Graphite · Night · Moss · Ember · Day · Paper"), take=1, first=72),
    take_seg(98, 110.5, [(B(99), 640, 360, 1.0), (B(100.5), 330, 300, 1.35), (B(103.5), 330, 280, 1.35), (B(105.1), 700, 260, 1.25),
                          (B(107), 620, 340, 1.15), (B(108.5), 640, 360, 1.05), (B(110.5), 640, 360, 1.05)],
             ("Developer mode", "a simple way to build your own packs — now IDE-style"), take=1, first=72),
    # freezes on the pressed Play button: the sandbox has no account tokens, and ~40 ms after the click
    # a "needs to sign in" message appears — find that frame again whenever the take changes
    take_seg(110.5, 124, [(B(111.5), 400, 330, 1.15), (B(113.8), 600, 360, 1.15), (B(115.6), 560, 470, 1.4), (B(118.5), 560, 480, 1.45),
                          (B(120.3), 480, 300, 1.12), (B(121.8), 980, 590, 1.35), (B(123.3), 1040, 630, 1.5), (B(124), 1060, 640, 1.55)],
             ("Java and memory", "the right Java downloads itself, memory is one slider"),
             hold=float(os.environ.get("HOLD", "40.64")), take=1, first=72),
]
