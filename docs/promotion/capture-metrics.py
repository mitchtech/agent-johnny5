"""Save read-only GitHub campaign observations; never treat missing data as zero."""

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = "repos/mitchtech/agent-johnny5"


def read_api(path):
    try:
        result = subprocess.run(
            ["gh", "api", f"{REPO}/{path}" if path else REPO],
            capture_output=True, text=True, timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"available": False, "error": str(error)}
    if result.returncode:
        return {"available": False, "error": result.stderr.strip()}
    return {"available": True, "data": json.loads(result.stdout)}


now = datetime.now(timezone.utc)
snapshot = {"observed_at_utc": now.isoformat(), "repository": "mitchtech/agent-johnny5"}
repository = read_api("")
if repository["available"]:
    repository["data"] = {
        key: repository["data"][key]
        for key in ("stargazers_count", "forks_count", "open_issues_count", "default_branch")
    }
snapshot["repository_metrics"] = repository
releases = read_api("releases?per_page=100")
if releases["available"]:
    releases["data"] = [
        {"id": release["id"], "tag_name": release["tag_name"],
         "published_at": release["published_at"], "draft": release["draft"],
         "prerelease": release["prerelease"],
         "assets": [{key: asset[key] for key in ("id", "name", "download_count")}
                    for asset in release["assets"]]}
        for release in releases["data"]
    ]
snapshot["releases_first_100"] = releases
for metric in ("views", "clones", "popular/referrers"):
    snapshot[f"traffic/{metric}"] = read_api(f"traffic/{metric}")
output = ROOT / "dist" / "promotion" / "metrics"
output.mkdir(parents=True, exist_ok=True)
path = output / f"{now:%Y%m%dT%H%M%S%fZ}.json"
path.write_text(json.dumps(snapshot, indent=2) + "\n")
print(f"Saved {path.relative_to(ROOT)}")
for name, result in snapshot.items():
    if isinstance(result, dict) and "available" in result:
        print(f"{name}: {'available' if result['available'] else 'unavailable; see snapshot'}")
