# Public post drafts

Owner review required before publishing. These drafts describe documented
behavior, not fabricated user results. Attach the matching captioned preview
from [demos.md](demos.md). Keep its preview label visible. Substitute a live clip
only after the native capture checklist passes. Recheck community rules and
flair on publication day. Use one primary destination per post.

## R1 - r/ClaudeCode weekly showcase

I built Agent Johnny 5, a free sound-notification plugin for Claude Code. It
plays Johnny 5's lines from *Short Circuit* when the agent needs you: "Need
input" for an approval, "I have questions" for a question, "More input" when
it is idle. If the approval is for `rm -rf`, a force push, or a hard reset, you
get "No disassemble, Number Five!" instead.

The attached clip is an illustrated sound preview, not a live hook recording.

Install from your terminal:

```bash
claude plugin marketplace add mitchtech/agent-johnny5
claude plugin install johnny5@agent-johnny5
```

It needs Node.js 22+ and local audio. Restart Claude Code after installation.
It runs locally with no runtime telemetry, and the hooks never approve or block
actions. The destructive-command alarm is a louder cue, not a safety check; the
command never leaves the hook process. If the session and prompt cues are too
much, ask "Johnny 5, use the attention preset."

Install details: https://github.com/mitchtech/agent-johnny5#install

Which cues would you keep on? I am especially curious whether the alarm earns
its place or just startles people.

## R2 - r/codex showcase

Title: I built Agent Johnny 5: Short Circuit sound cues for Codex approvals

I made Agent Johnny 5, a free plugin that plays Johnny 5's voice in local Codex
sessions. Approvals get "Need input"; shell and file-edit approvals get "No
disassemble?"; and approvals whose command matches a short destructive list
(`rm -rf`, `git push --force`, `git reset --hard`, `DROP TABLE`, and similar) get
"No disassemble, Number Five!" Only a yes/no flag leaves the hook; the command
is never logged or stored.

The attached video illustrates the sound; it is not a live Codex recording.

```bash
codex plugin marketplace add mitchtech/agent-johnny5
codex plugin add johnny5@agent-johnny5
```

Requirements: Node.js 22+, a local audio player/device, and a restart. Review
and trust the installed commands in Codex's hook settings. Installation alone
does not trust hooks.

There are no npm runtime dependencies or runtime telemetry. Hooks return
promptly and do not supply approval decisions. Completion, compaction, and
session-end sounds are off by default. SSH/container execution plays where the
hook runs, not automatically on your laptop.

Install and compatibility details:
https://github.com/mitchtech/agent-johnny5#install

Where does setup get confusing: adding the marketplace, hook trust, or local
audio? If something fails, the host version and operating system would help me
reproduce it. Please leave private prompts and credentials out of reports.

## X1 - sound introduction

I built Agent Johnny 5: Short Circuit sound cues for Claude Code, Codex, and Gemini CLI.

"Need input" when it wants approval. "No disassemble!" when that approval is rm -rf.

Local. No telemetry. Free. Clip: illustrated preview.

https://github.com/mitchtech/agent-johnny5#install

## X2 - destructive-command alarm

Agent Johnny 5 checks what your coding agent wants approval for.

Ordinary edit: "No disassemble?"
rm -rf, force push, DROP TABLE: "No disassemble, Number Five!"

A cue, not a guard. The command never leaves the hook.

https://github.com/mitchtech/agent-johnny5#sounds

## X3 - quiet configuration

Want approval cues without the prompt chatter?

Agent Johnny 5's attention preset turns off session and prompt sounds.
Ask your agent: "Johnny 5, use the attention preset."

Event coverage varies by host. Clip: preview.

https://github.com/mitchtech/agent-johnny5#sound-controls

## X4 - useful follow-up

Trying Agent Johnny 5? Add the marketplace, install the plugin, then restart.

Codex also requires hook trust review. Remote sessions play audio on the
machine running the hook. Already running Agent Navi, Warcraft, or Rocky? Disable one per host.

https://github.com/mitchtech/agent-johnny5#install

## X5 - Codex pet

Johnny 5 is now a Codex pet.

Nine animations, sixteen look directions, tank treads. Codex animates him from
what your agent is doing. Installs on its own: no sounds required.

Clip: atlas preview. Drive every animation yourself:

https://mitchtech.github.io/agent-johnny5/#pet

## L1 - LinkedIn maker introduction

I built Agent Johnny 5, a small sound-notification plugin for Claude Code,
Codex, and Gemini CLI. It plays Johnny 5's lines from *Short Circuit* when a
coding agent needs attention, and it changes its tone when the approval is for
something you cannot take back.

The attached video is an illustrated preview of the cues, rather than a live
agent recording. The project is free to try.

The engineering problem was making a notification useful without making it
part of the agent's control flow. The hooks return promptly, leave approval
decisions alone, and tolerate missing audio or malformed input. The runtime
requires Node.js 22+ and has no npm dependencies or telemetry.

Code and installation:
https://github.com/mitchtech/agent-johnny5#install

If you use local coding agents, which event deserves a sound: approval, a
question, or the agent becoming ready for your next input?

## L2 - LinkedIn engineering follow-up

The most interesting feature in Agent Johnny 5 is also the one with the
smallest output: a single boolean.

When a coding agent asks to run a command, the hook checks it against a short
list of destructive patterns: recursive force deletes, force pushes, hard
resets, dropped tables. A match changes which sound plays. That is all it does.

The design constraint was that the command text never leaves the hook process.
The detached playback worker receives "dangerous: true", not the command. Nothing
is logged, and the cooldown state stores only hashed identifiers and timestamps.
A notification tool has no business keeping a history of what your agent ran.

I also documented what it is not. Pattern matching is a cue, not a security
boundary; an obfuscated command still gets the ordinary sound. Calling it a
safety feature would make it worse, because people would start trusting it.

The implementation and its tests are public:
https://github.com/mitchtech/agent-johnny5

## Replies and follow-up

Successful install: "Glad it worked. Which host and OS are you using, and which
cues did you leave on?"

Continued use, after at least a week and only in a willing conversation:
"Have you kept Johnny 5 enabled? If you muted or removed it, what led to that?"

Install problem: "Which host/version and OS are you using? Please share the
error with private paths and credentials removed. The diagnostics and hook
trust notes are in the README."

Alarm as safety: "It is only a louder sound. It never blocks anything, and an
indirect or obfuscated command gets the ordinary cue. Keep your normal
permission settings."

Pet interest: "Grab agent-johnny5-pet.zip from the latest release, extract the
johnny5 folder into ~/.codex/pets/, and pick Johnny 5. It works without the
sound plugin. Which host are you using?"

When someone has found it useful: "A GitHub star helps other people find it if
you'd like to support the project." Do not ask for Reddit votes or coordinated
engagement.
