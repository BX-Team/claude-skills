# claude-skills

BX Team's agent skills, served as a Claude Code plugin marketplace. Each skill is a folder under `skills/` with a
`SKILL.md` and the files it reads or runs; `.claude-plugin/marketplace.json` groups them into the `minecraft-server`
and `desktop-apps` plugins. There is no build and no package manager here.

## Architecture

| Path | Responsibility |
| ---- | -------------- |
| `skills/jvm-flags` | JVM start flags for Minecraft servers and proxies. |
| `skills/server-config` | Paper, Purpur and DivineMC configuration tuning and review. |
| `skills/app-driver` | Runs a GUI app in headless cage and drives it through `driver.py` and the `vptr` Rust helper. |
| `skills/app-promo-video` | Promo videos from a real-time take recorded through `app-driver`: schedule, music, render. |

### Decisions that are settled

- **The flags skill and the site's flags generator are one source of truth in two places.** `jvm-flags`'s
  `reference/presets.md` and `apps/web/app/lib/flags/` in [BX-Team/code](https://github.com/BX-Team/code) carry the
  same sets and conditions. Change one, change the other.
- **bxteam.org builds the claude.ai zips from this repository at download time** (`apps/web/app/lib/skills.ts`
  in BX-Team/code reads the tree of `master`). A renamed skill folder breaks its download button.
- **`app-promo-video` does not copy the driver.** It runs `../app-driver/scripts`, so the two skills ship together
  in one plugin.
- **A promo take is recorded in real time.** Time-warping a loose take onto beats was tried and rejected because
  the speed changes showed; it stays only as the documented fallback.
- **The tools come from Nix.** `tools.sh` builds every binary through `nixpkgs`, so nothing is assumed installed.

## Commands

```bash
eval "$(skills/app-driver/scripts/tools.sh)"   # build the driver's tools and vptr
python3 -c 'import ast,sys; [ast.parse(open(f).read()) for f in sys.argv[1:]]' skills/*/scripts/*.py
```

Nothing runs on pull requests. A skill is verified by using it: say in the pull request what you asked and what
it did.

## Code Guidelines

### Comments

- NO file-header banners and NO divider comments (`// --- helpers ---`). Group code with functions, not comment art.
- Add an inline comment only where the code is genuinely non-obvious — a real footgun, a wire-format quirk, a
  reason a thing is done backwards. Then keep it to a line or two.
- Don't narrate the obvious. If a comment restates the next line, delete it.
- Doc comments on public items are fine and should say *why*, in one or two sentences.

### Style

- Match the surrounding code: follow the idiom already in the file you're editing.
- A `SKILL.md` description says what the skill does and when to use it, in the words a user would ask with. It is
  what decides whether the skill triggers; keep it under 1024 characters.
- A skill reads its references by relative path from its own folder; never by an absolute path on one machine.

### Language of user-facing strings

English, everywhere: the skills, their references and the captions in example plans.

### Gotchas

- `vptr` embeds `keymap.xkb` at compile time. `tools.sh` generates it before building; a bare `cargo build`
  without it fails.
- gpui ignores `wlrctl` and plain wheel `axis` events; see `skills/app-driver/SKILL.md` → Pitfalls before
  replacing any part of the input path.

### Testing

There is no test suite. Exercise a changed skill on a real request; for `app-driver`, start an app and take a shot.

## Bash Guidelines

- Don't pipe output through `head`/`tail`/`less` to truncate — use tool-native flags. Read the full output.
- Don't create scratch files (scripts, notes) unless asked.
- When given failures, just fix them — don't argue about who introduced them.
