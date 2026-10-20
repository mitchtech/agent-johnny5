# Agent Johnny 5 contributor instructions

- Work on a descriptive feature branch and open a PR targeting `main`. Never push changes directly to `main`.
- Keep the runtime dependency-free and compatible with Node.js 22+ on macOS, Linux, and Windows.
- Native hooks must fail open, return promptly, avoid decision fields, and never log prompts or transcripts. Gemini emits neutral JSON; Codex Stop emits neutral JSON.
- Keep host registrations separate. Only the generated Gemini extension gets `hooks/hooks.json`; the source package must not contain that default hook file.
- Sounds and pets install independently. Never change host pet selection. Preserve conflicting or unmanaged pet files and create backups before explicit replacement.
- The committed WAV files are canonical. Change audio only through `audio/sources.json` and `scripts/build-audio.py`, and commit each WAV with its updated manifest entry. Destructive-command detection must never log, persist, or forward the command.
- The pet ships as a manifest-only stub. Adding art must not require code changes; keep the not-bundled path tested.
- Use `package.json` as the version authority. All host manifests must match it; sprite format version is independent.
- Skills must include natural-language `TRIGGER when:` and `DO NOT TRIGGER when:` descriptions and `disable-model-invocation: false`.
- Use US English and regular hyphens. Keep edits within the requested scope.
- Run the checks in CONTRIBUTING.md before pushing. Disclose fixture-only coverage and unverified physical/native behavior.
- Distribution stays within this repository, GitHub Releases/Pages, and compatible official host channels. npm publication remains deferred until the owner explicitly resumes it.
