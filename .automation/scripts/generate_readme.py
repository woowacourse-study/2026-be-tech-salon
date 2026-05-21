#!/usr/bin/env python3
"""Generate README.md from presentation metadata and the fixed README header."""
from __future__ import annotations

import os
import re
import subprocess
import sys
import unicodedata
import urllib.parse
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent.parent
DATA_FILE = ROOT / ".automation" / "presentations.yml"
HEADER_FILE = ROOT / ".automation" / "templates" / "readme_header.md"
OUT_FILE = ROOT / "README.md"


def detect_repo_slug() -> str:
    env = os.environ.get("GITHUB_REPOSITORY")
    if env:
        return env.strip()
    try:
        url = subprocess.check_output(
            ["git", "-C", str(ROOT), "config", "--get", "remote.origin.url"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""
    match = re.search(r"github\.com[:/]([^/]+/[^/.]+?)(?:\.git)?$", url)
    return match.group(1) if match else ""


def detect_branch() -> str:
    return os.environ.get("GITHUB_REF_NAME") or os.environ.get("README_BRANCH") or "main"


REPO_SLUG = detect_repo_slug()
BRANCH = detect_branch()
REPO_BASE = f"https://github.com/{REPO_SLUG}/blob/{BRANCH}/" if REPO_SLUG else ""
RAW_BASE = f"https://github.com/{REPO_SLUG}/raw/{BRANCH}/" if REPO_SLUG else ""


def encode_repo_path(rel_path: str, *, raw: bool = False) -> str:
    if not rel_path:
        return ""
    if rel_path.startswith("http"):
        return rel_path
    parts = rel_path.split("/")
    encoded = [urllib.parse.quote(unicodedata.normalize("NFC", part), safe="()") for part in parts]
    base = RAW_BASE if raw else REPO_BASE
    return base + "/".join(encoded)


def load_levels() -> list[dict]:
    data = yaml.safe_load(DATA_FILE.read_text()) or {}
    levels = data.get("levels") or []
    return sorted(levels, key=lambda item: int(item["level"]))


def render_presentation_cell(presentation: dict) -> str:
    title = presentation["title"]
    presenter = presentation["presenter"]
    pdf_url = encode_repo_path(presentation.get("pdf", ""))
    thumb_url = encode_repo_path(presentation.get("thumbnail", ""), raw=True)
    video_url = (presentation.get("video_url") or "").strip()

    media = f'<a href="{pdf_url}"><img src="{thumb_url}" width="300"/></a>' if thumb_url else f'<a href="{pdf_url}">📚 발표 자료</a>'
    links = [media]
    if video_url:
        links.append(f'<a href="{video_url}">🎥 발표 영상</a>')

    left = f'<div align="center">{"<br><br>".join(links)}</div>'
    right = f"**발표자:** {presenter}<br>**발표 주제:** {title}"
    return f"| {left} | {right} |"


def render_archive(levels: list[dict]) -> str:
    lines = ["# 📚 발표 아카이브", ""]
    if not levels:
        lines.append("_아직 등록된 발표가 없습니다._")
        return "\n".join(lines)

    for level in levels:
        presentations = level.get("presentations") or []
        if not presentations:
            continue
        lines.extend([
            f"## Level {level['level']}",
            "",
            "| 발표 자료 | 발표 정보 |",
            "|---|---|",
        ])
        lines.extend(render_presentation_cell(presentation) for presentation in presentations)
        lines.extend(["", "<br>", ""])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    header = HEADER_FILE.read_text().rstrip()
    content = header + "\n\n" + render_archive(load_levels())
    OUT_FILE.write_text(content)
    print(f"wrote {OUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
