# Gemini CLI integration

Install from GitHub Releases containing the extension assets:

```bash
gemini extensions install https://github.com/mitchtech/agent-johnny5
```

For a pinned release, add `--ref v0.2.0`. Review hook consent, ensure Node.js 22+
and a local audio backend are on Gemini's PATH, and restart Gemini. Update with
`gemini extensions update agent-johnny5` and uninstall with
`gemini extensions uninstall agent-johnny5`.

## Packaging

Gemini discovers `hooks/hooks.json`, while Claude also automatically discovers
that filename. The source package keeps separate `hooks/claude.json`,
`hooks/codex.json`, and `hooks/gemini.json` registrations. `npm run gemini` builds
a self-contained extension in `dist/gemini`, putting only the Gemini hooks at
its default filename. Link that generated directory for local development.

The root `gemini-extension.json` provides shared version metadata and gallery
discovery. It does not make raw Git checkouts executable Gemini installations.
Use the packaged release or generated local directory.

Release assets named `darwin.agent-johnny5.zip`, `linux.agent-johnny5.zip`, and
`win32.agent-johnny5.zip` contain identical portable code. Separate names let Gemini
select the right extension when the release also contains npm and pet archives.
They include the shared runtime, sound clips, portable control skill, and the
pet manifest. Installing the extension never installs or selects a pet.

## Events and behavior

| Gemini event | Johnny 5 event |
|---|---|
| SessionStart: startup, resume, clear | session_started |
| BeforeAgent | prompt_submitted |
| Notification: ToolPermission | approval_required, with the destructive-command cue when `details.command` matches |
| AfterAgent, outside a retry | turn_completed, off by default |
| PreCompress | context_compacting, off by default |
| SessionEnd | session_ended, off by default |

Questions, ready notifications, and failures do not have mappings in this adapter.
Unknown notifications and retry completion are silent. Permission notifications
are advisory; Agent Johnny 5 never returns approval or denial decisions.
Every hook returns neutral JSON, including invalid-input and configuration-error
paths. Playback is detached, so the hook does not wait for a sound to finish.

The extension path is substituted into a hook environment variable and read by
a Node bootstrap. It is never interpolated into shell source. Event bodies are
not logged or forwarded to a service.

Sources: [extension format](https://geminicli.com/docs/extensions/reference/),
[hook contracts](https://geminicli.com/docs/hooks/reference/), and
[release asset selection](https://geminicli.com/docs/extensions/releasing/).
Payload and package tests validate those contracts. Live Gemini interaction and
physical audio on every OS remain separate checks.
