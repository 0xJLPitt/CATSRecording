# -*- coding: utf-8 -*-
#
# CATS Webcamviewer — UI Layer
# Design: "APEX CONTROL" — dark sports analytics × gaming HUD
#
# Layout sizes match the original hospital-mode (ui_scale=0.5) exactly.
# All widget objectNames are preserved.

from app_config import CONFIG
from ui_theme import (
    S, BG_BASE, BG_RAISED, BG_SURFACE,
    CYAN, CYAN_DIM, CYAN_DARK, BLUE, ORANGE,
    PURPLE, PURPLE_DARK, RED,
    TEXT_BRIGHT, TEXT_BODY, TEXT_DIM,
    BORDER, BORDER_MID,
    FONT_UI, FONT_MONO,
)
from PyQt5 import QtCore, QtGui, QtWidgets
import pyautogui
import os

# ── Convenience: direct scale helpers matching original formula ────────────
def _fs(base):
    """font-size helper: int(base * ui_scale)"""
    return int(base * CONFIG['ui_scale'])


# ══════════════════════════════════════════════════════════════════
# Global QSS — APEX CONTROL theme
# All font sizes use the same formula as the original code so they
# scale correctly in hospital mode (ui_scale=0.5).
# ══════════════════════════════════════════════════════════════════
APP_QSS = f"""

/* ─── Base ─── */
QMainWindow, QWidget {{
    background-color: {BG_BASE};
    color: {TEXT_BODY};
    font-family: {FONT_UI};
}}

/* ─── Tab widget ─── */
QTabWidget::pane {{
    background: {BG_RAISED};
    border: 1px solid {BORDER};
    border-top: none;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}}
QTabBar {{
    background: transparent;
    border-bottom: 2px solid {BORDER};
}}
QTabBar::tab {{
    background: transparent;
    color: {TEXT_DIM};
    font-family: {FONT_UI};
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    padding: {int(8 * CONFIG['ui_scale'])}px {int(20 * CONFIG['ui_scale'])}px;
    min-width: 200px;
    min-height: {int(40 * CONFIG['ui_scale'])}px;
    border: none;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
}}
QTabBar::tab:selected {{
    color: {CYAN};
    border-bottom: 2px solid {CYAN};
}}
QTabBar::tab:hover:!selected {{
    color: {TEXT_BODY};
    border-bottom: 2px solid {BORDER_MID};
}}

/* ─── Sport-select buttons on Recording landing ─── */
QPushButton#Deadlift_btn_3,
QPushButton#Benchpress_btn_3,
QPushButton#Squat_btn_3 {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {BG_SURFACE}, stop:0.6 {BG_RAISED}, stop:1 {BG_BASE});
    color: {TEXT_BRIGHT};
    font-family: {FONT_UI};
    font-size: {_fs(24)}px;
    font-weight: 800;
    letter-spacing: 6px;
    text-transform: uppercase;
    border: 1px solid {BORDER_MID};
    border-left: 4px solid {CYAN};
    border-radius: 10px;
    padding-left: 28px;
    text-align: left;
}}
QPushButton#Deadlift_btn_3:hover,
QPushButton#Benchpress_btn_3:hover,
QPushButton#Squat_btn_3:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {CYAN_DARK}, stop:1 {BG_RAISED});
    border-left: 4px solid {CYAN};
    border-color: {CYAN};
    color: {CYAN};
}}
QPushButton#Deadlift_btn_3:pressed,
QPushButton#Benchpress_btn_3:pressed,
QPushButton#Squat_btn_3:pressed {{
    background: {CYAN_DARK};
}}

/* ─── Checkbox ─── */
QCheckBox {{
    color: {TEXT_DIM};
    font-size: 12px;
    spacing: 10px;
    letter-spacing: 1px;
}}
QCheckBox::indicator {{
    width: 16px; height: 16px;
    border: 2px solid {BORDER_MID};
    border-radius: 3px;
    background: {BG_SURFACE};
}}
QCheckBox::indicator:checked {{
    background: {CYAN};
    border-color: {CYAN};
}}
QCheckBox:disabled {{
    color: {TEXT_DIM};
}}

/* ─── Replay sport-switcher buttons ─── */
/* Font size matches original: int(36 * ui_scale) */
QPushButton#Deadlift_play_btn,
QPushButton#Benchpress_play_btn,
QPushButton#Squat_play_btn {{
    background: {BG_SURFACE};
    color: {TEXT_BODY};
    font-family: {FONT_UI};
    font-size: {_fs(36)}px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    border: 1px solid {BORDER};
    border-bottom: 3px solid {BORDER};
    border-radius: 6px;
    padding: 6px 14px;
}}
QPushButton#Deadlift_play_btn:hover,
QPushButton#Benchpress_play_btn:hover,
QPushButton#Squat_play_btn:hover {{
    border-color: {CYAN};
    border-bottom-color: {CYAN};
    color: {CYAN};
    background: {CYAN_DARK};
}}
QPushButton#Deadlift_play_btn:pressed,
QPushButton#Benchpress_play_btn:pressed,
QPushButton#Squat_play_btn:pressed {{
    background: {BG_RAISED};
}}

/* ─── ComboBox (File_comboBox, fast_forward_combobox) ─── */
QComboBox {{
    background: {BG_SURFACE};
    color: {TEXT_BRIGHT};
    font-family: {FONT_UI};
    font-size: {_fs(28)}px;
    font-weight: 700;
    letter-spacing: 1px;
    border: 1px solid {BORDER_MID};
    border-radius: 6px;
    padding: {int(8 * CONFIG['ui_scale'])}px {int(16 * CONFIG['ui_scale'])}px;
    selection-background-color: {CYAN_DARK};
}}
QComboBox:hover {{
    border-color: {CYAN_DIM};
}}
QComboBox:focus {{
    border-color: {CYAN};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox QAbstractItemView {{
    background: {BG_RAISED};
    color: {TEXT_BRIGHT};
    border: 1px solid {BORDER_MID};
    selection-background-color: {CYAN_DARK};
    outline: none;
    padding: 4px;
}}

/* ─── Search LineEdit ─── */
QLineEdit#search_LineEdit {{
    background: {BG_SURFACE};
    color: {TEXT_BODY};
    font-family: {FONT_UI};
    font-size: {_fs(28)}px;
    font-weight: 700;
    letter-spacing: 1px;
    border: 1px solid {BORDER_MID};
    border-radius: 6px;
    padding: {int(8 * CONFIG['ui_scale'])}px {int(16 * CONFIG['ui_scale'])}px;
}}
QLineEdit#search_LineEdit:focus {{
    border-color: {CYAN};
    color: {TEXT_BRIGHT};
}}

/* ─── Data produce button (replay tab) ─── */
/* Font size: int(20 * ui_scale), same as original */
QPushButton#data_produce_btn_rp {{
    background: transparent;
    color: {CYAN};
    font-family: {FONT_UI};
    font-size: {_fs(20)}px;
    font-weight: 700;
    letter-spacing: 1px;
    border: 1px solid {CYAN};
    border-radius: 6px;
    padding: 4px 16px;
}}
QPushButton#data_produce_btn_rp:hover {{
    background: {CYAN_DARK};
    color: {TEXT_BRIGHT};
}}

/* ─── Video area groupbox ─── */
QGroupBox#play_groupBox {{
    background: {BG_RAISED};
    border: 1px solid {BORDER};
    border-radius: 10px;
    margin-top: 0px;
    padding: 6px;
}}
QGroupBox#play_groupBox::title {{ color: transparent; }}

/* ─── Time counter (monospace readout) ─── */
QLineEdit#TimeCount_LineEdit {{
    background: transparent;
    color: {CYAN};
    font-family: {FONT_MONO};
    font-size: 14px;
    font-weight: 700;
    border: none;
    letter-spacing: 2px;
}}

/* ─── Frame slider ─── */
QSlider::groove:horizontal {{
    height: 5px;
    background: {BG_SURFACE};
    border-radius: 3px;
    border: none;
}}
QSlider::sub-page:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {BLUE}, stop:1 {CYAN});
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    background: {TEXT_BRIGHT};
    border: 2px solid {CYAN};
    width: 14px; height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}}
QSlider::handle:horizontal:hover {{
    background: {CYAN};
}}
QSlider::handle:horizontal:disabled {{
    background: {TEXT_DIM};
    border-color: {BORDER_MID};
}}
QSlider::groove:horizontal:disabled {{
    background: {BG_RAISED};
}}

/* ─── Loop / Clear buttons ─── */
QPushButton#LoopA_btn,
QPushButton#LoopB_btn {{
    background: transparent;
    color: {PURPLE};
    font-family: {FONT_UI};
    font-size: {_fs(22)}px;
    font-weight: 700;
    border: 1px solid {PURPLE};
    border-radius: 5px;
    padding: {int(8 * CONFIG['ui_scale'])}px {int(16 * CONFIG['ui_scale'])}px;
}}
QPushButton#LoopA_btn:hover,
QPushButton#LoopB_btn:hover {{
    background: {PURPLE_DARK};
    color: {TEXT_BRIGHT};
}}
QPushButton#ClearLoop_btn {{
    background: transparent;
    color: {RED};
    font-family: {FONT_UI};
    font-size: {_fs(22)}px;
    font-weight: 700;
    border: 1px solid {RED};
    border-radius: 5px;
    padding: {int(8 * CONFIG['ui_scale'])}px {int(16 * CONFIG['ui_scale'])}px;
}}
QPushButton#ClearLoop_btn:hover {{
    background: rgba(239,68,68,0.10);
    color: {TEXT_BRIGHT};
}}

/* ─── Tool buttons (Play / Stop) ─── */
QToolButton {{
    background: {BG_SURFACE};
    border: 1px solid {BORDER_MID};
    border-bottom: 3px solid {BORDER_MID};
    border-radius: 8px;
}}
QToolButton:hover {{
    border-color: {CYAN};
    border-bottom-color: {CYAN};
    background: {CYAN_DARK};
}}
QToolButton:pressed {{
    background: #001824;
    border-bottom-width: 1px;
}}
QToolButton:disabled {{
    background: {BG_RAISED};
    border-color: {BORDER};
    border-bottom-color: {BORDER};
}}

/* ─── Read-only vision label line edits ─── */
QLineEdit[readOnly="true"] {{
    background: transparent;
    color: {CYAN};
    font-family: {FONT_MONO};
    font-weight: 700;
    border: none;
    letter-spacing: 2px;
}}

/* ─── Status bar ─── */
QStatusBar {{
    background: {BG_BASE};
    color: {TEXT_DIM};
    font-family: {FONT_UI};
    font-size: 11px;
    border-top: 1px solid {BORDER};
}}

/* ─── Scrollbars ─── */
QScrollBar:vertical {{
    background: {BG_BASE};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER_MID};
    border-radius: 3px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{ background: {CYAN_DIM}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: {BG_BASE};
    height: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:horizontal {{
    background: {BORDER_MID};
    border-radius: 3px;
    min-width: 24px;
}}
QScrollBar::handle:horizontal:hover {{ background: {CYAN_DIM}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
"""


