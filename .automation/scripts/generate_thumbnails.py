#!/usr/bin/env python3
"""Generate first-page PNG thumbnails for presentation PDFs."""
from __future__ import annotations

import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent.parent
DATA_FILE = ROOT / ".automation" / "presentations.yml"


def slugify_filename(title: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]', "_", title).strip()
    return unicodedata.normalize("NFC", cleaned) or "untitled"


def needs_rebuild(png: Path, pdf: Path) -> bool:
    if not png.exists():
        return True
    return png.stat().st_mtime < pdf.stat().st_mtime


def extract_first_page(pdf: Path, out_png: Path) -> bool:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    prefix = out_png.with_suffix("")
    cmd = ["pdftoppm", "-png", "-r", "150", "-singlefile", "-f", "1", "-l", "1", str(pdf), str(prefix)]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except FileNotFoundError:
        print("error: pdftoppm not found. Install poppler-utils.", file=sys.stderr)
        return False
    except subprocess.CalledProcessError as exc:
        print(f"error: pdftoppm failed for {pdf}: {exc.stderr.decode(errors='replace')}", file=sys.stderr)
        return False
    return out_png.exists()


def main() -> int:
    data = yaml.safe_load(DATA_FILE.read_text()) or {}
    generated = 0
    skipped = 0
    warnings = 0

    for level in data.get("levels") or []:
        level_no = int(level["level"])
        image_dir = ROOT / "images" / f"level{level_no}"
        for presentation in level.get("presentations") or []:
            pdf_rel = presentation.get("pdf")
            if not pdf_rel:
                continue
            pdf_path = ROOT / unicodedata.normalize("NFC", pdf_rel)
            if not pdf_path.exists():
                print(f"warn: missing pdf for level {level_no} / {presentation['presenter']}: {pdf_rel}", file=sys.stderr)
                warnings += 1
                continue

            existing_thumb = presentation.get("thumbnail")
            if existing_thumb:
                out_png = ROOT / unicodedata.normalize("NFC", existing_thumb)
            else:
                out_png = image_dir / f"{slugify_filename(presentation['title'])}.png"
                presentation["thumbnail"] = str(out_png.relative_to(ROOT))

            if not needs_rebuild(out_png, pdf_path):
                skipped += 1
                continue
            if extract_first_page(pdf_path, out_png):
                print(f"ok  : level {level_no} {presentation['presenter']} -> {out_png.relative_to(ROOT)}")
                generated += 1
            else:
                warnings += 1

    DATA_FILE.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False, width=1000))
    print(f"done. generated={generated} skipped={skipped} warnings={warnings}")
    return 0 if warnings == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
