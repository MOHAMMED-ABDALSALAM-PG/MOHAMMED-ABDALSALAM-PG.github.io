#!/usr/bin/env python3
"""Refresh public metadata for the repositories listed in data/projects.json.

Only repositories in the curated manifest are queried, and only public ones are
written out: a repository that is (or becomes) private is skipped, so nothing
private can reach the website. Output: data/github.json.

Uses GITHUB_TOKEN from the environment when present (higher rate limit);
works unauthenticated otherwise.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.github.com"


def get(path, retries=6):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "academic-site-refresh"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    for attempt in range(retries):
        req = urllib.request.Request(API + path, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status == 202:  # statistics are being computed
                    time.sleep(3 + 2 * attempt)
                    continue
                body = r.read()
                return json.loads(body) if body else None
        except urllib.error.HTTPError as e:
            if e.code in (404, 451):
                return None
            if e.code in (403, 429, 500, 502, 503) and attempt < retries - 1:
                time.sleep(5 + 5 * attempt)
                continue
            raise
    return None


def main():
    manifest = json.loads((ROOT / "data/projects.json").read_text())
    out_path = ROOT / "data/github.json"
    previous = json.loads(out_path.read_text()) if out_path.exists() else {"repos": {}}
    repos = {}
    for p in manifest["projects"]:
        name = p["repo"]
        meta = get(f"/repos/{name}")
        if meta is None or meta.get("private"):
            print(f"skip {name}: not publicly available", file=sys.stderr)
            continue
        weeks = get(f"/repos/{name}/stats/commit_activity")
        if not isinstance(weeks, list):  # keep the last good series if stats are not ready
            weeks = previous.get("repos", {}).get(name, {}).get("weekly_commits")
            weekly = weeks
        else:
            weekly = [{"week": w["week"], "total": w["total"]} for w in weeks]
        repos[name] = {
            "html_url": meta["html_url"],
            "description": meta.get("description"),
            "language": meta.get("language"),
            "stars": meta.get("stargazers_count", 0),
            "forks": meta.get("forks_count", 0),
            "license": (meta.get("license") or {}).get("spdx_id"),
            "pushed_at": meta.get("pushed_at"),
            "default_branch": meta.get("default_branch"),
            "weekly_commits": weekly,
        }
        print(f"ok   {name}", file=sys.stderr)
    data = {"retrieved_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "repos": repos}
    out_path.write_text(json.dumps(data, indent=1) + "\n")


if __name__ == "__main__":
    main()
