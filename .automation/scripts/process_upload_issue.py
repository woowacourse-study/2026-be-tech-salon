#!/usr/bin/env python3
"""Process a presentation upload issue form."""
from __future__ import annotations

import os
import re
import sys
import unicodedata
from pathlib import Path

import requests
import yaml


ROOT = Path(__file__).resolve().parent.parent.parent
DATA_FILE = ROOT / ".automation" / "presentations.yml"
NO_RESPONSE_PLACEHOLDERS = {"", "_No response_"}


def parse_issue_body(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current_key: str | None = None
    current_lines: list[str] = []
    for line in body.replace("\r\n", "\n").split("\n"):
        match = re.match(r"^###\s+(.+?)\s*$", line)
        if match:
            if current_key is not None:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = match.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_key is not None:
        sections[current_key] = "\n".join(current_lines).strip()
    return sections


def extract_pdf_url(text: str) -> str | None:
    match = re.search(r"https?://[^\s)]+\.pdf(?:[?#][^\s)]*)?", text, re.IGNORECASE)
    return match.group(0) if match else None


def slugify_filename(title: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]', "_", title).strip()
    return unicodedata.normalize("NFC", cleaned) or "untitled"


def set_output(name: str, value: str) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a") as file:
        file.write(f"{name}<<__EOF__\n{value}\n__EOF__\n")


def fail(msg: str) -> None:
    set_output("error", msg)
    print(f"::error::{msg}", file=sys.stderr)
    sys.exit(1)


def download_pdf(url: str) -> bytes:
    headers = {"Accept": "application/octet-stream"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(url, headers=headers, timeout=120, allow_redirects=True)
    if response.status_code != 200:
        fail(f"PDF 다운로드 실패: HTTP {response.status_code}")
    if not response.content.startswith(b"%PDF"):
        fail("받은 파일이 PDF가 아닙니다")
    return response.content


def normalize_level(level_str: str) -> int:
    match = re.search(r"\d+", level_str)
    if not match:
        fail(f"Level은 숫자를 포함해야 합니다: {level_str!r}")
    level_no = int(match.group(0))
    if level_no < 1 or level_no > 99:
        fail(f"Level 범위 초과: {level_no}")
    return level_no


def main() -> int:
    body = os.environ.get("ISSUE_BODY", "")
    if not body.strip():
        fail("이슈 본문이 비어있습니다")

    sections = parse_issue_body(body)
    level_no = normalize_level(sections.get("Level", "").strip())
    presenter = sections.get("발표자", "").strip()
    title = sections.get("제목", "").strip()
    video_url = sections.get("발표 영상 URL", "").strip()
    pdf_field = sections.get("PDF 파일", "")

    if not presenter:
        fail("발표자가 비어있습니다")
    if not title:
        fail("제목이 비어있습니다")
    if video_url in NO_RESPONSE_PLACEHOLDERS:
        video_url = ""
    if video_url and not re.match(r"^https?://", video_url):
        fail(f"발표 영상 URL 형식이 잘못되었습니다: {video_url!r}")

    pdf_url = extract_pdf_url(pdf_field)
    if not pdf_url:
        fail("PDF 첨부 링크를 본문에서 찾을 수 없습니다")

    data = yaml.safe_load(DATA_FILE.read_text()) or {}
    data.setdefault("levels", [])
    target_level = next((level for level in data["levels"] if int(level["level"]) == level_no), None)
    if target_level is None:
        target_level = {"level": level_no, "presentations": []}
        data["levels"].append(target_level)
        data["levels"].sort(key=lambda item: int(item["level"]))

    for presentation in target_level.get("presentations", []):
        if presentation.get("presenter") == presenter and presentation.get("title") == title:
            fail(f"이미 같은 항목이 등록되어 있습니다: Level {level_no} {presenter} {title!r}")

    pdf_bytes = download_pdf(pdf_url)
    file_basename = slugify_filename(title)
    docs_dir = ROOT / "docs" / f"level{level_no}"
    images_dir = ROOT / "images" / f"level{level_no}"
    docs_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = docs_dir / f"{file_basename}.pdf"
    if pdf_path.exists():
        fail(f"이미 같은 경로에 파일이 있습니다: {pdf_path.relative_to(ROOT)}")
    pdf_path.write_bytes(pdf_bytes)

    entry = {
        "presenter": presenter,
        "title": title,
        "pdf": str(pdf_path.relative_to(ROOT)),
        "thumbnail": str((images_dir / f"{file_basename}.png").relative_to(ROOT)),
    }
    if video_url:
        entry["video_url"] = video_url

    target_level.setdefault("presentations", []).append(entry)
    DATA_FILE.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False, width=1000))

    set_output("level", str(level_no))
    set_output("presenter", presenter)
    set_output("title", title)
    set_output("pdf_path", entry["pdf"])
    set_output("thumb_path", entry["thumbnail"])
    print(f"저장: {entry['pdf']} ({len(pdf_bytes):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
