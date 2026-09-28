#!/usr/bin/env python3
"""Propose a LINE CLI formula update only after verifying published archives."""

import hashlib
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path


REPOSITORY = "kongesque/line-cli"
RELEASE_API = f"https://api.github.com/repos/{REPOSITORY}/releases/latest"
FORMULA = Path(__file__).resolve().parents[1] / "Formula" / "line-cli.rb"
ARCHIVES = {
    "on_arm": "line-darwin-arm64.tar.gz",
    "on_intel": "line-darwin-amd64.tar.gz",
}
MAX_METADATA = 1024 * 1024
MAX_ARCHIVE = 128 * 1024 * 1024
VERSION = re.compile(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")
CHECKSUM = re.compile(r"([0-9a-fA-F]{64})\s+\*?([^\s]+)\Z")


def version_parts(tag):
    match = VERSION.fullmatch(tag)
    if not match:
        raise ValueError(f"Invalid stable release tag: {tag!r}")
    return tuple(int(part) for part in match.groups())


def fetch(url, limit, *, token=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "line-cli-homebrew-tap"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        if urllib.parse.urlsplit(response.geturl()).scheme != "https":
            raise ValueError("Release download redirected away from HTTPS")
        data = response.read(limit + 1)
        if len(data) > limit:
            raise ValueError(f"Release download exceeds {limit} bytes: {url}")
        return data


def release_assets(release):
    tag = release["tag_name"]
    version_parts(tag)
    if release.get("draft") or release.get("prerelease"):
        raise ValueError("Latest release is not stable and published")

    required = set(ARCHIVES.values()) | {"SHA256SUMS.txt"}
    found = {}
    for asset in release["assets"]:
        name = asset["name"]
        if name not in required:
            continue
        if name in found:
            raise ValueError(f"Duplicate release asset: {name}")
        expected_url = f"https://github.com/{REPOSITORY}/releases/download/{tag}/{name}"
        if asset["browser_download_url"] != expected_url:
            raise ValueError(f"Unexpected release asset URL: {name}")
        if not 0 < asset["size"] <= (MAX_METADATA if name == "SHA256SUMS.txt" else MAX_ARCHIVE):
            raise ValueError(f"Unexpected release asset size: {name}")
        found[name] = asset
    if found.keys() != required:
        raise ValueError(f"Missing release assets: {', '.join(sorted(required - found.keys()))}")
    return tag, found


def archive_checksums(manifest):
    checksums = {}
    for line in manifest.decode("utf-8").splitlines():
        match = CHECKSUM.fullmatch(line)
        if not match:
            raise ValueError("Malformed release checksum manifest")
        checksum, name = match.groups()
        if name in checksums:
            raise ValueError(f"Duplicate checksum: {name}")
        checksums[name] = checksum.lower()
    missing = set(ARCHIVES.values()) - checksums.keys()
    if missing:
        raise ValueError(f"Missing archive checksums: {', '.join(sorted(missing))}")
    return checksums


def verify_archives(assets, checksums, downloader=fetch):
    for archive in ARCHIVES.values():
        asset = assets[archive]
        content = downloader(asset["browser_download_url"], MAX_ARCHIVE)
        if len(content) != asset["size"]:
            raise ValueError(f"Archive size mismatch: {archive}")
        if hashlib.sha256(content).hexdigest() != checksums[archive]:
            raise ValueError(f"Archive checksum mismatch: {archive}")


def render_formula(formula, tag, checksums):
    current = re.findall(r'^  version "([^"]+)"$', formula, re.MULTILINE)
    if len(current) != 1:
        raise ValueError("Expected exactly one formula version")
    if version_parts(tag) < version_parts(f"v{current[0]}"):
        raise ValueError("Refusing to downgrade the formula")
    updated = formula.replace(f'  version "{current[0]}"', f'  version "{tag[1:]}"', 1)
    for block, archive in ARCHIVES.items():
        pattern = re.compile(
            rf'(  {block} do\n    url ")[^"]+("\n    sha256 ")[0-9a-f]{{64}}("\n  end)'
        )
        url = f"https://github.com/{REPOSITORY}/releases/download/{tag}/{archive}"
        updated, count = pattern.subn(
            lambda match: f"{match[1]}{url}{match[2]}{checksums[archive]}{match[3]}",
            updated,
        )
        if count != 1:
            raise ValueError(f"Expected exactly one {block} formula block")
    return updated


def main():
    release = json.loads(fetch(RELEASE_API, MAX_METADATA, token=os.getenv("GITHUB_TOKEN")))
    tag, assets = release_assets(release)
    formula = FORMULA.read_text()
    current = re.search(r'^  version "([^"]+)"$', formula, re.MULTILINE)
    if current and version_parts(tag) == version_parts(f"v{current[1]}"):
        print(f"Formula is current at {tag}")
        return

    manifest = fetch(assets["SHA256SUMS.txt"]["browser_download_url"], MAX_METADATA)
    checksums = archive_checksums(manifest)
    verify_archives(assets, checksums)

    updated = render_formula(formula, tag, checksums)
    if updated != formula:
        FORMULA.write_text(updated)
        print(f"Verified both macOS archives and updated formula to {tag}")


if __name__ == "__main__":
    main()
