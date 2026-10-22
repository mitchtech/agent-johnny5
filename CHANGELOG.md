# Changelog

## 0.2.0 - 2026-10-21

The Johnny 5 Codex pet ships.

- Bundle the Johnny 5 v2 pet with nine animations and sixteen look directions, an artwork license and provenance, and a lossless WebP that preserves every original PNG pixel. Releases now attach `agent-johnny5-pet.zip`.
- Preserve the original PNG under `assets/original/johnny5` and exercise real-art installation while retaining manifest-only package coverage.
- Add a nine-row `agent-johnny5-pet-web.webp` for ChatGPT account pet uploads, derived by `scripts/export-pet-web.py` and checked against the active atlas.
- Showcase the pet on the site: the hero robot reacts to each clip, and a pet section previews every animation and look direction with ZIP, CLI, and web-atlas install paths. Add a native-pet column to the compatibility table, structured data, and refreshed sharing metadata.
- Add pet animation GIFs to the README, put the robot on the banner and social card, and add a captioned `pet-preview.mp4`. The sound and attention previews now show the robot reacting to each cue.

## 0.1.0 - 2026-10-19

First release, built on the Agent Navi v0.4.0 runtime.

- Play 20 Johnny 5 lines from *Short Circuit* for Claude Code, Codex, and Gemini CLI, plus a generic `play` interface for other agents.
- Map session start to "Number five is alive!" or "Hi", prompts to "Input!", "Yup", or "You got it", approvals to "Need input", questions to "I have questions", and idle notifications to "More input".
- Play "No disassemble, Number Five!" when an approval's command is destructive (`rm -rf`, force push, `git reset --hard`, `DROP TABLE`, and similar). Only a yes/no flag leaves the hook; the command is never stored.
- Add a configurable 2% easter egg ("Hey, laser lips...", "Nice software", "Attractive") limited to non-urgent cues, with `mute easter-egg`.
- Add optional `context_compacting` (PreCompact, Gemini PreCompress) and `session_ended` (SessionEnd) events for all three hosts, off by default.
- Record every clip's source, trim, and output hash in `audio/sources.json`, with a reproducible ffmpeg build and an offline `--check`; clips are loudness-matched at -16 LUFS.
- Ship the Codex pet installer, validation, and packaging with a manifest-only stub; `pet status` reports `not-bundled` until the art lands.
- Add a NOVA Robotics themed site with a live oscilloscope for every clip, waveform previews, and Day/Night themes.
- Publish the Pages site from the pushed commit until the first release exists.
