# Promotion validation

Campaign publications have not started. No social accounts were modified, no
messages were sent, and no directory submissions were made. Local evidence under
`dist/promotion/` is ignored by Git.

## Initial observations

Capture the first metrics snapshot after the v0.1.0 release and before any
promotion:

```bash
python3 docs/promotion/capture-metrics.py
```

Record the star and fork counts, the release asset IDs with their initial
download counts, and the traffic window here. Treat downloads and clones from
release verification and isolated install checks as validation activity, not
campaign adoption.

| Measure | Initial value | Captured |
|---|---|---|
| Stars / forks | Pending | Pending |
| Traffic window views / unique visitors | Pending | Pending |
| Release assets and downloads | Pending | Pending |

## Pre-release checks

Completed on October 19, 2026 against the local build:

- `npm run check`, `npm test`, and `npm run test:package` passed.
- `python3 scripts/build-audio.py --check` verified all 20 clips. Each built
  clip was transcribed with whisper.cpp to confirm the intended line, and
  measured at -16 LUFS integrated, within 0.8 LU.
- `python3 scripts/check-pet.py` reported the pet as not bundled, as intended.
- `python3 scripts/build-assets.py --check` matched committed preview pixels.
- A local build of the site was checked in Chromium at 1440 x 900 and 390 x 844,
  in both themes and with reduced motion: no horizontal overflow, fonts loaded,
  no console errors, and clip playback drove the oscilloscope (static envelope
  under reduced motion).
- Both promotional MP4s were inspected with FFprobe: 24 and 12 seconds,
  1080 x 1080 H.264 with AAC audio.

## v0.2.0 pet checks

Completed on October 21, 2026 against the local build:

- All contributor checks above passed again, and `check-pet.py` validated the
  bundled atlas (73 occupied and 15 transparent cells) and confirmed the web
  atlas decodes to exactly its first nine rows.
- `build-assets.py --check` matched committed pixels for the new pet GIFs,
  banner, and social card. `package-release.py` produced the pet ZIPs and web
  atlas alongside the existing assets.
- The local site build was checked in Chromium at 1440 x 900 (Day) and
  390 x 844 (Night): no horizontal overflow and no console errors. The hero
  robot switched to the blocked animation for the destructive cue, look
  direction buttons selected the expected atlas cells, and reduced motion
  froze the animation and disabled the pause control.
- The three promotional MP4s were inspected with FFprobe: 24, 12, and 16
  seconds at 1080 x 1080; the pet preview has no audio track by design.

## Remaining native checks

The following have not been verified by automated, package, or browser checks:

- Physical speaker output from an actual Claude Code approval request.
- The destructive-command cue from an actual Claude Code `rm -rf` approval.
- Physical speaker output from an actual trusted Codex approval request.
- End-to-end native behavior on Linux or Windows.
- The published Pages site (only a local build has been checked).
- The local pet bundle rendered and animated by Codex desktop.
- The local pet in a graphics-capable Codex CLI terminal via `/pets Johnny 5`.
- An account pet upload of `agent-johnny5-pet-web.webp`.

The committed MP4s are labeled illustrated previews, not proof of those checks.
Before publishing a claim of native behavior personally observed, complete the
[capture script](demos.md) and record host/version, OS, event, and result here.

| Check | Host/version | OS | Event/result | Evidence |
|---|---|---|---|---|
| Claude physical approval cue | Pending | Pending | Pending | Pending |
| Claude destructive-command cue | Pending | Pending | Pending | Pending |
| Codex trusted physical approval cue | Pending | Pending | Pending | Pending |
| Codex desktop native pet | Pending | Pending | Pending | Pending |
| Codex CLI terminal pet | Pending | Pending | Pending | Pending |
