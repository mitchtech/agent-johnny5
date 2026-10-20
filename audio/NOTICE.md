# Audio provenance and rights

The WAV files in this directory are derived from *Short Circuit* (1986, TriStar
Pictures). Johnny 5 was voiced by Tim Blaney. The rights holders retain all
rights to the underlying film audio, including Johnny 5's lines. No ownership
of those clips is claimed, and no affiliation or endorsement is implied.

The repository's MIT license covers source code and configuration only. It
does not cover these recordings or grant any rights to the film's audio.

The clips are included for personal, non-commercial use. This notice records
their provenance; it is not a license from the rights holders. They will be
removed on request from a rights holder.

## Sources and processing

[`sources.json`](sources.json) lists every source URL, its SHA-256, the trim
window, and the hash of each committed output. The sources are public fan
soundboards: johnny5soundboard.com and the 101soundboards *Short Circuit*
board. Neither publishes a license for its recordings.

[`scripts/build-audio.py`](../scripts/build-audio.py) trims each source,
removes leading and trailing room tone, applies one linear gain to reach
-16 LUFS integrated with a peak limiter, adds 10-20 ms fades, and writes 16-bit
mono PCM WAV at 32 kHz. `--check` verifies the committed files without
downloading anything.

| File | Line | Length | Source |
|---|---|---|---|
| `alive.wav` | Number five is alive! | 5.32 s | 101soundboards.com |
| `hi.wav` | Hi | 0.60 s | johnny5soundboard.com |
| `input.wav` | Input! | 1.10 s | 101soundboards.com |
| `yup.wav` | Yup | 0.45 s | johnny5soundboard.com |
| `gotit.wav` | You got it | 0.52 s | johnny5soundboard.com |
| `need-input.wav` | Need input | 1.08 s | johnny5soundboard.com |
| `more-input.wav` | More input | 1.12 s | johnny5soundboard.com |
| `questions.wav` | I have questions | 2.16 s | johnny5soundboard.com |
| `no-disassemble-q.wav` | No disassemble? | 1.13 s | johnny5soundboard.com |
| `no-disassemble-five.wav` | No disassemble, Number Five! | 2.45 s | johnny5soundboard.com |
| `malfunction.wav` | Malfunction | 1.14 s | johnny5soundboard.com |
| `error.wav` | Error | 0.65 s | johnny5soundboard.com |
| `uh-oh.wav` | Uh oh | 1.13 s | johnny5soundboard.com |
| `excellent.wav` | Excellent | 0.69 s | johnny5soundboard.com |
| `pretty-good.wav` | Pretty good | 1.07 s | johnny5soundboard.com |
| `reassemble.wav` | Reassemble | 1.40 s | 101soundboards.com |
| `times-up.wav` | Time's up | 0.70 s | johnny5soundboard.com |
| `laser-lips.wav` | Hey, laser lips! Your mama was a snow blower! | 3.97 s | johnny5soundboard.com |
| `nice-software.wav` | Nice software | 1.74 s | johnny5soundboard.com |
| `attractive.wav` | Attractive | 0.97 s | johnny5soundboard.com |

Use the user audio directory setting to supply your own replacement recordings
without editing installed plugin files.
