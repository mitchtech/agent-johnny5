# Johnny 5 pet artwork

This artwork depicts Johnny 5 from *Short Circuit*. Michael J. Mitchell
requested it on October 21, 2026, and created it with Codex using built-in
image generation. A canonical robot image grounded the animation strips and
look-direction strips. Deterministic processing extracted, registered,
assembled, cleaned, and validated the generated pixels. The artwork was not
extracted from film frames.

Johnny 5 and *Short Circuit* belong to their respective rights holders. This
project is not affiliated with or endorsed by them. Film audio has a separate
[rights notice](../../../audio/NOTICE.md).

The contributor's rights in this artwork are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), as described in
[LICENSE.txt](LICENSE.txt). Suggested credit: "Johnny 5 pet artwork by Michael
J. Mitchell / mitchtech, CC BY 4.0, https://github.com/mitchtech/agent-johnny5."

## Format and validation

- ID: `johnny5`; display name: `Johnny 5`; sprite version: `2`.
- Transparent RGBA WebP, 1536 x 2288 pixels, with 192 x 208 cells.
- Nine animation rows: idle, moving right, moving left, waving, jumping,
  failure, waiting, working, and review.
- Two look rows: sixteen clockwise directions, beginning at up.
- 73 occupied cells and 15 fully transparent unused cells.

The final PNG passed structural, chroma, jump, registration, and visual
direction checks. Three isolated reviewers confirmed the gaze axes. The
active WebP preserves every decoded RGBA pixel from that PNG; encoding adds
no new artwork, neutral cell, or animation frame.

## Source and active files

The original PNG and local host manifest are preserved in
`assets/original/johnny5`. The original account-pet ID and temporary upload
links are not part of the distribution. `assets/pet-revision.json` records
source and active hashes.

| File | SHA-256 |
|---|---|
| Original PNG | `0862fae88ceec2312a09fa1b4f0fa05b3a5509317d69568193c4bc8d85299a24` |
| Active WebP | `e33c50c6c33252c9368c78a0c75f3a377e904918943e34afd80c80aeb8bc359b` |

The WebP was encoded with Pillow using `lossless=True`, `quality=100`,
`method=6`, and `exact=True`. Decoded pixels and transparent RGB were checked
after encoding. Native host rendering remains unverified.
