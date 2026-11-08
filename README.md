<div align="center">

# claude-skills

A small collection of the skills we use with Claude and other agents at BX Team: two that know how to run a
Minecraft server well, and two that let an agent run a desktop app off-screen and use it like a person would, to
test what it is building or to record a promo video of it.

[![Chat on Discord](https://cdn.jsdelivr.net/npm/@intergrav/devins-badges@3/assets/cozy/social/discord-plural_vector.svg)](https://discord.gg/qNyybSSPm5)
[![documentation](https://cdn.jsdelivr.net/npm/@intergrav/devins-badges@3/assets/cozy/documentation/website_vector.svg)](https://bxteam.org/tools#skills)
[![github](https://cdn.jsdelivr.net/npm/@intergrav/devins-badges@3/assets/cozy/available/github_vector.svg)](https://github.com/BX-Team/claude-skills)

</div>

## ⚙️ Features

| Plugin | Skill | What it does |
| ------ | ----- | ------------ |
| `minecraft-server` | [`jvm-flags`](skills/jvm-flags) | Picks a flag set for your Java, JVM, OS, CPU and heap, explains every flag and writes `start.sh`, `start.bat` or a panel line. Also reads a failed start and says which flag broke it. |
| `minecraft-server` | [`server-config`](skills/server-config) | Tunes `server.properties`, `bukkit.yml`, `spigot.yml` and the Paper, Purpur and DivineMC configs for your kind of server, and reviews a config you already have. |
| `desktop-apps` | [`app-driver`](skills/app-driver) | Starts a GUI app (gpui, GTK, Qt, any Wayland client) in a headless compositor and drives it with real mouse moves, clicks, drags, scrolling, typing and screenshots. The agent checks its own UI changes in the actual app instead of asking you to click through them. |
| `desktop-apps` | [`app-promo-video`](skills/app-promo-video) | Turns a real, scripted session in your app into a promo video: one take recorded in real time, a smooth camera, captions, a logo intro and outro, and generated music. |

The `desktop-apps` skills need Linux and [Nix](https://nixos.org/download): every tool they use (cage, grim,
wf-recorder, ffmpeg, a Python with numpy and Pillow, the Rust input helper) is built through `nix build` on first
use, and nothing appears on your screen while they work.

## 📦 Installation

### Claude Code

```
/plugin marketplace add BX-Team/claude-skills
/plugin install minecraft-server@bx-team
/plugin install desktop-apps@bx-team
```

Install either plugin or both. They update with this repository.

### Claude apps

The `minecraft-server` skills can be downloaded as zips from [bxteam.org/tools](https://bxteam.org/tools#skills).
In Claude, open [Customize → Skills](https://claude.ai/customize/skills), choose *Create skill* and upload one.
The `desktop-apps` skills run programs on your machine, so they only make sense in Claude Code.

### Other agents

Each skill is a folder with a `SKILL.md`; copy `skills/<name>` wherever your agent loads skills from. `app-promo-video`
expects `app-driver` next to it.

## 🚀 Getting started

Ask in plain words, the skills pick themselves up:

- "Which JVM flags should my 16 GB Paper server on Java 21 use?"
- "Here is my `paper-world-defaults.yml`, why does the server lag with 40 players?"
- "Build the app and check that the settings dialog now remembers the theme."
- "Make a 45-second teaser of the launcher: installing a modpack, the themes, the developer mode."

## 🤝 Contributing

See [CONTRIBUTING.md](https://github.com/BX-Team/.github/blob/master/CONTRIBUTING.md). A change to a skill is
checked by using it: say in the pull request what you asked and what it did.

## ⚖️ License

This project is licensed under the GNU Affero General Public License v3.0 — see the [LICENSE](LICENSE) file for details.

## 💛 Credits

- [Aikar's flags](https://docs.papermc.io/paper/aikars-flags), [MeowIce](https://github.com/MeowIce/meowice-flags), [brucethemoose](https://github.com/brucethemoose/Minecraft-Performance-Flags-Benchmarks) and [hilltty](https://github.com/hilltty/hilltty-flags), the flag sets `jvm-flags` builds on.
- [cage](https://github.com/cage-kiosk/cage), [grim](https://sr.ht/~emersion/grim/) and [wf-recorder](https://github.com/ammen99/wf-recorder), which `app-driver` runs the app in, screenshots and records.
