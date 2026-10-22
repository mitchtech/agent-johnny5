# Johnny 5 pet

The sound plugin and the Codex pet are independent. The local v2 pet has nine
animations and sixteen clockwise look directions. The host controls its
animations without additional hooks or a daemon. Preview every animation and
look direction on the [project site](https://mitchtech.github.io/agent-johnny5/#pet).

## Installation

The quickest route needs no Node.js, Python, audio player, or sound plugin:

1. Download [agent-johnny5-pet.zip](https://github.com/mitchtech/agent-johnny5/releases/latest/download/agent-johnny5-pet.zip)
   from v0.2.0 or a later release.
2. Extract its `johnny5` folder into `~/.codex/pets/`, or `<CODEX_HOME>/pets/`
   when `CODEX_HOME` is configured.
3. Refresh the host's pet picker and choose Johnny 5.

From this source checkout:

```bash
node scripts/johnny5.mjs pet install
node scripts/johnny5.mjs doctor --pet
```

With a CLI package that includes the artwork, use `agent-johnny5 pet install`
and `agent-johnny5 doctor --pet`. Older packages without artwork continue to
report `not-bundled` without changing local pet files.

Releases from v0.2.0 include `agent-johnny5-pet.zip` and a versioned copy for
manual installation. The extracted layout is:

```text
~/.codex/pets/johnny5/
  pet.json
  spritesheet.webp
  LICENSE.txt
  NOTICE.md
```

If `CODEX_HOME` is configured, use `<CODEX_HOME>/pets/johnny5/` instead. Manual
installation needs no Node.js, Python, audio player, or sound plugin. Preserve
a backup before replacing a different existing pet.

## Selection and support

Installation never changes the selected pet or other host settings. The local
bundle targets Codex sprite version 2.

| Surface | Local Johnny 5 pet | Selection |
|---|---|---|
| Desktop host with custom pet picker | Compatible v2 bundle | Refresh the pet picker and choose Johnny 5 |
| Interactive Codex CLI | Compatible graphics terminal required | `/pets Johnny 5`; `/pets` opens the picker |
| Codex IDE extension | No native picker or overlay | Use the desktop host or CLI |
| Claude Code | No native integration provided here | Sound plugin only |
| Gemini CLI | No native integration provided here | Sound extension only |
| Other agents | No native integration provided here | Check the host's own pet format |
| ChatGPT web | Separate account upload and compatibility rules | Use the [web atlas](#web-upload) |

Terminal pets require iTerm2 3.6+, Kitty graphics, or Sixel support and are not
available inside tmux or Zellij. `/pets off` hides a terminal pet. Local custom
pets do not automatically sync to the web.
[Official pet documentation](https://learn.chatgpt.com/docs/pets)

Refresh the installed host's pet picker rather than editing a selected avatar
ID in its configuration. The host drives activity states; the sound plugin
drives its own event cues.

## Web upload

Download [agent-johnny5-pet-web.webp](https://github.com/mitchtech/agent-johnny5/releases/latest/download/agent-johnny5-pet-web.webp)
from v0.2.0 or a later release, or from the [project site](https://mitchtech.github.io/agent-johnny5/exports/agent-johnny5-pet-web.webp).
It is a transparent 1536 x 1872 lossless WebP of about 1.7 MB, well below the
20 MiB upload limit, containing the nine animation rows. The two look-direction
rows are omitted for the web format.

Upload it through the web pet creation flow and retain the artwork attribution
and [CC BY 4.0 license](../pets/johnny5/LICENSE.txt) when sharing it. This upload
creates a separate account pet; it does not install or select the local Codex
bundle. Structural compatibility is validated, but an upload of this exact file
has not been verified.

## Installer behavior

The CLI copies the four bundle files and a local ownership
record into `$CODEX_HOME/pets/johnny5` (default `~/.codex/pets/johnny5`). It
leaves avatar selection, agent settings, hooks, and audio configuration
unchanged. An identical install is a no-op. A matching manual installation
remains unmanaged.

Different files require `agent-johnny5 pet install --replace`. The previous entire
directory is renamed to `johnny5.backup-<unique-suffix>` next to the new
installation. Files and symbolic links at the target directory path are never
replaced.

Status reports `not-bundled`, `not-installed`, `matching`, `modified`, or
`conflict`. Uninstall removes only an unchanged CLI-owned installation, even
when the current package has no art. It refuses edited files, unknown additional
files, symbolic links, and unmanaged installations.

```bash
agent-johnny5 pet status --json
agent-johnny5 pet uninstall
```

## Artwork and validation

The active atlas lives in `pets/johnny5/spritesheet.webp`. The original PNG
is preserved byte-for-byte in `assets/original/johnny5`. Lossless WebP encoding
preserves every decoded RGBA pixel. Source and active hashes are recorded in
`assets/pet-revision.json` and the [artwork notice](../pets/johnny5/NOTICE.md).
The artwork license applies to the contributor's rights; third-party character
rights remain with their respective owners.

`python3 scripts/check-pet.py` validates the 1536 x 2288 RGBA WebP, all 73
occupied cells, the 15 transparent cells, transparent-pixel RGB cleanup, and
that the web atlas decodes to exactly the first nine rows of the active atlas.
`python3 scripts/export-pet-web.py` regenerates that atlas and records its hash
in `assets/pet-revision.json`.
`python3 scripts/package-pet.py` builds a reproducible four-file pet ZIP;
release packaging includes it automatically.

The creation workflow reviewed all nine animation states and sixteen gaze
directions, including an independent blind direction check. Repository tests
exercise real-art installation and package diagnostics, with small fixtures
for conflicts and missing-art behavior. Native desktop and terminal rendering
have not been independently verified for this bundle.
