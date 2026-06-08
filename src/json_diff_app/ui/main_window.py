from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any

from PySide6.QtCore import QRegularExpression, Qt, Slot
from PySide6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat, QTextCursor, QTextFormat
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QTableWidgetItem,
    QTextEdit,
)

from json_diff_app.core.diff_engine import (
    DiffItem,
    FormattedJson,
    compare_json,
    format_json_with_line_map,
    path_to_text,
    preview_value,
)
from json_diff_app.ui.generated.ui_main_window import Ui_MainWindow


KIND_LABELS = {
    "removed": "左侧独有",
    "added": "右侧新增",
    "changed": "值变化",
    "type_changed": "类型变化",
}

KIND_COLORS = {
    "removed": QColor("#ffe2e2"),
    "added": QColor("#dff7e7"),
    "changed": QColor("#fff0b8"),
    "type_changed": QColor("#eadfff"),
    "error": QColor("#ffd6d6"),
}


class MainWindow(QMainWindow):
    """JSON 比较器主窗口，负责界面交互、解析、比较和结果展示。"""

    def __init__(self) -> None:
        """初始化窗口、状态数据、语法高亮器和界面样式。"""

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._diffs: list[DiffItem] = []
        self._left_formatted: FormattedJson | None = None
        self._right_formatted: FormattedJson | None = None

        self._left_highlighter = JsonHighlighter(self.ui.leftEditor.document())
        self._right_highlighter = JsonHighlighter(self.ui.rightEditor.document())

        self._setup_ui()

    def _setup_ui(self) -> None:
        """配置窗口标题、控件尺寸、字体、快捷键和初始状态。"""

        self.setWindowTitle("JSON 比较器")
        self.ui.mainSplitter.setSizes([560, 220])
        self.ui.editorSplitter.setSizes([640, 640])

        self.ui.diffTable.setColumnWidth(0, 110)
        self.ui.diffTable.setColumnWidth(1, 260)
        self.ui.diffTable.setColumnWidth(2, 360)
        self.ui.diffTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.ui.diffTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.ui.diffTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.ui.diffTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.ui.diffTable.verticalHeader().setVisible(False)

        editor_font = QFont("Consolas", 10)
        editor_font.setStyleHint(QFont.StyleHint.Monospace)
        self.ui.leftEditor.setFont(editor_font)
        self.ui.rightEditor.setFont(editor_font)

        self.ui.compareButton.setShortcut("Ctrl+Return")
        self.ui.formatLeftButton.setShortcut("Ctrl+L")
        self.ui.formatRightButton.setShortcut("Ctrl+R")

        self._set_status(self.ui.leftStatusLabel, "等待输入", "muted")
        self._set_status(self.ui.rightStatusLabel, "等待输入", "muted")
        self.statusBar().showMessage("准备就绪")
        self._apply_style()

    @Slot()
    def on_compareButton_clicked(self) -> None:
        """响应比较按钮点击事件。"""

        self.compare()

    @Slot()
    def on_formatLeftButton_clicked(self) -> None:
        """响应左侧格式化按钮点击事件。"""

        self.format_side("left")

    @Slot()
    def on_formatRightButton_clicked(self) -> None:
        """响应右侧格式化按钮点击事件。"""

        self.format_side("right")

    @Slot()
    def on_openLeftButton_clicked(self) -> None:
        """响应左侧打开文件按钮点击事件。"""

        self.open_file("left")

    @Slot()
    def on_openRightButton_clicked(self) -> None:
        """响应右侧打开文件按钮点击事件。"""

        self.open_file("right")

    @Slot()
    def on_swapButton_clicked(self) -> None:
        """响应交换按钮点击事件。"""

        self.swap_json()

    @Slot()
    def on_clearButton_clicked(self) -> None:
        """响应清空按钮点击事件。"""

        self.clear_all()

    @Slot(int, int)
    def on_diffTable_cellClicked(self, row: int, column: int) -> None:
        """响应差异表格单元格点击事件。"""

        self.jump_to_diff(row, column)

    @Slot()
    def on_leftEditor_textChanged(self) -> None:
        """响应左侧编辑器文本变化事件。"""

        self._mark_edited("left")

    @Slot()
    def on_rightEditor_textChanged(self) -> None:
        """响应右侧编辑器文本变化事件。"""

        self._mark_edited("right")

    def compare(self) -> None:
        """解析左右 JSON，执行比较并刷新差异表格和高亮。"""

        self._clear_highlights()

        left_data = self._parse_editor("left", format_after_parse=True)
        if left_data is None:
            return

        right_data = self._parse_editor("right", format_after_parse=True)
        if right_data is None:
            return

        self._diffs = compare_json(left_data, right_data)
        self._populate_diff_table()
        self._highlight_diffs()

        if not self._diffs:
            self.ui.summaryLabel.setText("两个 JSON 完全一致")
            self.statusBar().showMessage("比较完成：没有差异")
            QMessageBox.information(self, "比较完成", "两个 JSON 完全一致。")
            return

        counts = Counter(diff.kind for diff in self._diffs)
        summary = (
            f"共 {len(self._diffs)} 处差异："
            f"左侧独有 {counts['removed']} / "
            f"右侧新增 {counts['added']} / "
            f"值变化 {counts['changed']} / "
            f"类型变化 {counts['type_changed']}"
        )
        self.ui.summaryLabel.setText(summary)
        self.statusBar().showMessage(f"比较完成：发现 {len(self._diffs)} 处差异")

    def format_side(self, side: str) -> None:
        """格式化指定一侧的 JSON 文本。"""

        if self._parse_editor(side, format_after_parse=True) is not None:
            label = "左侧" if side == "left" else "右侧"
            self.statusBar().showMessage(f"{label} JSON 格式化完成")

    def open_file(self, side: str) -> None:
        """打开本地 JSON 或文本文件并填充到指定编辑器。"""

        path, _ = QFileDialog.getOpenFileName(
            self,
            "打开 JSON 文件",
            "",
            "JSON 文件 (*.json);;文本文件 (*.txt);;所有文件 (*.*)",
        )
        if not path:
            return

        try:
            text = Path(path).read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            text = Path(path).read_text(encoding="gb18030")
        except OSError as exc:
            QMessageBox.critical(self, "打开失败", f"无法读取文件：\n{exc}")
            return

        editor = self._editor(side)
        editor.setPlainText(text)
        self._set_status(self._status_label(side), Path(path).name, "muted")
        self.statusBar().showMessage(f"已打开：{path}")

    def swap_json(self) -> None:
        """交换左右编辑器内容并清理已有比较结果。"""

        left = self.ui.leftEditor.toPlainText()
        right = self.ui.rightEditor.toPlainText()
        self.ui.leftEditor.setPlainText(right)
        self.ui.rightEditor.setPlainText(left)
        self._diffs.clear()
        self._clear_table()
        self._clear_highlights()
        self.ui.summaryLabel.setText("已交换左右 JSON，等待比较")
        self.statusBar().showMessage("已交换左右内容")

    def clear_all(self) -> None:
        """清空左右编辑器、差异结果和状态提示。"""

        self.ui.leftEditor.clear()
        self.ui.rightEditor.clear()
        self._diffs.clear()
        self._left_formatted = None
        self._right_formatted = None
        self._clear_table()
        self._clear_highlights()
        self._set_status(self.ui.leftStatusLabel, "等待输入", "muted")
        self._set_status(self.ui.rightStatusLabel, "等待输入", "muted")
        self.ui.summaryLabel.setText("尚未比较")
        self.statusBar().showMessage("已清空")

    def jump_to_diff(self, row: int, _column: int) -> None:
        """根据表格行号跳转到对应差异在编辑器中的位置。"""

        if row < 0 or row >= len(self._diffs):
            return

        diff = self._diffs[row]
        if diff.kind in {"removed", "changed", "type_changed"}:
            self._scroll_to_path(self.ui.leftEditor, self._left_formatted, diff.path)
        if diff.kind in {"added", "changed", "type_changed"}:
            self._scroll_to_path(self.ui.rightEditor, self._right_formatted, diff.path)

    def _parse_editor(self, side: str, format_after_parse: bool) -> Any | None:
        """解析指定编辑器中的 JSON，并可在成功后回写格式化文本。"""

        editor = self._editor(side)
        status_label = self._status_label(side)
        text = editor.toPlainText().strip()
        label = "左侧" if side == "left" else "右侧"

        if not text:
            self._set_status(status_label, "内容为空", "error")
            QMessageBox.warning(self, "解析失败", f"{label} JSON 为空。")
            return None

        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            message = f"{label} JSON 解析失败：第 {exc.lineno} 行，第 {exc.colno} 列。\n\n{exc.msg}"
            self._set_status(status_label, f"解析失败：{exc.lineno}:{exc.colno}", "error")
            self._highlight_error_line(editor, exc.lineno - 1)
            self.statusBar().showMessage(f"{label} JSON 解析失败")
            QMessageBox.warning(self, "解析失败", message)
            return None

        formatted = format_json_with_line_map(data)
        if format_after_parse:
            editor.blockSignals(True)
            editor.setPlainText(formatted.text)
            editor.blockSignals(False)

        if side == "left":
            self._left_formatted = formatted
        else:
            self._right_formatted = formatted

        self._set_status(status_label, "解析成功", "success")
        return data

    def _populate_diff_table(self) -> None:
        """把当前差异列表渲染到结果表格中。"""

        self._clear_table()
        self.ui.diffTable.setRowCount(len(self._diffs))

        for row, diff in enumerate(self._diffs):
            values = [
                KIND_LABELS[diff.kind],
                path_to_text(diff.path),
                preview_value(diff.left_value),
                preview_value(diff.right_value),
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if column == 0:
                    item.setBackground(KIND_COLORS[diff.kind])
                self.ui.diffTable.setItem(row, column, item)

    def _highlight_diffs(self) -> None:
        """根据差异类型在左右编辑器中高亮对应行。"""

        left_selections: list[QTextEdit.ExtraSelection] = []
        right_selections: list[QTextEdit.ExtraSelection] = []

        for diff in self._diffs:
            if diff.kind in {"removed", "changed", "type_changed"}:
                left_selections.extend(self._selections_for_path(self.ui.leftEditor, self._left_formatted, diff))
            if diff.kind in {"added", "changed", "type_changed"}:
                right_selections.extend(self._selections_for_path(self.ui.rightEditor, self._right_formatted, diff))

        self.ui.leftEditor.setExtraSelections(left_selections)
        self.ui.rightEditor.setExtraSelections(right_selections)

    def _selections_for_path(
        self,
        editor: QPlainTextEdit,
        formatted: FormattedJson | None,
        diff: DiffItem,
    ) -> list[QTextEdit.ExtraSelection]:
        """为单个差异路径生成编辑器高亮选区。"""

        if formatted is None:
            return []

        start, end = formatted.span_map.get(diff.path, (None, None))
        if start is None or end is None:
            return []

        color = KIND_COLORS[diff.kind]
        selections: list[QTextEdit.ExtraSelection] = []
        for line in range(start, end + 1):
            selections.append(self._line_selection(editor, line, color))
        return selections

    def _highlight_error_line(self, editor: QPlainTextEdit, line: int) -> None:
        """高亮解析错误所在行并滚动到该行。"""

        editor.setExtraSelections([self._line_selection(editor, max(line, 0), KIND_COLORS["error"])])
        self._scroll_to_line(editor, max(line, 0))

    def _line_selection(self, editor: QPlainTextEdit, line: int, color: QColor) -> QTextEdit.ExtraSelection:
        """创建覆盖整行的文本高亮选区。"""

        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(color)
        selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        block = editor.document().findBlockByNumber(line)
        selection.cursor = QTextCursor(block)
        selection.cursor.clearSelection()
        return selection

    def _scroll_to_path(
        self,
        editor: QPlainTextEdit,
        formatted: FormattedJson | None,
        path: tuple[str | int, ...],
    ) -> None:
        """滚动指定编辑器到 JSON 路径对应的行。"""

        if formatted is None:
            return
        line = formatted.line_map.get(path)
        if line is None:
            return
        self._scroll_to_line(editor, line)

    def _scroll_to_line(self, editor: QPlainTextEdit, line: int) -> None:
        """滚动指定编辑器到给定的文本行。"""

        block = editor.document().findBlockByNumber(line)
        if not block.isValid():
            return
        cursor = QTextCursor(block)
        editor.setTextCursor(cursor)
        editor.centerCursor()
        editor.setFocus()

    def _mark_edited(self, side: str) -> None:
        """标记指定侧内容已被用户修改，并清除旧格式化映射。"""

        self._set_status(self._status_label(side), "已修改", "muted")
        if side == "left":
            self._left_formatted = None
        else:
            self._right_formatted = None

    def _clear_table(self) -> None:
        """清空差异结果表格。"""

        self.ui.diffTable.setRowCount(0)

    def _clear_highlights(self) -> None:
        """清空左右编辑器中的所有额外高亮。"""

        self.ui.leftEditor.setExtraSelections([])
        self.ui.rightEditor.setExtraSelections([])

    def _editor(self, side: str) -> QPlainTextEdit:
        """根据侧别返回对应的 JSON 编辑器。"""

        return self.ui.leftEditor if side == "left" else self.ui.rightEditor

    def _status_label(self, side: str) -> QLabel:
        """根据侧别返回对应的状态标签。"""

        return self.ui.leftStatusLabel if side == "left" else self.ui.rightStatusLabel

    def _set_status(self, label: QLabel, text: str, state: str) -> None:
        """设置状态标签文本和样式状态。"""

        label.setText(text)
        label.setProperty("state", state)
        label.style().unpolish(label)
        label.style().polish(label)

    def _apply_style(self) -> None:
        """应用主窗口和子控件的样式表。"""

        self.setStyleSheet(
            """
            QMainWindow {
                background: #f5f7fb;
                color: #1f2937;
            }
            QFrame#headerPanel, QFrame#leftPanel, QFrame#rightPanel, QFrame#resultPanel {
                background: #ffffff;
                border: 1px solid #dce3ef;
                border-radius: 8px;
            }
            QLabel#titleLabel {
                font-size: 22px;
                font-weight: 700;
                color: #111827;
            }
            QLabel#subtitleLabel, QLabel#legendLabel {
                color: #667085;
            }
            QLabel#leftTitleLabel, QLabel#rightTitleLabel, QLabel#resultTitleLabel {
                font-size: 15px;
                font-weight: 700;
                color: #111827;
            }
            QLabel#summaryLabel {
                color: #4b5563;
                padding-left: 10px;
            }
            QLabel[state="muted"] {
                color: #6b7280;
                background: #eef2f7;
                border-radius: 4px;
                padding: 3px 8px;
            }
            QLabel[state="success"] {
                color: #116329;
                background: #dff7e7;
                border-radius: 4px;
                padding: 3px 8px;
            }
            QLabel[state="error"] {
                color: #9f1239;
                background: #ffe2e2;
                border-radius: 4px;
                padding: 3px 8px;
            }
            QPushButton {
                background: #ffffff;
                border: 1px solid #cfd8e6;
                border-radius: 6px;
                padding: 7px 12px;
                color: #1f2937;
            }
            QPushButton:hover {
                background: #f1f5fb;
                border-color: #aebbd0;
            }
            QPushButton:pressed {
                background: #e7edf7;
            }
            QPushButton#compareButton {
                background: #2563eb;
                border-color: #2563eb;
                color: #ffffff;
                font-weight: 700;
            }
            QPushButton#compareButton:hover {
                background: #1d4ed8;
            }
            QPlainTextEdit {
                background: #fbfdff;
                border: 1px solid #dce3ef;
                border-radius: 6px;
                color: #1f2937;
                padding: 8px;
                selection-background-color: #bfdbfe;
                selection-color: #111827;
            }
            QTableWidget {
                background: #ffffff;
                border: 1px solid #dce3ef;
                border-radius: 6px;
                selection-background-color: #dbeafe;
                selection-color: #111827;
            }
            QHeaderView::section {
                background: #f3f6fb;
                border: none;
                border-bottom: 1px solid #dce3ef;
                padding: 7px 8px;
                font-weight: 700;
                color: #374151;
            }
            QTableWidget::item {
                border-bottom: 1px solid #edf1f7;
                padding: 6px 8px;
            }
            QSplitter::handle {
                background: #e5ebf5;
            }
            QStatusBar {
                color: #4b5563;
            }
            """
        )


class JsonHighlighter(QSyntaxHighlighter):
    """为 JSON 编辑器提供字符串、键、数字和关键字语法高亮。"""

    def __init__(self, parent: Any) -> None:
        """初始化语法高亮规则。"""

        super().__init__(parent)
        self._rules = self._build_rules()

    def highlightBlock(self, text: str) -> None:
        """对当前文本块应用所有 JSON 语法高亮规则。"""

        for pattern, text_format in self._rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), text_format)

    def _build_rules(self) -> list[tuple[QRegularExpression, QTextCharFormat]]:
        """构建 JSON 语法高亮所需的正则表达式和文本格式。"""

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#0f766e"))

        key_format = QTextCharFormat()
        key_format.setForeground(QColor("#1d4ed8"))
        key_format.setFontWeight(QFont.Weight.DemiBold)

        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#b45309"))

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#7c3aed"))
        keyword_format.setFontWeight(QFont.Weight.DemiBold)

        return [
            (QRegularExpression(r'"(?:\\.|[^"\\])*"'), string_format),
            (QRegularExpression(r'"(?:\\.|[^"\\])*"(?=\s*:)'), key_format),
            (QRegularExpression(r"(?<![\w.])-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?(?![\w.])"), number_format),
            (QRegularExpression(r"\b(?:true|false|null)\b"), keyword_format),
        ]


def run() -> int:
    """创建 Qt 应用并启动主窗口事件循环。"""

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()
