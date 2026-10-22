"""Validate the Johnny 5 v2 pet bundle when its art is present. Requires requirements-dev.txt."""

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PET = ROOT / "pets" / "johnny5"
STATES = [
    ("idle", 6), ("moving-right", 8), ("moving-left", 8), ("waving", 4),
    ("jumping", 5), ("failure", 8), ("waiting", 6), ("working", 6),
    ("review", 6), ("look-up-to-down-right", 8), ("look-down-to-up-left", 8),
]


def validate():
    manifest = json.loads((PET / "pet.json").read_text())
    if (manifest.get("id"), manifest.get("spriteVersionNumber"), manifest.get("spritesheetPath")) != ("johnny5", 2, "spritesheet.webp"):
        raise ValueError("Expected the johnny5 v2 manifest")
    for key in ["displayName", "description"]:
        if not isinstance(manifest.get(key), str) or not manifest[key].strip():
            raise ValueError(f"Missing {key}")
    sheet = PET / manifest["spritesheetPath"]
    if not sheet.exists():
        # The pet ships as a manifest-only stub until its art lands.
        return {"bundled": False, "message": "pet art not bundled; skipping"}
    if not (PET / "LICENSE.txt").exists():
        raise ValueError("Bundled pet art needs LICENSE.txt")
    with Image.open(sheet) as source:
        if source.format != "WEBP" or source.mode != "RGBA" or source.size != (1536, 2288):
            raise ValueError("Expected a transparent 1536 x 2288 RGBA WebP")
        image = source.copy()
    occupied = 0
    empty = 0
    for row, (state, count) in enumerate(STATES):
        for column in range(8):
            cell = image.crop((column * 192, row * 208, (column + 1) * 192, (row + 1) * 208))
            visible = sum(cell.getchannel("A").histogram()[1:])
            if column < count:
                if not 50 <= visible < 192 * 208 * 0.95:
                    raise ValueError(f"Empty or opaque {state} frame {column}")
                occupied += 1
            else:
                if visible:
                    raise ValueError(f"Unused cell {row},{column} is not transparent")
                empty += 1
    data = image.tobytes()
    if any(data[i + 3] == 0 and any(data[i:i + 3]) for i in range(0, len(data), 4)):
        raise ValueError("Transparent pixels contain RGB residue")
    web = ROOT / "assets" / "exports" / "agent-johnny5-pet-web.webp"
    with Image.open(web) as export:
        if export.format != "WEBP" or export.size != (1536, 1872) or export.convert("RGBA").tobytes() != image.crop((0, 0, 1536, 1872)).tobytes():
            raise ValueError("Web export is stale; run python3 scripts/export-pet-web.py")
    return {"bundled": True, "format": "v2", "width": image.width, "height": image.height,
            "occupiedCells": occupied, "transparentCells": empty, "webExport": "matching"}


if __name__ == "__main__":
    print(json.dumps(validate(), indent=2))
