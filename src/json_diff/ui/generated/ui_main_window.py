# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSplitter,
    QStatusBar, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 820)
        MainWindow.setMinimumSize(QSize(980, 680))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(14)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(18, 18, 18, 14)
        self.headerPanel = QFrame(self.centralwidget)
        self.headerPanel.setObjectName(u"headerPanel")
        self.headerPanel.setFrameShape(QFrame.Shape.NoFrame)
        self.headerLayout = QHBoxLayout(self.headerPanel)
        self.headerLayout.setSpacing(10)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(16, 12, 16, 12)
        self.titleLayout = QVBoxLayout()
        self.titleLayout.setSpacing(2)
        self.titleLayout.setObjectName(u"titleLayout")
        self.titleLabel = QLabel(self.headerPanel)
        self.titleLabel.setObjectName(u"titleLabel")

        self.titleLayout.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel(self.headerPanel)
        self.subtitleLabel.setObjectName(u"subtitleLabel")

        self.titleLayout.addWidget(self.subtitleLabel)


        self.headerLayout.addLayout(self.titleLayout)

        self.headerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)

        self.openLeftButton = QPushButton(self.headerPanel)
        self.openLeftButton.setObjectName(u"openLeftButton")

        self.headerLayout.addWidget(self.openLeftButton)

        self.openRightButton = QPushButton(self.headerPanel)
        self.openRightButton.setObjectName(u"openRightButton")

        self.headerLayout.addWidget(self.openRightButton)

        self.swapButton = QPushButton(self.headerPanel)
        self.swapButton.setObjectName(u"swapButton")

        self.headerLayout.addWidget(self.swapButton)

        self.clearButton = QPushButton(self.headerPanel)
        self.clearButton.setObjectName(u"clearButton")

        self.headerLayout.addWidget(self.clearButton)

        self.compareButton = QPushButton(self.headerPanel)
        self.compareButton.setObjectName(u"compareButton")

        self.headerLayout.addWidget(self.compareButton)


        self.rootLayout.addWidget(self.headerPanel)

        self.mainSplitter = QSplitter(self.centralwidget)
        self.mainSplitter.setObjectName(u"mainSplitter")
        self.mainSplitter.setOrientation(Qt.Orientation.Vertical)
        self.mainSplitter.setChildrenCollapsible(False)
        self.editorSplitter = QSplitter(self.mainSplitter)
        self.editorSplitter.setObjectName(u"editorSplitter")
        self.editorSplitter.setOrientation(Qt.Orientation.Horizontal)
        self.editorSplitter.setChildrenCollapsible(False)
        self.leftPanel = QFrame(self.editorSplitter)
        self.leftPanel.setObjectName(u"leftPanel")
        self.leftPanel.setFrameShape(QFrame.Shape.NoFrame)
        self.leftLayout = QVBoxLayout(self.leftPanel)
        self.leftLayout.setSpacing(8)
        self.leftLayout.setObjectName(u"leftLayout")
        self.leftLayout.setContentsMargins(12, 12, 12, 12)
        self.leftHeaderLayout = QHBoxLayout()
        self.leftHeaderLayout.setSpacing(8)
        self.leftHeaderLayout.setObjectName(u"leftHeaderLayout")
        self.leftTitleLabel = QLabel(self.leftPanel)
        self.leftTitleLabel.setObjectName(u"leftTitleLabel")

        self.leftHeaderLayout.addWidget(self.leftTitleLabel)

        self.leftHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.leftHeaderLayout.addItem(self.leftHeaderSpacer)

        self.leftStatusLabel = QLabel(self.leftPanel)
        self.leftStatusLabel.setObjectName(u"leftStatusLabel")

        self.leftHeaderLayout.addWidget(self.leftStatusLabel)

        self.formatLeftButton = QPushButton(self.leftPanel)
        self.formatLeftButton.setObjectName(u"formatLeftButton")

        self.leftHeaderLayout.addWidget(self.formatLeftButton)


        self.leftLayout.addLayout(self.leftHeaderLayout)

        self.leftEditor = QPlainTextEdit(self.leftPanel)
        self.leftEditor.setObjectName(u"leftEditor")
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(10)
        self.leftEditor.setFont(font)
        self.leftEditor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.leftLayout.addWidget(self.leftEditor)

        self.editorSplitter.addWidget(self.leftPanel)
        self.rightPanel = QFrame(self.editorSplitter)
        self.rightPanel.setObjectName(u"rightPanel")
        self.rightPanel.setFrameShape(QFrame.Shape.NoFrame)
        self.rightLayout = QVBoxLayout(self.rightPanel)
        self.rightLayout.setSpacing(8)
        self.rightLayout.setObjectName(u"rightLayout")
        self.rightLayout.setContentsMargins(12, 12, 12, 12)
        self.rightHeaderLayout = QHBoxLayout()
        self.rightHeaderLayout.setSpacing(8)
        self.rightHeaderLayout.setObjectName(u"rightHeaderLayout")
        self.rightTitleLabel = QLabel(self.rightPanel)
        self.rightTitleLabel.setObjectName(u"rightTitleLabel")

        self.rightHeaderLayout.addWidget(self.rightTitleLabel)

        self.rightHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.rightHeaderLayout.addItem(self.rightHeaderSpacer)

        self.rightStatusLabel = QLabel(self.rightPanel)
        self.rightStatusLabel.setObjectName(u"rightStatusLabel")

        self.rightHeaderLayout.addWidget(self.rightStatusLabel)

        self.formatRightButton = QPushButton(self.rightPanel)
        self.formatRightButton.setObjectName(u"formatRightButton")

        self.rightHeaderLayout.addWidget(self.formatRightButton)


        self.rightLayout.addLayout(self.rightHeaderLayout)

        self.rightEditor = QPlainTextEdit(self.rightPanel)
        self.rightEditor.setObjectName(u"rightEditor")
        self.rightEditor.setFont(font)
        self.rightEditor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.rightLayout.addWidget(self.rightEditor)

        self.editorSplitter.addWidget(self.rightPanel)
        self.mainSplitter.addWidget(self.editorSplitter)
        self.resultPanel = QFrame(self.mainSplitter)
        self.resultPanel.setObjectName(u"resultPanel")
        self.resultPanel.setFrameShape(QFrame.Shape.NoFrame)
        self.resultLayout = QVBoxLayout(self.resultPanel)
        self.resultLayout.setSpacing(8)
        self.resultLayout.setObjectName(u"resultLayout")
        self.resultLayout.setContentsMargins(12, 12, 12, 12)
        self.resultHeaderLayout = QHBoxLayout()
        self.resultHeaderLayout.setSpacing(8)
        self.resultHeaderLayout.setObjectName(u"resultHeaderLayout")
        self.resultTitleLabel = QLabel(self.resultPanel)
        self.resultTitleLabel.setObjectName(u"resultTitleLabel")

        self.resultHeaderLayout.addWidget(self.resultTitleLabel)

        self.summaryLabel = QLabel(self.resultPanel)
        self.summaryLabel.setObjectName(u"summaryLabel")

        self.resultHeaderLayout.addWidget(self.summaryLabel)

        self.resultHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.resultHeaderLayout.addItem(self.resultHeaderSpacer)

        self.legendLabel = QLabel(self.resultPanel)
        self.legendLabel.setObjectName(u"legendLabel")

        self.resultHeaderLayout.addWidget(self.legendLabel)


        self.resultLayout.addLayout(self.resultHeaderLayout)

        self.diffTable = QTableWidget(self.resultPanel)
        if (self.diffTable.columnCount() < 4):
            self.diffTable.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.diffTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.diffTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.diffTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.diffTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.diffTable.setObjectName(u"diffTable")
        self.diffTable.setAlternatingRowColors(False)
        self.diffTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.diffTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.diffTable.setShowGrid(False)
        self.diffTable.horizontalHeader().setStretchLastSection(True)

        self.resultLayout.addWidget(self.diffTable)

        self.mainSplitter.addWidget(self.resultPanel)

        self.rootLayout.addWidget(self.mainSplitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.compareButton.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"JSON Diff", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"JSON \u6bd4\u8f83\u5668", None))
        self.subtitleLabel.setText(QCoreApplication.translate("MainWindow", u"\u7c98\u8d34\u6216\u6253\u5f00\u4e24\u4e2a JSON\uff0c\u683c\u5f0f\u5316\u540e\u6bd4\u8f83\u7ed3\u6784\u548c\u503c\u7684\u5dee\u5f02", None))
        self.openLeftButton.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u5de6\u4fa7", None))
        self.openRightButton.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u53f3\u4fa7", None))
        self.swapButton.setText(QCoreApplication.translate("MainWindow", u"\u4ea4\u6362", None))
        self.clearButton.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7a7a", None))
        self.compareButton.setText(QCoreApplication.translate("MainWindow", u"\u6bd4\u8f83 JSON", None))
        self.leftTitleLabel.setText(QCoreApplication.translate("MainWindow", u"\u5de6\u4fa7 JSON", None))
        self.leftStatusLabel.setText(QCoreApplication.translate("MainWindow", u"\u7b49\u5f85\u8f93\u5165", None))
        self.formatLeftButton.setText(QCoreApplication.translate("MainWindow", u"\u683c\u5f0f\u5316", None))
        self.leftEditor.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u5728\u8fd9\u91cc\u7c98\u8d34\u5de6\u4fa7 JSON", None))
        self.rightTitleLabel.setText(QCoreApplication.translate("MainWindow", u"\u53f3\u4fa7 JSON", None))
        self.rightStatusLabel.setText(QCoreApplication.translate("MainWindow", u"\u7b49\u5f85\u8f93\u5165", None))
        self.formatRightButton.setText(QCoreApplication.translate("MainWindow", u"\u683c\u5f0f\u5316", None))
        self.rightEditor.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u5728\u8fd9\u91cc\u7c98\u8d34\u53f3\u4fa7 JSON", None))
        self.resultTitleLabel.setText(QCoreApplication.translate("MainWindow", u"\u5dee\u5f02\u660e\u7ec6", None))
        self.summaryLabel.setText(QCoreApplication.translate("MainWindow", u"\u5c1a\u672a\u6bd4\u8f83", None))
        self.legendLabel.setText(QCoreApplication.translate("MainWindow", u"\u7ea2\u8272=\u5de6\u4fa7\u72ec\u6709\uff0c\u7eff\u8272=\u53f3\u4fa7\u65b0\u589e\uff0c\u9ec4\u8272=\u503c\u53d8\u5316\uff0c\u7d2b\u8272=\u7c7b\u578b\u53d8\u5316", None))
        ___qtablewidgetitem = self.diffTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u7c7b\u578b", None))
        ___qtablewidgetitem1 = self.diffTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u8def\u5f84", None))
        ___qtablewidgetitem2 = self.diffTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u5de6\u4fa7\u503c", None))
        ___qtablewidgetitem3 = self.diffTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u53f3\u4fa7\u503c", None))
    # retranslateUi

