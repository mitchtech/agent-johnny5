# Contributing

Create a feature branch and submit a PR to `main`. Describe the resulting user
behavior, the checks run, and any host limitations. Preserve unrelated work.

## Checks

```bash
npm run check
npm test
npm run test:package
python3 -m pip install -r requirements-dev.txt
python3 scripts/build-audio.py --check
python3 scripts/check-pet.py
python3 scripts/build-assets.py
python3 scripts/package-release.py
npm run site
```

Runtime tests inject players and random sources, and use isolated configuration/pet directories.
Package checks install the real tarball offline and execute the Gemini bundle's
registered hooks, including paths with spaces and shell metacharacters. They do
not prove speaker playback or native pet rendering on every host.

## Layout

`scripts/johnny5.mjs` owns sound behavior; `scripts/pet.mjs` owns independent local
pet installation. Host manifests and `hooks/{claude,codex,gemini}.json` adapt
those components. `skills/` contains the portable control workflow. The Gemini
builder creates a self-contained extension in `dist/gemini` without adding a
root default hook file to Claude/Codex installations.

`audio/` holds the canonical clips; `audio/sources.json` and
`scripts/build-audio.py` record and reproduce them (ffmpeg required for
rebuilds). `pets/johnny5` holds the complete pet bundle; `assets/original/johnny5`
preserves the original PNG. Installer tests cover the real bundle and isolated
fixtures, including packages without art. `assets/previews` is generated from
the clips and pet atlas by `scripts/build-assets.py`, and `assets/exports` by
`scripts/export-pet-web.py`; keep preview generation reproducible.

Release and discovery procedures live in [distribution maintenance](docs/distribution.md).
The [promotion kit](docs/promotion/README.md) contains public post drafts,
captioned media, install guidance, and the owner-run campaign calendar.