# ══════════════════════════════════════════════════════════════════
# Ui_MainWindow
# ══════════════════════════════════════════════════════════════════
class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        screen_width, screen_height = pyautogui.size()
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("CATS Webcamviewer")
        MainWindow.setStyleSheet(APP_QSS)

        sz_pol = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sz_pol.setHorizontalStretch(0)
        sz_pol.setVerticalStretch(0)
        sz_pol.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())\

        MainWindow.setSizePolicy(sz_pol)
        MainWindow.setMinimumSize(QtCore.QSize(screen_width, screen_height))

        space_10 = screen_width / 256

        # ── Central widget ─────────────────────────────────────
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(space_10, space_10, space_10, space_10)

        # ── Tab widget ─────────────────────────────────────────
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabs.setObjectName("replay_tabWidget")
        self.tabs.setDocumentMode(True)
        self.tabs.setTabBarAutoHide(False)
        self.tabs.tabBar().setExpanding(False)

        # ══════════════════════════════════════════════════════
        #  RECORDING TAB
        # ══════════════════════════════════════════════════════
        self.Recording_tab = QtWidgets.QWidget()
        self.Recording_tab.setObjectName("Recording_tab")

        # Margins identical to original
        self.recording_layout = QtWidgets.QVBoxLayout(self.Recording_tab)
        self.recording_layout.setContentsMargins(10, 10, 10, 10)

        # Grid for sport buttonstructure as original
        self.grid_Layout_recording = QtWidgets.QGridLayout()
        self.grid_Layout_recording.setContentsMargins(0, 0, 0, 0)

        # Checkbox
        self.manual_checkbox = QtWidgets.QCheckBox(self.Recording_tab)
        self.manual_checkbox.setObjectName("manual_checkbox")
        self.manual_checkbox.setEnabled(False)
        self.manual_checkbox.setChecked(True)
        self.grid_Layout_recording.addWidget(self.manual_checkbox, 0, 0, 1, 1)

        # Sport buttons — EXACT same fixed sizes as original
        self.rc_Deadlift_btn = QtWidgets.QPushButton(self.Recording_tab)
        self.rc_Deadlift_btn.setObjectName("Deadlift_btn_3")
        self.rc_Deadlift_btn.setText("Deadlift")
        self.rc_Deadlift_btn.setFixedSize(
            int(800 * CONFIG['ui_scale']), int(120 * CONFIG['ui_scale']))
        self.grid_Layout_recording.addWidget(self.rc_Deadlift_btn, 1, 0, 1, 1)

        self.rc_Benchpress_btn = QtWidgets.QPushButton(self.Recording_tab)
        self.rc_Benchpress_btn.setObjectName("Benchpress_btn_3")
        self.rc_Benchpress_btn.setText("Benchpress")
        self.rc_Benchpress_btn.setFixedSize(
            int(800 * CONFIG['ui_scale']), int(120 * CONFIG['ui_scale']))
        self.grid_Layout_recording.addWidget(self.rc_Benchpress_btn, 2, 0, 1, 1)

        self.rc_Squat_btn = QtWidgets.QPushButton(self.Recording_tab)
        self.rc_Squat_btn.setObjectName("Squat_btn_3")
        self.rc_Squat_btn.setText("Squat")
        self.rc_Squat_btn.setFixedSize(
            int(800 * CONFIG['ui_scale']), int(120 * CONFIG['ui_scale']))
        self.grid_Layout_recording.addWidget(self.rc_Squat_btn, 3, 0, 1, 1)

        self.recording_layout.addLayout(self.grid_Layout_recording)

        # ══════════════════════════════════════════════════════
        #  REPLAY TAB
        # ══════════════════════════════════════════════════════
        self.Replay_tab = QtWidgets.QWidget()
        self.Replay_tab.setObjectName("Replay_tab")

        # Margins identical to original
        self.replay_layout = QtWidgets.QVBoxLayout(self.Replay_tab)
        self.replay_layout.setContentsMargins(10, 10, 10, 10)

        # ── Top controls — plain HBoxLayout (no frame, same as original) ─
        self.top_controls_layout = QtWidgets.QHBoxLayout()

        # Sport switcher buttons — no individual setStyleSheet; QSS handles it
        self.rp_Deadlift_btn = QtWidgets.QPushButton(self.Replay_tab)
        self.rp_Deadlift_btn.setObjectName("Deadlift_play_btn")
        self.top_controls_layout.addWidget(self.rp_Deadlift_btn)

        self.rp_Benchpress_btn = QtWidgets.QPushButton(self.Replay_tab)
        self.rp_Benchpress_btn.setObjectName("Benchpress_play_btn")
        self.top_controls_layout.addWidget(self.rp_Benchpress_btn)

        self.rp_Squat_btn = QtWidgets.QPushButton(self.Replay_tab)
        self.rp_Squat_btn.setObjectName("Squat_play_btn")
        self.top_controls_layout.addWidget(self.rp_Squat_btn)

        # File combo — same fixed width as original (800, NOT scaled)
        self.File_comboBox = QtWidgets.QComboBox(self.Replay_tab)
        self.File_comboBox.setObjectName("File_comboBox")
        self.File_comboBox.setEditable(False)
        self.File_comboBox.setFixedWidth(800)
        self.File_comboBox.currentTextChanged.connect(self.handle_file_selection_changed)
        self.top_controls_layout.addWidget(self.File_comboBox)

        # Search input
        self.search_LineEdit = QtWidgets.QLineEdit(self.Replay_tab)
        self.search_LineEdit.setObjectName("search_LineEdit")
        self.search_LineEdit.setText("請輸入想尋找的文件")
        self.top_controls_layout.addWidget(self.search_LineEdit)

        # Data produce button
        self.data_produce_btn_rp = QtWidgets.QPushButton(self.Replay_tab)
        self.data_produce_btn_rp.setObjectName("data_produce_btn_rp")
        self.data_produce_btn_rp.setText("data produce")
        self.top_controls_layout.addWidget(self.data_produce_btn_rp)

        # Stretch — EXACT same as original
        self.top_controls_layout.setStretch(0, 1)
        self.top_controls_layout.setStretch(1, 1)
        self.top_controls_layout.setStretch(2, 1)
        self.top_controls_layout.setStretch(3, 8)
        self.top_controls_layout.setStretch(4, 6)
        self.top_controls_layout.setStretch(5, 2)
        self.top_controls_layout.setContentsMargins(0, 0, 20, 0)
        self.replay_layout.addLayout(self.top_controls_layout)

        # ── Video area groupbox (same structure as original) ───────────
        self.play_groupBox = QtWidgets.QGroupBox(self.Replay_tab)
        self.play_groupBox.setObjectName("play_groupBox")
        self.play_layout = QtWidgets.QHBoxLayout()
        self.vision_layout_V = QtWidgets.QVBoxLayout()
        self.data_ctrl_layout_V = QtWidgets.QVBoxLayout()
        self.head_vis_layout = QtWidgets.QGridLayout()
        self.bottom_vis_layout = QtWidgets.QHBoxLayout()
        self.vision_layout_V.addLayout(self.head_vis_layout)
        self.vision_layout_V.addLayout(self.bottom_vis_layout)
        self.play_layout.addLayout(self.vision_layout_V)
        self.play_layout.addLayout(self.data_ctrl_layout_V)
        self.play_groupBox.setLayout(self.play_layout)
        self.replay_layout.addWidget(self.play_groupBox)

        # ── Bottom controls — 2-row VBoxLayout ──────────────────────────
        # Row 1 (top): Loop A / Loop B / Clear  (above the slider)
        # Row 2 (bottom): Play | Stop | Speed | ──Frameslider──── | Time
        # ui_frontend.py line 75 adds this to replay_layout.
        self.bottom_controls_layout = QtWidgets.QVBoxLayout()
        self.bottom_controls_layout.setSpacing(4)
        self.bottom_controls_layout.setContentsMargins(0, 0, 0, 0)

        # ── Row 1: Loop marker buttons ───────────────────────────────────
        loop_row = QtWidgets.QHBoxLayout()
        loop_row.setSpacing(6)

        self.LoopA_btn = QtWidgets.QPushButton()
        self.LoopA_btn.setEnabled(True)
        self.LoopA_btn.setObjectName("LoopA_btn")
        self.LoopA_btn.setMinimumWidth(140)
        loop_row.addWidget(self.LoopA_btn)

        self.LoopB_btn = QtWidgets.QPushButton()
        self.LoopB_btn.setEnabled(True)
        self.LoopB_btn.setObjectName("LoopB_btn")
        self.LoopB_btn.setMinimumWidth(140)
        loop_row.addWidget(self.LoopB_btn)

        self.ClearLoop_btn = QtWidgets.QPushButton()
        self.ClearLoop_btn.setEnabled(True)
        self.ClearLoop_btn.setObjectName("ClearLoop_btn")
        self.ClearLoop_btn.setMinimumWidth(140)
        loop_row.addWidget(self.ClearLoop_btn)

        loop_row.addStretch(1)  # push buttons to the left, slider area stays empty
        self.bottom_controls_layout.addLayout(loop_row)

        # ── Row 2: Playback controls ─────────────────────────────────────
        playback_row = QtWidgets.QHBoxLayout()
        playback_row.setSpacing(6)

        # Play / Stop — no fixed size (same as original)
        self.Play_btn = QtWidgets.QToolButton()
        self.Play_btn.setEnabled(False)
        self.Play_btn.setObjectName("Play_btn")
        playback_row.addWidget(self.Play_btn)

        self.Stop_btn = QtWidgets.QToolButton()
        self.Stop_btn.setEnabled(False)
        self.Stop_btn.setObjectName("Stop_btn")
        playback_row.addWidget(self.Stop_btn)

        # Speed combobox
        self.fast_forward_combobox = QtWidgets.QComboBox()
        self.fast_forward_combobox.setEnabled(False)
        self.fast_forward_combobox.setObjectName("fast_forward_combobox")
        self.fast_forward_combobox.setEditable(False)
        self.fast_forward_combobox.setMinimumWidth(100)
        playback_row.addWidget(self.fast_forward_combobox)

        # Frame slider — takes most horizontal space
        self.Frameslider = QtWidgets.QSlider()
        self.Frameslider.setGeometry(QtCore.QRect(190, 100, 90, 16))
        self.Frameslider.setEnabled(False)
        self.Frameslider.setOrientation(QtCore.Qt.Horizontal)
        self.Frameslider.setObjectName("Frameslider")
        playback_row.addWidget(self.Frameslider, stretch=90)

        # Time counter
        self.TimeCount_LineEdit = QtWidgets.QLineEdit()
        self.TimeCount_LineEdit.setEnabled(True)
        self.TimeCount_LineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.TimeCount_LineEdit.setReadOnly(True)
        self.TimeCount_LineEdit.setObjectName("TimeCount_LineEdit")
        playback_row.addWidget(self.TimeCount_LineEdit, stretch=5)

        self.bottom_controls_layout.addLayout(playback_row)

        # ── Assemble tabs ──────────────────────────────────────
        # Pass uppercase text directly — avoids Qt QSS text-transform size-calculation bug
        # (Qt sizes tabs using original text, but renders transformed text → clips symmetrically)
        self.tabs.addTab(self.Recording_tab, "RECORDING")
        self.tabs.addTab(self.Replay_tab, "REPLAY")
        self.main_layout.addWidget(self.tabs)

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # ──────────────────────────────────────────────────────────────
    def retranslateUi(self, MainWindow):
        _t = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_t("MainWindow", "CATS Webcamviewer"))
        self.rc_Benchpress_btn.setText(_t("MainWindow", "Benchpress"))
        self.rc_Squat_btn.setText(_t("MainWindow", "Squat"))
        self.rc_Deadlift_btn.setText(_t("MainWindow", "Deadlift"))
        self.manual_checkbox.setText(_t("MainWindow", "manual recording"))
        self.TimeCount_LineEdit.setPlaceholderText(_t("MainWindow", "00:00"))
        self.rp_Deadlift_btn.setText(_t("MainWindow", "Deadlift"))
        self.rp_Benchpress_btn.setText(_t("MainWindow", "Benchpress"))
        self.rp_Squat_btn.setText(_t("MainWindow", "Squat"))
        self.LoopA_btn.setText(_t("MainWindow", "設為循環 A 點"))
        self.LoopB_btn.setText(_t("MainWindow", "設為循環 B 點"))
        self.ClearLoop_btn.setText(_t("MainWindow", "清除區間"))

    # ──────────────────────────────────────────────────────────────
    def handle_file_selection_changed(self, text):
        path = text.strip()
        if path and os.path.isdir(path):
            self.folder = path
        else:
            self.folder = None