# Response sheet

Use these as factual starting points. Answer the person's question directly
and link only the relevant documentation.

**What is Agent Johnny 5?** A free sound-notification plugin for coding agents
that plays Johnny 5's lines from *Short Circuit*. Native sounds support Claude
Code, Codex, and Gemini CLI; other tools can call the shared event interface.
It is a sibling of Agent Navi and shares its runtime design.

**Is it constantly talking?** Session, prompt, and attention events are enabled
by default where supported. Use the attention preset to silence session and
prompt cues, mute individual events, or mute everything. Completion, error,
compaction, and session-end cues are off by default.

**What is the "No disassemble" alarm?** When an approval's command matches a
short list of destructive patterns (recursive force deletes, force pushes, hard
resets, `git clean -f`, dropped or truncated tables, `mkfs`, `dd of=`,
`chmod -R 777`, and PowerShell recursive force removal), the approval plays
"No disassemble, Number Five!" instead of the ordinary cue.

**Is the alarm a safety feature?** No. It is a louder sound. It never blocks or
approves anything, and an indirect or obfuscated command gets the ordinary cue.
Keep your normal permission settings.

**Does it read my commands?** Only to set a yes/no flag inside the short-lived
hook process. The command is never passed to the playback worker, logged, or
stored. Local playback state stores hashed identifiers and timestamps only.

**What are the easter eggs?** About 2% of session, prompt, ready, and completion
cues are replaced by a bonus line ("Hey, laser lips...", "Nice software", or
"Attractive"). They never replace approval, question, error, or alarm cues.
`agent-johnny5 mute easter-egg` turns them off.

**Does it send telemetry?** No. It runs locally without runtime telemetry, and
the site loads no analytics. GitHub and social platforms keep their own aggregate
metrics.

**Why do I hear nothing?** Check Node.js on the hook process's PATH, restart the
agent, verify the local audio player/device, and inspect the mute state. Codex
also requires hook trust review. Use `doctor` for diagnostics and
`preview need-input` for an explicit audio check.

**I hear a fairy and a robot.** Agent Navi is installed too. Disable one per
host; see the [install walkthrough](install.md#already-using-agent-navi).

**Will it play on my laptop from SSH, WSL, or a container?** Not automatically.
Audio plays where the hook runs. A working audio bridge must already exist if
the execution environment and speakers are on different machines.

**Do all hosts expose the same events?** No. Claude has question, idle, and
error mappings that Codex and Gemini lack. Completion is optional, not a task
success detector. See [compatibility](../compatibility.md).

**Is there a Codex pet?** Yes, since v0.2.0. Johnny 5 has nine animations and
sixteen look directions. Download `agent-johnny5-pet.zip` from the latest
release, extract the `johnny5` folder into `~/.codex/pets/`, and choose Johnny 5
in the pet picker (or `/pets Johnny 5` in a graphics-capable Codex CLI terminal).
It installs independently of the sounds. See [pets](../pets.md).

**Does the pet work in Claude Code or Gemini?** No. Those hosts get the sounds;
native pets are a Codex feature. For a ChatGPT account pet, upload the separate
nine-row web atlas described in [pets](../pets.md#web-upload).

**Who made the pet art, and can I reuse it?** Michael created it with Codex's
built-in image generation; it was not extracted from film frames. The
contributor's rights are licensed CC BY 4.0, and character rights remain with
their owners. See the [artwork notice](../../pets/johnny5/NOTICE.md).

**Is this official Short Circuit software?** No. Character rights and trademarks
remain with their owners. Code and configuration use MIT; the bundled audio is
excluded, and its provenance notice is not permission from the rights holders.
See the [audio notice](../../audio/NOTICE.md).

**Can I use my own audio?** Yes. Configure your own audio directory with a
`<clip>.wav` for every name in `agent-johnny5 list`, using 16-bit PCM WAV for
player compatibility. See [configuration](../../README.md#configuration).

**Was every platform physically tested?** CI exercises Node 22/24 on macOS,
Linux, and Windows with simulated players. Package tests exercise installed
bundles. Neither proves physical speaker output on every surface. Current
campaign checks are recorded in [validation](validation.md).
