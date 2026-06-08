from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Any


JsonPath = tuple[str | int, ...]


@dataclass(frozen=True)
class DiffItem:
    """表示一个 JSON 路径上的差异项。"""

    kind: str
    path: JsonPath
    left_value: Any
    right_value: Any


@dataclass(frozen=True)
class FormattedJson:
    """保存格式化后的 JSON 文本以及路径到行号的映射。"""

    text: str
    line_map: dict[JsonPath, int]
    span_map: dict[JsonPath, tuple[int, int]]


MISSING = object()


def compare_json(left: Any, right: Any) -> list[DiffItem]:
    """递归比较左右两个 JSON 值并返回差异列表。"""

    diffs: list[DiffItem] = []
    _compare_value(left, right, (), diffs)
    return diffs


def format_json_with_line_map(value: Any) -> FormattedJson:
    """格式化 JSON 值，并记录每个路径对应的起止行号。"""

    lines: list[str] = []
    line_map: dict[JsonPath, int] = {}
    span_map: dict[JsonPath, tuple[int, int]] = {}

    def emit(current: Any, path: JsonPath, indent: int, prefix: str = "") -> None:
        """递归输出当前值，并维护路径到文本行的映射。"""

        start = len(lines)
        line_map[path] = start
        pad = " " * indent

        if isinstance(current, dict):
            lines.append(f"{pad}{prefix}{{")
            items = list(current.items())
            for index, (key, child) in enumerate(items):
                child_prefix = f"{json.dumps(key, ensure_ascii=False)}: "
                emit(child, (*path, key), indent + 2, child_prefix)
                if index < len(items) - 1:
                    lines[-1] += ","
            lines.append(f"{pad}}}")
        elif isinstance(current, list):
            lines.append(f"{pad}{prefix}[")
            for index, child in enumerate(current):
                emit(child, (*path, index), indent + 2)
                if index < len(current) - 1:
                    lines[-1] += ","
            lines.append(f"{pad}]")
        else:
            lines.append(f"{pad}{prefix}{json.dumps(current, ensure_ascii=False)}")

        span_map[path] = (start, len(lines) - 1)

    emit(value, (), 0)
    return FormattedJson("\n".join(lines), line_map, span_map)


def path_to_text(path: JsonPath) -> str:
    """将内部 JSON 路径转换为用户可读的路径文本。"""

    if not path:
        return "$"

    text = "$"
    for segment in path:
        if isinstance(segment, int):
            text += f"[{segment}]"
        elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", segment):
            text += f".{segment}"
        else:
            text += f"[{json.dumps(segment, ensure_ascii=False)}]"
    return text


def preview_value(value: Any, max_length: int = 120) -> str:
    """生成适合在差异表格中展示的短值预览。"""

    if value is MISSING:
        return "-"

    try:
        text = json.dumps(value, ensure_ascii=False, separators=(",", ": "))
    except TypeError:
        text = str(value)

    text = text.replace("\n", " ")
    if len(text) <= max_length:
        return text
    return f"{text[: max_length - 1]}…"


def _compare_value(left: Any, right: Any, path: JsonPath, diffs: list[DiffItem]) -> None:
    """比较指定路径上的左右值，并把发现的差异追加到列表。"""

    if left is MISSING:
        diffs.append(DiffItem("added", path, MISSING, right))
        return
    if right is MISSING:
        diffs.append(DiffItem("removed", path, left, MISSING))
        return

    if _type_name(left) != _type_name(right):
        diffs.append(DiffItem("type_changed", path, left, right))
        return

    if isinstance(left, dict):
        left_keys = list(left.keys())
        right_keys = list(right.keys())
        ordered_keys = left_keys + [key for key in right_keys if key not in left]
        for key in ordered_keys:
            _compare_value(left.get(key, MISSING), right.get(key, MISSING), (*path, key), diffs)
        return

    if isinstance(left, list):
        max_length = max(len(left), len(right))
        for index in range(max_length):
            left_child = left[index] if index < len(left) else MISSING
            right_child = right[index] if index < len(right) else MISSING
            _compare_value(left_child, right_child, (*path, index), diffs)
        return

    if left != right:
        diffs.append(DiffItem("changed", path, left, right))


def _type_name(value: Any) -> str:
    """返回 JSON 语义下的类型名称。"""

    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__
