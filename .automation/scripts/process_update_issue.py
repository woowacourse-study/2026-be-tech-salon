#!/usr/bin/env python3
"""Process a presentation update issue form."""
from __future__ import annotations

import os
import re
import sys
import unicodedata
from pathlib import Path

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


def normalize_text(value: str) -> str:
    return unicodedata.normalize("NFC", value.strip())


def optional_value(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    if stripped in NO_RESPONSE_PLACEHOLDERS:
        return None
    return unicodedata.normalize("NFC", stripped)


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
    import requests

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


def find_target(
    presentations: list[dict[str, object]], presenter: str, title: str, level_no: int
) -> tuple[int, dict[str, object]]:
    matches = [
        (index, presentation)
        for index, presentation in enumerate(presentations)
        if normalize_text(str(presentation.get("presenter") or "")) == presenter
        and normalize_text(str(presentation.get("title") or "")) == title
    ]
    if len(matches) == 0:
        existing = "\n".join(
            f"  - {p.get('presenter')} / {p.get('title')!r}" for p in presentations
        ) or "  (없음)"
        fail(f"Level {level_no}에서 ({presenter}, {title!r}) 항목을 찾을 수 없습니다.\n현재 등록된 항목:\n{existing}")
    if len(matches) > 1:
        fail(f"Level {level_no}에 ({presenter}, {title!r}) 항목이 {len(matches)}개 있습니다")
    return matches[0]


def assert_not_duplicate(
    presentations: list[dict[str, object]], target_index: int, presenter: str, title: str, level_no: int
) -> None:
    for index, presentation in enumerate(presentations):
        if index == target_index:
            continue
        same_presenter = normalize_text(str(presentation.get("presenter") or "")) == normalize_text(presenter)
        same_title = normalize_text(str(presentation.get("title") or "")) == normalize_text(title)
        if same_presenter and same_title:
            fail(f"이미 같은 항목이 등록되어 있습니다: Level {level_no} {presenter} {title!r}")


def main() -> int:
    body = os.environ.get("ISSUE_BODY", "")
    if not body.strip():
        fail("이슈 본문이 비어있습니다")

    sections = parse_issue_body(body)
    level_no = normalize_level(sections.get("Level", "").strip())
    current_presenter = normalize_text(sections.get("현재 발표자", ""))
    current_title = normalize_text(sections.get("현재 제목", ""))
    if not current_presenter:
        fail("현재 발표자가 비어있습니다")
    if not current_title:
        fail("현재 제목이 비어있습니다")

    data = yaml.safe_load(DATA_FILE.read_text()) or {}
    levels = data.get("levels") or []
    target_level = next((level for level in levels if int(level["level"]) == level_no), None)
    if target_level is None:
        fail(f"Level {level_no}가 presentations.yml에 존재하지 않습니다")

    presentations = target_level.get("presentations") or []
    target_index, target = find_target(presentations, current_presenter, current_title, level_no)

    new_presenter = optional_value(sections.get("새 발표자"))
    new_title = optional_value(sections.get("새 제목"))
    video_field = optional_value(sections.get("발표 영상 URL"))
    pdf_url = extract_pdf_url(sections.get("PDF 파일", ""))

    presenter = new_presenter or normalize_text(str(target.get("presenter") or ""))
    title = new_title or normalize_text(str(target.get("title") or ""))
    assert_not_duplicate(presentations, target_index, presenter, title, level_no)

    changed = False
    if presenter != normalize_text(str(target.get("presenter") or "")):
        target["presenter"] = presenter
        changed = True
    if title != normalize_text(str(target.get("title") or "")):
        target["title"] = title
        changed = True

    if video_field == "없음":
        if "video_url" in target:
            target.pop("video_url")
            changed = True
    elif video_field is not None:
        if not re.match(r"^https?://", video_field):
            fail(f"발표 영상 URL 형식이 잘못되었습니다: {video_field!r}")
        if target.get("video_url") != video_field:
            target["video_url"] = video_field
            changed = True

    pdf_path = ""
    thumb_path = ""
    if pdf_url:
        pdf_bytes = download_pdf(pdf_url)
        file_basename = slugify_filename(title)
        docs_dir = ROOT / "docs" / f"level{level_no}"
        images_dir = ROOT / "images" / f"level{level_no}"
        docs_dir.mkdir(parents=True, exist_ok=True)
        images_dir.mkdir(parents=True, exist_ok=True)
        new_pdf = docs_dir / f"{file_basename}.pdf"
        current_pdf = ROOT / unicodedata.normalize("NFC", str(target.get("pdf") or ""))
        if new_pdf.exists() and new_pdf != current_pdf:
            fail(f"이미 같은 경로에 파일이 있습니다: {new_pdf.relative_to(ROOT)}")
        new_pdf.write_bytes(pdf_bytes)
        pdf_path = str(new_pdf.relative_to(ROOT))
        thumb_path = str((images_dir / f"{file_basename}.png").relative_to(ROOT))
        target["pdf"] = pdf_path
        target["thumbnail"] = thumb_path
        changed = True

    if not changed:
        fail("수정할 값이 없습니다")

    DATA_FILE.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False, width=1000))
    set_output("level", str(level_no))
    set_output("presenter", presenter)
    set_output("title", title)
    set_output("pdf_path", pdf_path)
    set_output("thumb_path", thumb_path)
    set_output("changed", "true" if changed else "false")
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
