#!/usr/bin/env python3
"""Process a presentation rollback issue form."""
from __future__ import annotations

import os
import re
import sys
import unicodedata
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent.parent
DATA_FILE = ROOT / ".automation" / "presentations.yml"


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


def normalize_level(level_str: str) -> int:
    match = re.search(r"\d+", level_str)
    if not match:
        fail(f"Level은 숫자를 포함해야 합니다: {level_str!r}")
    return int(match.group(0))


def delete_if_local(path_text: str) -> str:
    if not path_text or path_text.startswith("http"):
        return ""
    path = ROOT / unicodedata.normalize("NFC", path_text)
    if path.exists():
        path.unlink()
    return path_text


def main() -> int:
    body = os.environ.get("ISSUE_BODY", "")
    if not body.strip():
        fail("이슈 본문이 비어있습니다")

    sections = parse_issue_body(body)
    level_no = normalize_level(sections.get("Level", "").strip())
    presenter = sections.get("발표자", "").strip()
    title = sections.get("제목", "").strip()

    if not presenter:
        fail("발표자가 비어있습니다")
    if not title:
        fail("제목이 비어있습니다")

    data = yaml.safe_load(DATA_FILE.read_text()) or {}
    levels = data.get("levels") or []
    target_level = next((level for level in levels if int(level["level"]) == level_no), None)
    if target_level is None:
        fail(f"Level {level_no}가 presentations.yml에 존재하지 않습니다")

    presentations = target_level.get("presentations") or []
    matches = [
        (index, presentation)
        for index, presentation in enumerate(presentations)
        if presentation.get("presenter") == presenter and presentation.get("title") == title
    ]
    if len(matches) == 0:
        existing = "\n".join(f"  - {p.get('presenter')} / {p.get('title')!r}" for p in presentations) or "  (없음)"
        fail(f"Level {level_no}에서 ({presenter}, {title!r}) 항목을 찾을 수 없습니다.\n현재 등록된 항목:\n{existing}")
    if len(matches) > 1:
        fail(f"Level {level_no}에 ({presenter}, {title!r}) 항목이 {len(matches)}개 있습니다")

    index, target = matches[0]
    pdf_deleted = delete_if_local(target.get("pdf") or "")
    thumb_deleted = delete_if_local(target.get("thumbnail") or "")
    presentations.pop(index)

    if not presentations:
        data["levels"] = [level for level in levels if int(level["level"]) != level_no]

    DATA_FILE.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False, width=1000))
    set_output("level", str(level_no))
    set_output("presenter", presenter)
    set_output("title", title)
    set_output("pdf_path", pdf_deleted)
    set_output("thumb_path", thumb_deleted)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
