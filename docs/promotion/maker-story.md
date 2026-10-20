# Why I built Agent Johnny 5

Coding agents spend part of their time waiting for a person. An approval needs
a decision. A question needs an answer. The terminal may be ready for the next
instruction while attention is somewhere else. I had already built Agent Navi
to give those moments a familiar sound. Agent Johnny 5 gives them a different
voice, and one new idea.

The voice is Johnny 5 from *Short Circuit* (1986), a robot whose defining trait
is wanting more input. That fit was hard to pass up: "Need input" for an
approval, "I have questions" when the agent asks one, "More input" when it is
idle and waiting. Twenty lines in all, each tied to an agent event.

The new idea came from the film's other catchphrase. "No disassemble!" is what
Johnny 5 says when he thinks he is about to be taken apart. That is a reasonable
thing to hear when your agent asks permission to run `rm -rf`, force-push, or
drop a table. So when an approval's command matches a short list of destructive
patterns, the cue changes.

The interesting part is what that feature is not allowed to do. The hook reads
the command, sets a yes/no flag, and stops. The command text never reaches the
detached playback worker, is never logged, and is never stored; the cooldown
state holds only hashed identifiers and timestamps. A notification tool has no
business keeping a history of what your agent ran.

It is also not a safety feature, and the documentation says so. Pattern matching
catches the obvious cases; an indirect or obfuscated command gets the ordinary
sound. If people started trusting the alarm, it would make them less careful,
which is the opposite of the point.

The rest of the design is inherited from Agent Navi. Host hooks return promptly
and fail open on malformed input, missing audio, invalid configuration, and
playback failure. They never approve or block actions. The shared player uses
Node.js 22+ with no npm runtime dependencies across macOS, Linux, and Windows.
Repeated events have a cooldown, overlapping clips are dropped, and the
attention preset keeps only the cues that need you.

The audio needed more care than Navi's five clips. The sources are fan
soundboard rips of varying quality and length, so a build script records each
source URL and hash, trims it, matches loudness across all twenty clips, and
records the output hash. I transcribed every result to confirm the trim kept
the right words, which is how I learned one source's "Input!" starts with a
beep and another's "Reassemble" has someone else saying "Huh?" at the end.

There are also a few easter eggs. About one in fifty of the routine cues is
replaced by a bonus line. They never replace an approval, question, error, or
alarm, and one command turns them off.

The project separates its licenses: MIT for code and configuration, and a
separate notice for the *Short Circuit* recordings. There is no claim of
official affiliation or ownership of the character or the audio.

If you try Johnny 5, I would like to know which cues you keep and whether the
alarm earns its place. Those answers are more useful than another feature
imagined in advance of someone needing it.

[Install Agent Johnny 5](https://github.com/mitchtech/agent-johnny5#install)
or [hear every clip](https://mitchtech.github.io/agent-johnny5/).
