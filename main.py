from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from json_diff_app.ui.main_window import run


def main() -> int:
    """通过根目录兼容入口启动 JSON Diff 桌面应用。"""

    return run()


if __name__ == "__main__":
    raise SystemExit(main())
