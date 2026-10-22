# Distribution maintenance

Distribution channels: this GitHub repository, its Releases and Pages site, and
compatible official host distribution. npm publication is deferred until npm
authentication is ready. The GitHub package remains usable without a registry
publication.

## Release

`package.json` is the version authority. `npm run check` verifies that the
portable, Claude, and Gemini manifests match it, and that a release tag matches
`v` plus that version.

Prepare a release on a feature branch, update all manifest versions and the
changelog, and run the contributor checks. After its PR merges into `main`, tag
the merged commit and push the tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The release workflow checks Node 22/24 on macOS, Linux, and Windows, including
actual offline tarball installation and Gemini hook execution. Publishing also
requires the tagged commit to be contained in `main`. It verifies the committed
audio, validates the pet when art exists, regenerates previews and compares
their pixels with the committed files, then creates the GitHub release. The
workflow publishes no npm registry package.

Local release build:

```bash
npm run check
npm test
npm run test:package
python3 -m pip install -r requirements-dev.txt
python3 scripts/build-audio.py --check
python3 scripts/check-pet.py
python3 scripts/build-assets.py
python3 scripts/package-release.py
```

Release assets include the versioned npm tarball, a stable `agent-johnny5.tgz`
alias, three identically encoded platform-prefixed Gemini ZIPs, and versioned
and stable pet ZIPs containing the bundled artwork.
`SHA256SUMS` covers every attached artifact. ZIP order, timestamps, permissions,
and extracted source bytes are checked.

The Gemini archives contain the manifest at their root and their own default
hook file. Platform prefixes make selection unambiguous among the other assets.
See [Gemini integration](gemini.md). Never publish an archive with missing shared
runtime files or add a default hook file to the source package.

## Audio

The committed WAV files are canonical. `audio/sources.json` records each source
URL and hash, its trim window, and the hash of the committed output.
`python3 scripts/build-audio.py` downloads the sources, verifies their hashes,
and rebuilds every clip with ffmpeg; the output is byte-identical for a given
ffmpeg build. `--check` runs offline in CI and verifies hashes, format, length,
and that the manifest lists exactly the runtime's clips.

To change a clip, edit its entry in `sources.json` (or add one, and add the id
to `CLIPS` in `scripts/johnny5.mjs`), rebuild, listen to the result, and commit
the WAV and updated manifest together. If a source disappears upstream, the
committed files keep working; only rebuilds need the source.

## Pages and previews

`site/` contains dependency-free HTML, CSS, and JavaScript. `npm run site`
builds `dist/site`, copying audio and preview assets from their source
directories. Avoid maintaining duplicate audio files.

`python3 scripts/build-assets.py` renders a waveform GIF for each headline
clip, a 1200 x 630 social card, a 1280 x 440 README banner, and a 180 x 180
touch icon, all from the committed WAV files. Cards use the site's self-hosted
fonts with Pillow's basic layout engine, so their pixels match on every OS.
`--check` renders to a temporary directory and fails if any committed preview
differs by pixel; PNG bytes legitimately differ between platforms' zlib builds.
No analytics, third-party fonts, or runtime telemetry are loaded; `site/fonts`
holds the OFL-licensed faces.

The Pages workflow checks out the latest published release tag, validates, and
builds before deployment. Before the first release it publishes the pushed
commit. It runs after successful releases, on main updates, or manually.
The repository homepage points to `https://mitchtech.github.io/agent-johnny5/`.
Its social card is also available at
`https://mitchtech.github.io/agent-johnny5/previews/social.png`.

Check keyboard navigation, narrow viewports, reduced motion, clipboard feedback,
and all sound previews in both themes. The theme follows the operating system
until a visitor chooses one; `theme.js` stores that choice locally. `404.html`
uses root-relative `/agent-johnny5/` paths because Pages serves it at any
missing depth.

## npm and host directories

Future npm publication should use the `mitchtech` account, verifying
availability of the unscoped `agent-johnny5` name first. Configure
[npm trusted publishing](https://docs.npmjs.com/trusted-publishers/) through
GitHub Actions after the initial package ownership setup; do not store a
long-lived publishing token in the project.

OpenAI's public plugin submission currently excludes lifecycle-hook ZIPs, so
this package uses its documented GitHub marketplace installation.
[Submission rules](https://developers.openai.com/plugins/deploy/submission)

## Discovery

The repository homepage, concise About description, topics, CI/release/license
badges, and Pages previews form the primary discovery surface. Set
`assets/previews/social.png` as the repository's custom social preview through
GitHub Settings; there is no API for it.

The `gemini-cli-extension` topic plus the root `gemini-extension.json` make the
repository eligible for the official Gemini extension gallery; listing depends
on its validation and crawl schedule.
[Official discovery requirements](https://geminicli.com/docs/extensions/releasing/)

Use authenticated GitHub traffic and release-download counts
(`docs/promotion/capture-metrics.py`) for aggregate visibility checks. Those
counts include development checks and are not reliable measurements of unique
users. Keep the website free of analytics.
