"""Rebuild or verify the bundled clips from audio/sources.json. Building requires ffmpeg."""

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import urllib.request
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIO = ROOT / "audio"
MANIFEST = AUDIO / "sources.json"
MAX_SECONDS = 6
digest = lambda data: hashlib.sha256(data).hexdigest()


def runtime_clips():
    source = (ROOT / "scripts" / "johnny5.mjs").read_text()
    return re.findall(r"'([a-z0-9-]+)'", re.search(r"const CLIPS = \[(.*?)\];", source, re.S).group(1))


def fetch(url, expected, cache):
    path = cache / expected
    if not path.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "agent-johnny5-build-audio"})
        with urllib.request.urlopen(request, timeout=30) as response:
            path.write_bytes(response.read())
    if digest(path.read_bytes()) != expected:
        raise ValueError(f"Source changed upstream: {url}")
    return path


def ffmpeg(*args):
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-y", *args], check=True, capture_output=True, text=True)


def render(clip, cache, scratch, loudness, rate):
    inputs, chains = [], []
    for index, source in enumerate(clip["sources"]):
        inputs += ["-i", str(fetch(source["url"], source["sha256"], cache))]
        trim = f"atrim=start={source.get('start', 0)}" + (f":end={source['end']}" if "end" in source else "")
        chains.append(f"[{index}:a]{trim},asetpts=PTS-STARTPTS[s{index}]")
    joined = "".join(f"[s{index}]" for index in range(len(chains)))
    # Trim leading and trailing room tone before measuring.
    edges = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
    graph = ";".join(chains) + f";{joined}concat=n={len(chains)}:v=0:a=1,{edges}[out]"
    trimmed = scratch / f"{clip['id']}.wav"
    ffmpeg(*inputs, "-filter_complex", graph, "-map", "[out]", "-ar", str(rate), "-ac", "1", "-c:a", "pcm_f32le", str(trimmed))
    # Loudness gating ignores silence, so padding lets clips shorter than one 400 ms block be measured.
    report = ffmpeg("-i", str(trimmed), "-af", "apad=pad_dur=2,loudnorm=print_format=json", "-f", "null", "-").stderr
    measured = float(re.search(r'"input_i" : "(-?[0-9.]+)"', report).group(1))
    # One linear gain per clip keeps speech natural; the limiter only catches peaks.
    shape = f"volume={loudness - measured:.2f}dB,alimiter=limit=0.84:level=disabled,afade=t=in:d=0.01,areverse,afade=t=in:d=0.02,areverse"
    target = AUDIO / f"{clip['id']}.wav"
    ffmpeg("-i", str(trimmed), "-af", shape, "-ar", str(rate), "-ac", "1", "-c:a", "pcm_s16le",
           "-map_metadata", "-1", "-fflags", "+bitexact", "-flags:a", "+bitexact", str(target))
    return target


def verify(manifest):
    ids = [clip["id"] for clip in manifest["clips"]]
    if ids != runtime_clips():
        raise ValueError("audio/sources.json and CLIPS in scripts/johnny5.mjs list different clips")
    form = manifest["format"]
    report = {}
    for clip in manifest["clips"]:
        path = AUDIO / f"{clip['id']}.wav"
        if digest(path.read_bytes()) != clip["output"]:
            raise ValueError(f"{path.name} does not match its recorded build output")
        with wave.open(str(path)) as audio:
            if (audio.getframerate(), audio.getnchannels(), audio.getsampwidth()) != (form["sampleRate"], form["channels"], form["sampleWidth"]):
                raise ValueError(f"{path.name} is not {form['sampleRate']} Hz mono 16-bit PCM")
            seconds = audio.getnframes() / audio.getframerate()
        if not 0.2 < seconds <= MAX_SECONDS:
            raise ValueError(f"{path.name} lasts {seconds:.2f} s")
        report[clip["id"]] = round(seconds, 2)
    extra = sorted(path.name for path in AUDIO.glob("*.wav") if path.stem not in ids)
    if extra:
        raise ValueError(f"Unlisted audio files: {', '.join(extra)}")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify committed clips without downloading")
    parser.add_argument("--cache", type=Path, help="Directory for downloaded sources (default: a temporary directory)")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    if not args.check:
        with tempfile.TemporaryDirectory() as temporary:
            cache = args.cache or Path(temporary)
            cache.mkdir(parents=True, exist_ok=True)
            for clip in manifest["clips"]:
                target = render(clip, cache, Path(temporary), manifest["format"]["loudness"], manifest["format"]["sampleRate"])
                clip["output"] = digest(target.read_bytes())
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(verify(manifest), indent=2))


if __name__ == "__main__":
    main()
