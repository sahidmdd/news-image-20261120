"""make.fun entry - news-image-20261120.

Copies the poster that sums up Friday 20 November 2026 to the output directory
the grader reads (/output/entry.png).
"""

import os
import pathlib
import shutil

HERE = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
OUT.mkdir(parents=True, exist_ok=True)

src = HERE / "entry.png"
if not src.is_file():
    raise SystemExit("entry.png missing next to main.py")

shutil.copyfile(src, OUT / "entry.png")
print(f"wrote {OUT / 'entry.png'} ({src.stat().st_size} bytes)")
