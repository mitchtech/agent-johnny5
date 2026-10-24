# From install to first cue

Agent Johnny 5 is free to try. Sounds require Node.js 22+ on the agent's PATH and
local audio: `afplay` on macOS, a supported Linux player, or Windows PowerShell
on Windows. Remote hooks play on the remote machine unless an audio bridge is
already configured.

## Claude Code

Run in a terminal:

```bash
claude plugin marketplace add mitchtech/agent-johnny5
claude plugin install johnny5@agent-johnny5
```

Restart Claude Code. A new session should greet you with "Number five is alive!"
or "Hi". In a disposable project, request a harmless operation that requires
approval under your existing permission settings; it should play "Need input"
or, for a file edit, "No disassemble?". Do not weaken permissions to make the
demonstration work. Use the explicit preview below to check audio separately.

## Codex

```bash
codex plugin marketplace add mitchtech/agent-johnny5
codex plugin add johnny5@agent-johnny5
```

Review and trust the installed hooks in Codex's hook settings, then restart.
Repeat the harmless approval check under your normal permission settings.
Installing or enabling the plugin alone does not establish hook trust.

## Already using another Agent plugin?

Agent Navi, Agent Johnny 5, Agent Warcraft, and Agent Rocky answer the same
events. Disable all but one per host, for example:
`claude plugin disable navi@agent-navi` for Claude Code, or `enabled = false`
under `[plugins."navi@agent-navi"]` in `~/.codex/config.toml` for Codex.

## Diagnose and preview without a global install

The bundled control skill supports requests such as "check Johnny 5's sound
status," "mute Johnny 5," "turn off easter eggs," and "Johnny 5, use the
attention preset." For an explicit terminal preview, use the repository CLI:

```bash
git clone https://github.com/mitchtech/agent-johnny5.git
cd agent-johnny5
node scripts/johnny5.mjs doctor
node scripts/johnny5.mjs preview need-input
```

`doctor` does not play audio or change settings. `preview` explicitly plays a
clip even when muted; it is an audio check, not proof that a host hook fired.
These commands need no npm install. To hear the destructive-command path without
an agent:

```bash
node scripts/johnny5.mjs play approval_required --tool Bash --command "rm -rf build"
```

That passes the string to the matcher only; nothing is executed.

To keep only attention-related events:

```bash
node scripts/johnny5.mjs preset attention
node scripts/johnny5.mjs status
```

The attention preset turns off session, prompt, completion, error, compaction,
and session-end cues. Approval, question, and ready events remain enabled where
the host exposes them.

```bash
node scripts/johnny5.mjs mute all
node scripts/johnny5.mjs unmute all
node scripts/johnny5.mjs preset default
```

Mute/unmute preserves individual event preferences. The default preset restores
event enablement and preserves global mute and custom clip choices.

## Remove sounds

Use the command for the host you installed:

```bash
claude plugin uninstall johnny5@agent-johnny5
```

```bash
codex plugin remove johnny5@agent-johnny5
```

Restart the host. Persistent sound settings are stored separately from plugin
caches.

If a check fails, report the host/version, operating system, expected event,
and redacted diagnostic error through [GitHub Issues](https://github.com/mitchtech/agent-johnny5/issues).
Do not include prompts, transcripts, credentials, or private configuration.
