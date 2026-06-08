from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from json_diff_app.core.diff_engine import (
    MISSING,
    compare_json,
    format_json_with_line_map,
    path_to_text,
    preview_value,
)


class DiffEngineTestCase(unittest.TestCase):
    """测试 JSON 差异比较核心逻辑。"""

    def test_compare_json_reports_all_diff_kinds(self) -> None:
        """比较左右 JSON 时应识别新增、删除、值变化和类型变化。"""

        left = {
            "same": 1,
            "removed": 2,
            "changed": 3,
            "typed": 4,
            "items": [1, 2],
        }
        right = {
            "same": 1,
            "changed": 4,
            "typed": "4",
            "items": [1, 2, 3],
            "added": 5,
        }

        diffs = compare_json(left, right)
        actual = {(diff.kind, diff.path) for diff in diffs}

        self.assertEqual(
            actual,
            {
                ("removed", ("removed",)),
                ("changed", ("changed",)),
                ("type_changed", ("typed",)),
                ("added", ("items", 2)),
                ("added", ("added",)),
            },
        )

    def test_path_to_text_formats_common_and_quoted_paths(self) -> None:
        """路径文本应同时支持点号、数组下标和引号属性。"""

        self.assertEqual(path_to_text(()), "$")
        self.assertEqual(path_to_text(("user", 0, "name")), "$.user[0].name")
        self.assertEqual(path_to_text(("with space", "中文")), '$["with space"]["中文"]')

    def test_format_json_with_line_map_records_nested_lines(self) -> None:
        """格式化 JSON 时应记录嵌套路径对应的起止行。"""

        formatted = format_json_with_line_map({"a": {"b": 1}, "list": [True]})

        self.assertEqual(formatted.line_map[()], 0)
        self.assertEqual(formatted.line_map[("a",)], 1)
        self.assertEqual(formatted.line_map[("a", "b")], 2)
        self.assertEqual(formatted.line_map[("list",)], 4)
        self.assertEqual(formatted.line_map[("list", 0)], 5)
        self.assertEqual(formatted.span_map[()], (0, 7))

    def test_preview_value_handles_missing_and_truncation(self) -> None:
        """值预览应处理缺失值并截断过长文本。"""

        preview = preview_value("abcdefghijklmnopqrstuvwxyz", max_length=10)

        self.assertEqual(preview_value(MISSING), "-")
        self.assertEqual(len(preview), 10)
        self.assertTrue(preview.endswith("…"))


if __name__ == "__main__":
    unittest.main()
