---
name: johnny5-control
disable-model-invocation: false
description: >-
  Inspect and control Agent Johnny 5 sound notifications without changing pet selection.
  TRIGGER when: the user says "mute Johnny 5", "unmute Johnny 5", "Johnny 5 status",
  "turn off prompt sounds", "enable approval sounds", "Johnny 5 attention mode",
  "turn off easter eggs", "stop the laser lips", "enable compaction sounds",
  "turn on session end sounds", "preview a Johnny 5 sound", "play No disassemble",
  "Number 5 is too loud", or asks to inspect or adjust Agent Johnny 5 notifications.
  DO NOT TRIGGER when: the user wants operating system volume controls, unrelated
  notification settings, Agent Navi controls (use navi-control), Agent Warcraft
  controls (use warcraft-control), Agent Rocky controls (use rocky-control),
  Agent Star Wars controls (use starwars-control), Agent StarCraft controls (use
  starcraft-control), pet artwork, or pet selection through the host picker.
---

# Johnny 5 sound controls

Resolve this installed SKILL.md's directory. The bundled CLI is
`../../scripts/johnny5.mjs` relative to it. Run it with Node and a quoted absolute
path, rather than assuming a global `agent-johnny5` executable is installed.

- Inspect: `status`, `status --json`, `list`, or `config --effective`.
- Mute/unmute: `mute EVENT|easter-egg|all` or `unmute EVENT|easter-egg|all`.
- Presets: `preset attention` or `preset default`.
- Requested sound preview: `preview CLIP`.

Use `list` to resolve supported event and clip names. Translate a clear request
into the corresponding event: prompt sounds are `prompt_submitted`, approval
sounds are `approval_required`, questions are `input_required`, ready
notifications are `ready_for_input`, compaction sounds are `context_compacting`,
and session end sounds are `session_ended`. Rare bonus lines ("laser lips",
"nice software", "attractive") are `easter-egg`. The destructive-command alarm
("No disassemble, Number Five!") is part of `approval_required`; it cannot be
muted separately without muting approvals. Ask only when the requested event is unclear.

Change preferences only when the user requests that change. Inspection and
troubleshooting do not imply muting, unmuting, applying a preset, or playing audio.
Always specify an event or explicit `all`. Global mute/unmute preserves event
preferences. Presets change event enablement and preserve clips and global mute.

Changes persist outside plugin caches and take effect on the next hook. Report
the resulting status. If `AGENT_JOHNNY5_MUTE` overrides the saved preference, explain
that the user must change it in the agent's launch environment. Do not modify
shell startup files or host configuration automatically.

Pet installation and selection are independent. These controls never change
pets, register hooks, or approve agent actions.
