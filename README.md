# JSON Diff

一个基于 **PySide6** 的桌面端 JSON 比较器。

它适合在接口联调、配置排查、数据验收和日常开发中快速对比两份 JSON：左侧和右侧可以直接粘贴内容，也可以打开本地文件；程序会自动格式化 JSON、递归比较结构和值，并在编辑器和差异表格中同步展示结果。

## 项目亮点

- **左右并排编辑**：同时查看两份 JSON，支持粘贴和打开本地文件。
- **一键格式化**：解析成功后以统一缩进格式展示，方便阅读和定位。
- **递归结构比较**：支持对象、数组、字符串、数字、布尔值、`null` 等 JSON 类型。
- **差异类型清晰**：区分左侧独有、右侧新增、值变化和类型变化。
- **行级高亮定位**：在编辑器中高亮差异所在行，点击表格可跳转到对应位置。
- **解析错误提示**：JSON 格式错误时展示具体行列，并高亮错误行。
- **自动信号槽连接**：窗口交互使用 PySide6 的 `on_对象名_事件名` 自动连接约定，减少手工连接代码。

## 截图说明

当前项目未内置截图资源。运行程序后，你会看到左右两个 JSON 编辑区和下方差异明细表：

- 左侧独有：红色
- 右侧新增：绿色
- 值变化：黄色
- 类型变化：紫色

## 目录结构

```text
json_diff/
├─ main.py                              # 根目录兼容启动器
├─ pyproject.toml                       # 项目元数据和依赖配置
├─ README.md                            # 项目说明文档
├─ tests/
│  └─ test_diff_engine.py               # JSON 比较核心逻辑测试
└─ src/
   └─ json_diff_app/
      ├─ main.py                        # 包入口
      ├─ core/
      │  └─ diff_engine.py              # JSON 比较、路径格式化和行号映射
      └─ ui/
         ├─ main_window.py              # 主窗口、槽函数和界面行为
         ├─ forms/
         │  └─ main_window.ui           # Qt Designer 表单源文件
         └─ generated/
            └─ ui_main_window.py        # 由 .ui 生成的 Python 代码
```

## 环境要求

- Python `>= 3.14`
- PySide6 `>= 6.11.1`
- 推荐使用 `uv` 管理依赖和运行环境

## 安装依赖

使用 `uv`：

```powershell
uv sync
```

或使用普通 `pip`：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
```

## 运行项目

从项目根目录直接运行：

```powershell
python main.py
```

如果已经安装为可编辑包，也可以使用命令行入口：

```powershell
json-diff
```

## 使用方式

1. 在左侧和右侧编辑器中粘贴 JSON，或点击“打开左侧”“打开右侧”选择本地文件。
2. 点击“格式化”可以单独格式化某一侧 JSON。
3. 点击“比较 JSON”开始比较。
4. 查看下方差异明细表，点击任意差异行会跳转到对应 JSON 位置。
5. 点击“交换”可互换左右内容，点击“清空”可重置界面。

## 快捷键

- `Ctrl + Return`：比较 JSON
- `Ctrl + L`：格式化左侧 JSON
- `Ctrl + R`：格式化右侧 JSON

## 测试

运行标准库单元测试：

```powershell
python -m unittest discover -s tests
```

运行语法检查：

```powershell
python -m compileall -q main.py src tests
```

GUI 冒烟测试可以在无显示环境中运行：

```powershell
$env:QT_QPA_PLATFORM="offscreen"
python -c "import sys; sys.path.insert(0, 'src'); from PySide6.QtWidgets import QApplication; from json_diff_app.ui.main_window import MainWindow; app=QApplication([]); window=MainWindow(); print(window.windowTitle()); window.close(); app.quit()"
```

## 重新生成 UI 代码

界面结构由 Qt Designer 表单维护：

```text
src/json_diff_app/ui/forms/main_window.ui
```

修改 `.ui` 后，使用下面的命令重新生成 Python 代码：

```powershell
pyside6-uic src/json_diff_app/ui/forms/main_window.ui -o src/json_diff_app/ui/generated/ui_main_window.py
```

注意：`src/json_diff_app/ui/generated/ui_main_window.py` 是生成文件，不建议手工修改。

## 信号槽约定

主窗口交互使用 PySide6 自动连接机制：

```python
on_对象名_事件名
```

例如：

- `on_compareButton_clicked`
- `on_openLeftButton_clicked`
- `on_diffTable_cellClicked`
- `on_leftEditor_textChanged`

这样可以让 `.ui` 文件中的对象名和 Python 槽函数自然对应，减少手写 `.connect(...)` 的维护成本。

## 作者

- 作者：屿你有关
- GitHub：[@yuniyouguan](https://github.com/yuniyouguan)
- 邮箱：niyouguanyu@gmail.com
- 组织：SpectacleHQ

## 项目描述

中文描述：基于 PySide6 的桌面端 JSON 比较器，支持格式化、递归差异比较、差异高亮和表格定位。

推荐 GitHub 仓库描述：

```text
基于 PySide6 的桌面端 JSON 比较器，支持格式化、递归差异比较、差异高亮和表格定位。
```
