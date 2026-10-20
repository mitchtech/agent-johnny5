"""Build checked release assets, including the isolated Gemini extension."""

import hashlib
import importlib.util
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "release"


def main():
    spec = importlib.util.spec_from_file_location("package_pet", ROOT / "scripts" / "package-pet.py")
    pet = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pet)
    if OUT.exists():
        shutil.rmtree(OUT)
    archive = pet.package(OUT, with_package=True)
    version = json.loads((ROOT / "package.json").read_text())["version"]
    if archive:
        shutil.copyfile(archive, OUT / "agent-johnny5-pet.zip")
    shutil.copyfile(OUT / f"agent-johnny5-{version}.tgz", OUT / "agent-johnny5.tgz")
    subprocess.run(["node", "scripts/build-gemini.mjs"], cwd=ROOT, check=True)
    extension = ROOT / "dist" / "gemini"
    archive = OUT / "darwin.agent-johnny5.zip"
    files = sorted(path for path in extension.rglob("*") if path.is_file())
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(extension).as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            output.writestr(info, path.read_bytes(), compresslevel=9)
    with zipfile.ZipFile(archive) as output:
        for path in files:
            if output.read(path.relative_to(extension).as_posix()) != path.read_bytes():
                raise ValueError(f"Gemini ZIP altered {path.name}")
    # Gemini selects platform-prefixed assets when a release has multiple files.
    # All three contain identical portable Node code, rather than native binaries.
    for platform in ["linux", "win32"]:
        shutil.copyfile(archive, OUT / f"{platform}.agent-johnny5.zip")
    web = ROOT / "assets" / "exports" / "agent-johnny5-pet-web.webp"
    if web.exists():
        shutil.copyfile(web, OUT / web.name)
    artifacts = sorted(path for path in OUT.iterdir() if path.name != "SHA256SUMS")
    (OUT / "SHA256SUMS").write_text("".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in artifacts))
    changelog = (ROOT / "CHANGELOG.md").read_text()
    section = changelog.split(f"## {version} - ", 1)[1].split("\n## ", 1)[0].split("\n", 1)[1].lstrip("\n")
    (ROOT / "dist" / "release-notes.md").write_text(section)
    print(f"Built {len(artifacts)} release assets and checksums in {OUT}")


if __name__ == "__main__":
    main()
