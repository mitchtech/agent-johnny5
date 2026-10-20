# Media and live capture scripts

## Available previews

These assets are illustrated previews assembled from the bundled WAV files and
the site's fonts. They do not show a native host, a real approval dialog, or
physical speaker playback. Keep their labels visible and describe them as previews.

| Asset | Duration | Use |
|---|---|---|
| [Sound preview](../../assets/promotion/sound-preview.mp4) | 24 seconds | Main sound posts; cues at 0.5 s (alive), 6.5 s (need input), 10.5 s (no disassemble, with `rm -rf` on screen), 15.5 s (more input) |
| [Attention preview](../../assets/promotion/attention-preview.mp4) | 12 seconds | Configuration post; one approval cue at 5.5 s |

Each MP4 is 1080 x 1080, 15 fps, H.264/yuv420p with AAC audio, burned-in
captions, and a fast-start header. An oscilloscope on screen sweeps each clip's
waveform in sync with its audio. Matching `.srt` files and PNG posters live
beside the videos. The [manifest](../../assets/promotion/manifest.json) records
hashes, source files, tool versions, and limitations. The README's
[waveform GIFs](../../assets/previews/need-input.gif) remain available.

Build locally with existing Pillow and FFmpeg installations:

```bash
python3 docs/promotion/build-media.py
```

This script never installs tools, plays audio through speakers, uses account
credentials, or publishes files. Code is MIT. Video composition does not grant
rights to the *Short Circuit* audio. Preserve the [audio notice](../../audio/NOTICE.md)
and [font notice](../../site/fonts/OFL.md).

## Native approval recording - 20-30 seconds

Use this script when a verified host recording is available. Capture a fresh
disposable project and only the relevant host window. Keep your normal permission
settings. Capture application/system audio if supported; a screen recording
without an audio track does not establish an audible cue.

| Time | Capture | Caption |
|---|---|---|
| 0-3 s | Host and exact version visible; harmless task underway | Your agent is waiting for approval |
| 3-8 s | A real approval request and the corresponding cue | Need input |
| 8-15 s | Your response to the dialog; retain enough context to understand it | You make the decision |
| 15-22 s | Verified install commands for that host | Agent Johnny 5 - local sound cues |
| 22-27 s | Repository address | github.com/mitchtech/agent-johnny5 |

Use a request to write a temporary text file in the disposable project if it
requires approval under the existing policy. If it is already approved, do not
manufacture an approval dialog or substitute a `play` invocation while claiming
native behavior. Match the caption to the actual cue: file-edit requests play
"No disassemble?" rather than "Need input".

## Destructive-command recording - 10-15 seconds

In a disposable directory containing only a throwaway `build/` folder, ask the
agent to delete it with `rm -rf build`. Record the approval dialog and the
"No disassemble, Number Five!" cue, then deny or approve as you would normally.
Never point the demonstration at anything you would mind losing, and never
weaken permissions to stage it. Caption it as a cue, not a safeguard.

Pass criteria for both recordings: visible native dialog, matching audio track,
exact host/version noted in the capture record, readable captions at phone
width, no private content, and no dubbed cue presented as live playback. Replace
the preview disclaimer in the relevant post only after these criteria pass.

## Quiet configuration recording - 10-15 seconds

Show the current status; invoke `preset attention` through the bundled skill or
repository CLI; show the resulting enabled events. Caption session/prompt cues
as disabled and attention events as host-dependent. Do not claim a silent event
was observed merely because no audio was captured.
