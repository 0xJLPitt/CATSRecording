from ui import Ui_MainWindow
from rcfunc import Recordingbackend
from rpfunc import Replaybackend
from app_config import CONFIG
from ui_theme import (
    S, BG_BASE, BG_RAISED, BG_SURFACE, CYAN, CYAN_DARK,
    ORANGE, BLUE, TEXT_BRIGHT, TEXT_DIM, BORDER, BORDER_MID,
    FONT_UI, FONT_MONO,
    recording_mode_btn_style, toolbutton_style,
)
from PyQt5 import QtCore, QtGui, QtWidgets
import os, glob, sys

# frontend logic

class SliderJumpFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
            opt = QtWidgets.QStyleOptionSlider()
            obj.initStyleOption(opt)
            sr = obj.style().subControlRect(QtWidgets.QStyle.CC_Slider, opt, QtWidgets.QStyle.SC_SliderHandle, obj)
            if not sr.contains(event.pos()):
                val = obj.minimum() + ((obj.maximum() - obj.minimum()) * event.pos().x()) / obj.width()
                obj.setValue(int(val))
        return super().eventFilter(obj, event)

class Mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(Mainwindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.rcbf = Recordingbackend()
        self.rpbf = Replaybackend()
        self.ui.setupUi(self)
        
        #self.ui.rc_Squat_btn.setEnabled(True)
        self.icons = []
        self.names = []
        self.graghs = []
        self.player_btn = []
        self.data_layouts = []
        self.D_layout_inited = False
        self.B_layout_inited = False
        self.S_layout_inited = False
        
        icon_srcs = glob.glob('./ui_src/*.png')
        for icon in icon_srcs:
            self.icons.append(QtGui.QIcon(icon))
        self.ui.Play_btn.setIcon(self.icons[1])
        self.ui.Stop_btn.setIcon(self.icons[3])

        self.ui.tabs.currentChanged.connect(self.tab_changed)
        self.ui.rc_Deadlift_btn.clicked.connect(self.rc_Deadlift_clicked)
        self.ui.rc_Benchpress_btn.clicked.connect(self.rc_Benchpress_clicked)
        self.ui.rc_Squat_btn.clicked.connect(self.rc_Squat_clicked)
        self.ui.rp_Deadlift_btn.clicked.connect(lambda :self.rp_layout_set('Deadlift'))
        self.ui.rp_Benchpress_btn.clicked.connect(lambda :self.rp_layout_set('Benchpress'))
        self.ui.rp_Squat_btn.clicked.connect(lambda :self.rp_layout_set('Squat'))
        
        self.Vision_labels = []  # Store QLabel for camera frames
        self.ui.File_comboBox.currentTextChanged.connect(lambda: self.rpbf.File_combobox_TextChanged(
            self.ui.File_comboBox, self.ui.Play_btn, self.icons, self.ui.Frameslider))
        self.ui.Stop_btn.clicked.connect(lambda: self.rpbf.stop(self.ui.Frameslider, self.ui.Play_btn, self.icons))
        
        # replay bottom ctrl connection
        rates = [1, 1.5, 0.8, 0.5]
        for rate in rates:
            self.ui.fast_forward_combobox.addItems([str(rate)])
        self.ui.Play_btn.clicked.connect(lambda: self.rpbf.play_btn_clicked(
            self.ui.fast_forward_combobox, self.ui.Play_btn, self.icons, self.ui.Frameslider))
        self.ui.Frameslider.valueChanged.connect(lambda: self.rpbf.sliding(self.ui.Frameslider, self.ui.TimeCount_LineEdit))
        self.ui.Frameslider.sliderPressed.connect(self.rpbf.slider_Pressed)
        self.ui.Frameslider.sliderReleased.connect(self.rpbf.slider_released)
        self.ui.Frameslider.valueChanged.connect(lambda: self.rpbf.slider_changed(self.ui.Frameslider, self.ui.Play_btn, self.icons))
        self.slider_filter = SliderJumpFilter()
        self.ui.Frameslider.installEventFilter(self.slider_filter)
        self.ui.search_LineEdit.textChanged.connect(lambda: self.rpbf.search_text_changed(self.ui.File_comboBox, self.ui.search_LineEdit.text()))
        self.ui.data_produce_btn_rp.clicked.connect(lambda: self.rpbf.data_produce_btn_clicked_rp(self.rpbf.currentsport))
        self.ui.LoopA_btn.clicked.connect(lambda: self.rpbf.set_loop_A(self.ui.Frameslider, self.ui.LoopA_btn))
        self.ui.LoopB_btn.clicked.connect(lambda: self.rpbf.set_loop_B(self.ui.Frameslider, self.ui.LoopB_btn))
        self.ui.ClearLoop_btn.clicked.connect(lambda: self.rpbf.clear_loop(self.ui.LoopA_btn, self.ui.LoopB_btn))
        self.ui.replay_layout.addLayout(self.ui.bottom_controls_layout)

    def tab_changed(self, index):
        if index == 0:
            self.layout_clear(self.ui.head_vis_layout)
            self.layout_clear(self.ui.bottom_vis_layout)
            self.layout_clear(self.ui.data_ctrl_layout_V)
            if self.data_layouts:
                for layout in self.data_layouts:
                    self.layout_clear(layout)
            self.data_layouts = []
            self.rpbf.tab_changed()

    def rc_Deadlift_clicked(self):
        self.names.clear()
        self.rc_Deadlift_layout_set()
        self.rcbf.currentsport = 'Deadlift'  
        self.rcbf.init_rc_backend('Deadlift', self.rc_Vision_labels)

    def rc_Squat_clicked(self):
        self.names.clear()
        self.rc_Squat_layout_set()
        self.rcbf.currentsport = 'Squat'
        self.rcbf.init_rc_backend('Squat', self.rc_Vision_labels)

    def rc_Benchpress_clicked(self):
        self.names.clear()
        self.rc_Benchpress_layout_set()
        self.rcbf.currentsport = 'Benchpress'
        self.rcbf.init_rc_backend('Benchpress', self.rc_Vision_labels)

    def back_toolbtn_clicked(self):
        # 清空 recording_layout
        self.rpbf.clear_layout(self.ui.recording_layout)
        self.rcbf.stop_event.set()
        # 重新添加原本的控件
        self.add_original_recording_tab_content()

    def add_original_recording_tab_content(self):
        grid_layout = self.ui.grid_Layout_recording

        self.ui.manual_checkbox = QtWidgets.QCheckBox(self.ui.Recording_tab)
        self.ui.manual_checkbox.setObjectName("manual_checkbox")
        self.ui.manual_checkbox.setText("manual recording")
        self.ui.manual_checkbox.setChecked(True)
        self.ui.manual_checkbox.setDisabled(True)
        grid_layout.addWidget(self.ui.manual_checkbox, 0, 0, 1, 1)

        self.ui.rc_Deadlift_btn = self.create_recording_button(
            self.ui.Recording_tab, "Deadlift", "rc_Deadlift_btn", self.rc_Deadlift_clicked)
        grid_layout.addWidget(self.ui.rc_Deadlift_btn, 1, 0, 1, 1)

        self.ui.rc_Benchpress_btn = self.create_recording_button(
            self.ui.Recording_tab, "Benchpress", "rc_Benchpress_btn", self.rc_Benchpress_clicked)
        grid_layout.addWidget(self.ui.rc_Benchpress_btn, 2, 0, 1, 1)

        self.ui.rc_Squat_btn = self.create_recording_button(
            self.ui.Recording_tab, "Squat", "rc_Squat_btn", self.rc_Squat_clicked)
        grid_layout.addWidget(self.ui.rc_Squat_btn, 3, 0, 1, 1)

        self.ui.recording_layout.addLayout(grid_layout)


    
    def rc_Deadlift_layout_set(self):
        # clear recording layout
        grid_layout = self.ui.grid_Layout_recording
        for i in reversed(range(grid_layout.count())):
            widget = grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # set recording layout
        self.ctrl_layout = QtWidgets.QHBoxLayout()
        self.ctrl_layout.setContentsMargins(0, 0, 0, 0)
        self.ctrl_layout.setSpacing(int(400 * CONFIG['ui_scale']))
        self.ui.recording_layout.addLayout(self.ctrl_layout)
        
        # ▶️ Recording 按鈕
        self.recording_ctrl_btn = QtWidgets.QToolButton(self.ui.Recording_tab)
        self.recording_ctrl_btn.setIcon(self.icons[2])
        self.recording_ctrl_btn.setIconSize(QtCore.QSize(int(140 * CONFIG['ui_scale']), int(140 * CONFIG['ui_scale'])))
        self.recording_ctrl_btn.setFixedSize(int(180 * CONFIG['ui_scale']), int(180 * CONFIG['ui_scale']))  # ✅ 可加這行
        self.ctrl_layout.addWidget(self.recording_ctrl_btn)

        self.auto_recording_btn = QtWidgets.QPushButton(self.ui.Recording_tab)
        self.auto_recording_btn.setText("AUTO RECORDING")
        self.auto_recording_btn.setEnabled(False)
        self.auto_recording_btn.setStyleSheet(recording_mode_btn_style(color=TEXT_DIM))
        self.auto_recording_btn.setMinimumSize(S(500), S(150))
        self.ctrl_layout.addWidget(self.auto_recording_btn)

        self.data_produce_btn = QtWidgets.QPushButton(self.ui.Recording_tab)
        self.data_produce_btn.setText("DATA PRODUCE")
        self.data_produce_btn.setStyleSheet(recording_mode_btn_style(color=CYAN))
        self.data_produce_btn.setMinimumSize(S(500), S(150))
        self.ctrl_layout.addWidget(self.data_produce_btn)

        self.source_ctrl_btn = QtWidgets.QPushButton(self.ui.Recording_tab)
        self.source_ctrl_btn.setText("SOURCE CHANGE")
        self.source_ctrl_btn.setStyleSheet(recording_mode_btn_style(color=ORANGE))
        self.source_ctrl_btn.setMinimumSize(S(500), S(150))
        self.ctrl_layout.addWidget(self.source_ctrl_btn)

        # 🔙 Back 按鈕（順序正確）
        self.back_toolbtn = QtWidgets.QToolButton(self.ui.Recording_tab)
        self.back_toolbtn.setIcon(self.icons[4])
        self.back_toolbtn.setIconSize(QtCore.QSize(int(140 * CONFIG['ui_scale']), int(140 * CONFIG['ui_scale'])))
        self.back_toolbtn.setFixedSize(int(180 * CONFIG['ui_scale']), int(180 * CONFIG['ui_scale']))
        self.back_toolbtn.clicked.connect(self.back_toolbtn_clicked)
        self.ctrl_layout.addWidget(self.back_toolbtn)

        self.Deadlift_vision_layout = QtWidgets.QHBoxLayout()
        self.ui.recording_layout.addLayout(self.Deadlift_vision_layout)

        # self.subject_layout = QtWidgets.QGridLayout()
        # self.subject_layout.setContentsMargins(0, 0, 0, 0)
        # for x in range(8):
        #     for y in range(2):
        #         if y == 0:
        #             text = QtWidgets.QLineEdit()
        #             text.setFocus(True)
        #             text.setAlignment(QtCore.Qt.AlignCenter)
        #             text.setText(f'Name {x+1}')
        #             text.setStyleSheet(f"font-size:{int(20 * CONFIG['ui_scale'])}px; color:yellow;")
        #             self.names.append(text)
        #             self.subject_layout.addWidget(text, y, x)    
        #         if y == 1:
        #             btn = QtWidgets.QPushButton(self.ui.Recording_tab)
        #             btn.setFont(QtGui.QFont('Times New Roman', 32))
        #             btn.setText(f'Player {x+1}')
        #             btn.clicked.connect(lambda checked, i=x: self.rcbf.player_reset(self.names[i]))
        #             self.player_btn.append(btn)
        #             self.subject_layout.addWidget(btn, y, x)
                    
        # self.ui.recording_layout.addLayout(self.subject_layout)

        labelsize = [480, 640]
        self.rc_Vision_labels, self.rc_qpixmaps = self.rpbf.creat_vision_labels_pixmaps([x * 0.8 for x in labelsize], self.ui.Recording_tab, self.Deadlift_vision_layout, 'Deadlift', CONFIG['cameras']['Deadlift'])
        self.data_produce_btn.clicked.connect(lambda: self.rcbf.data_produce_btn_clicked('Deadlift'))
        self.source_ctrl_btn.clicked.connect(lambda: self.rcbf.source_ctrl_btn_clicked('Deadlift', self.rc_Vision_labels))
        self.recording_ctrl_btn.clicked.connect(lambda: self.rcbf.recording_ctrl_btn_clicked('Deadlift', self.data_produce_btn, self.source_ctrl_btn, self.back_toolbtn))
        
    def rc_Benchpress_layout_set(self):
        # clear recording layout
        grid_layout = self.ui.grid_Layout_recording
        for i in reversed(range(grid_layout.count())):
            widget = grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # set recording layout
        self.ctrl_layout = QtWidgets.QHBoxLayout()
        self.ctrl_layout.setContentsMargins(0, 0, 0, 0)
        self.ctrl_layout.setSpacing(int(400 * CONFIG['ui_scale']))
        self.ui.recording_layout.addLayout(self.ctrl_layout)

        # ▶️ Recording 按鈕
        self.recording_ctrl_btn = QtWidgets.QToolButton(self.ui.Recording_tab)
        self.recording_ctrl_btn.setIcon(self.icons[2])
        self.recording_ctrl_btn.setIconSize(QtCore.QSize(int(140 * CONFIG['ui_scale']), int(140 * CONFIG['ui_scale'])))
        self.recording_ctrl_btn.setFixedSize(int(180 * CONFIG['ui_scale']), int(180 * CONFIG['ui_scale']))  # ✅ 可加這行
        self.ctrl_layout.addWidget(self.recording_ctrl_btn)
        self.recording_ctrl_btn.setEnabled(True)  # ✅ 啟用按鈕
        
        self.auto_recording_btn = QtWidgets.QPushButton(self.ui.Recording_tab)
        self.auto_recording_btn.setText("AUTO RECORDING")
        self.auto_recording_btn.setEnabled(True)
        self.auto_recording_btn.setStyleSheet(recording_mode_btn_style(color=ORANGE))
        self.auto_recording_btn.setMinimumSize(S(500), S(150))
        self.ctrl_layout.addWidget(self.auto_recording_btn)

        self.data_produce_btn = QtWidgets.QPushButton(self.ui.Recording_tab)
        self.data_produce_btn.setText("DATA PRODUCE")
        self.data_produce_btn.setStyleSheet(recording_mode_btn_style(color=CYAN))
        self.data_produce_btn.setMinimumSize(S(500), S(150))
        self.ctrl_layout.addWidget(self.data_produce_btn)

        self.source_ctrl_btn = QtWidgets.QPushButton(self.ui.Recording_tab)
        self.source_ctrl_btn.setText("SOURCE CHANGE")
        self.source_ctrl_btn.setStyleSheet(recording_mode_btn_style(color=ORANGE))
        self.source_ctrl_btn.setMinimumSize(S(500), S(150))
        self.ctrl_layout.addWidget(self.source_ctrl_btn)

        # 🔙 Back 按鈕（順序正確）
        self.back_toolbtn = QtWidgets.QToolButton(self.ui.Recording_tab)
        self.back_toolbtn.setIcon(self.icons[4])
        self.back_toolbtn.setIconSize(QtCore.QSize(int(140 * CONFIG['ui_scale']), int(140 * CONFIG['ui_scale'])))
        self.back_toolbtn.setFixedSize(int(180 * CONFIG['ui_scale']), int(180 * CONFIG['ui_scale']))
        self.back_toolbtn.clicked.connect(self.back_toolbtn_clicked)
        self.ctrl_layout.addWidget(self.back_toolbtn)

        self.Benchpress_vision_layout = QtWidgets.QHBoxLayout()
        self.ui.recording_layout.addLayout(self.Benchpress_vision_layout)
        
        # self.subject_layout = QtWidgets.QGridLayout()
        # self.subject_layout.setContentsMargins(0, 0, 0, 0)
        # for x in range(8):
        #     for y in range(2):
        #         if y == 0:
        #             text = QtWidgets.QLineEdit()
        #             text.setFocus(True)
        #             text.setAlignment(QtCore.Qt.AlignCenter)
        #             text.setText(f'Name {x+1}')
        #             text.setStyleSheet(f"font-size:{int(20 * CONFIG['ui_scale'])}px; color:yellow;")
        #             self.names.append(text)
        #             self.subject_layout.addWidget(text, y, x)    
        #         if y == 1:
        #             btn = QtWidgets.QPushButton(self.ui.Recording_tab)
        #             btn.setFont(QtGui.QFont('Times New Roman', 32))
        #             btn.setText(f'Player {x+1}')
        #             btn.clicked.connect(lambda checked, i=x: self.rcbf.player_reset(self.names[i]))
        #             self.player_btn.append(btn)
        #             self.subject_layout.addWidget(btn, y, x)
                    
        # self.ui.recording_layout.addLayout(self.subject_layout)

        labelsize = [640, 480]
        self.rc_Vision_labels, self.rc_qpixmaps = self.rpbf.creat_vision_labels_pixmaps([x * 0.75 for x in labelsize], self.ui.Recording_tab, self.Benchpress_vision_layout, 'Benchpress', CONFIG['cameras']['Benchpress'])
        self.data_produce_btn.clicked.connect(lambda: self.rcbf.data_produce_btn_clicked('Benchpress'))
        self.source_ctrl_btn.clicked.connect(lambda: self.rcbf.source_ctrl_btn_clicked('Benchpress', self.rc_Vision_labels))
        # self.recording_ctrl_btn.clicked.connect(lambda: self.rcbf.recording_ctrl_btn_clicked('Benchpress', self.data_produce_btn, self.source_ctrl_btn, self.back_toolbtn))
        # --- 原本只有 recording_ctrl_btn 被綁到 rcbf.recording_ctrl_btn_clicked(...) ---
        self.recording_ctrl_btn.clicked.connect(
            lambda: self.rcbf.recording_ctrl_btn_clicked('Benchpress', self.data_produce_btn, self.source_ctrl_btn, self.back_toolbtn)
        )  # 手動錄影：維持既有綁定，對應 shared_state["recording_sig"]  #
        # --- 新增：把 AUTO 鈕綁到「自動錄影切換」(設定 shared_state["auto_recording_sig"]) ---
        self.auto_recording_btn.clicked.connect(                                   # 綁定 AUTO 按鈕點擊事件
            lambda: self.rcbf.auto_recording_btn_clicked(                          # 呼叫後端處理
                'Benchpress', self.data_produce_btn, self.source_ctrl_btn,         # 傳入資料產生/來源控制
                self.back_toolbtn, self.recording_ctrl_btn                         # 傳入返回按鈕與「手動錄影」按鈕
            )
        ) # 自動錄影：切換 shared_state["auto_recording_sig"]  


    def apply_big_yellow_button(widget, font_size=32):
        widget.setStyleSheet(f"font-size: {font_size}px; color: yellow;")


    def rc_Squat_layout_set(self):
        # clear recording layout
        grid_layout = self.ui.grid_Layout_recording
        for i in reversed(range(grid_layout.count())):
            widget = grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # set recording layout
        self.ctrl_layout = QtWidgets.QHBoxLayout()
        self.ctrl_layout.setContentsMargins(0, 0, 0, 0)
        self.ctrl_layout.setSpacing(int(400 * CONFIG['ui_scale']))
        self.ui.recording_layout.addLayout(self.ctrl_layout)

        # ▶️ Recording 按鈕
        self.recording_ctrl_btn = QtWidgets.QToolButton(self.ui.Recording_tab)
        self.recording_ctrl_btn.setIcon(self.icons[2])
        self.recording_ctrl_btn.setIconSize(QtCore.QSize(int(140 * CONFIG['ui_scale']), int(140 * CONFIG['ui_scale'])))
        self.recording_ctrl_btn.setFixedSize(int(180 * CONFIG['ui_scale']), int(180 * CONFIG['ui_scale']))  # ✅ 可加這行
        self.ctrl_layout.addWidget(self.recording_ctrl_btn)

        self.auto_recording_btn = QtWidgets.QPushButton(self.ui.Recording_tab)
        self.auto_recording_btn.setText("AUTO RECORDING")
        self.auto_recording_btn.setEnabled(False)
        self.auto_recording_btn.setStyleSheet(recording_mode_btn_style(color=TEXT_DIM))
        self.auto_recording_btn.setMinimumSize(S(500), S(150))
        self.ctrl_layout.addWidget(self.auto_recording_btn)

        self.data_produce_btn = QtWidgets.QPushButton(self.ui.Recording_tab)
        self.data_produce_btn.setText("DATA PRODUCE")
        self.data_produce_btn.setStyleSheet(recording_mode_btn_style(color=CYAN))
        self.data_produce_btn.setMinimumSize(S(500), S(150))
        self.ctrl_layout.addWidget(self.data_produce_btn)

        self.source_ctrl_btn = QtWidgets.QPushButton(self.ui.Recording_tab)
        self.source_ctrl_btn.setText("SOURCE CHANGE")
        self.source_ctrl_btn.setStyleSheet(recording_mode_btn_style(color=ORANGE))
        self.source_ctrl_btn.setMinimumSize(S(500), S(150))
        self.ctrl_layout.addWidget(self.source_ctrl_btn)

        # 🔙 Back 按鈕（順序正確）
        self.back_toolbtn = QtWidgets.QToolButton(self.ui.Recording_tab)
        self.back_toolbtn.setIcon(self.icons[4])
        self.back_toolbtn.setIconSize(QtCore.QSize(int(140 * CONFIG['ui_scale']), int(140 * CONFIG['ui_scale'])))
        self.back_toolbtn.setFixedSize(int(180 * CONFIG['ui_scale']), int(180 * CONFIG['ui_scale']))
        self.back_toolbtn.clicked.connect(self.back_toolbtn_clicked)
        self.ctrl_layout.addWidget(self.back_toolbtn)

        self.Squat_vision_layout = QtWidgets.QHBoxLayout()
        self.ui.recording_layout.addLayout(self.Squat_vision_layout)

        # self.subject_layout = QtWidgets.QGridLayout()
        # self.subject_layout.setContentsMargins(0, 0, 0, 0)
        # for x in range(8):
        #     for y in range(2):
        #         if y == 0:
        #             text = QtWidgets.QLineEdit()
        #             text.setFocus(True)
        #             text.setAlignment(QtCore.Qt.AlignCenter)
        #             text.setText(f'Name {x+1}')
        #             text.setStyleSheet(f"font-size:{int(20 * CONFIG['ui_scale'])}px; color:yellow;")
        #             self.names.append(text)
        #             self.subject_layout.addWidget(text, y, x)    
        #         if y == 1:
        #             btn = QtWidgets.QPushButton(self.ui.Recording_tab)
        #             btn.setFont(QtGui.QFont('Times New Roman', 32))
        #             btn.setText(f'Player {x+1}')
        #             btn.clicked.connect(lambda checked, i=x: self.rcbf.player_reset(self.names[i]))
        #             self.player_btn.append(btn)
        #             self.subject_layout.addWidget(btn, y, x)
                    
        # self.ui.recording_layout.addLayout(self.subject_layout)

        labelsize = [480, 640]
        self.rc_Vision_labels, self.rc_qpixmaps = self.rpbf.creat_vision_labels_pixmaps([x * 0.8 for x in labelsize], self.ui.Recording_tab, self.Squat_vision_layout, 'Squat', CONFIG['cameras']['Squat'])
        self.data_produce_btn.clicked.connect(lambda: self.rcbf.data_produce_btn_clicked('Squat'))
        self.source_ctrl_btn.clicked.connect(lambda: self.rcbf.source_ctrl_btn_clicked('Squat', self.rc_Vision_labels))
        self.recording_ctrl_btn.clicked.connect(lambda: self.rcbf.recording_ctrl_btn_clicked('Squat', self.data_produce_btn, self.source_ctrl_btn, self.back_toolbtn))
       

    def rp_layout_set(self, sport):
        self.rpbf.currentsport = sport
        self.layout_clear(self.ui.head_vis_layout)
        self.layout_clear(self.ui.bottom_vis_layout)
        self.layout_clear(self.ui.data_ctrl_layout_V)
        if self.data_layouts:
            for layout in self.data_layouts:
                self.layout_clear(layout)
        self.data_layouts = []
        if sport == 'Deadlift':
            label_size = [480, 640]
            # 左半邊labels
            self.head_Vis_label, _ = self.rpbf.creat_vision_labels_pixmaps([x * 0.6 for x in label_size], self.ui.Replay_tab, self.ui.head_vis_layout, sport, 1)
            self.bottom_Vis_labels, _ = self.rpbf.creat_vision_labels_pixmaps([x * 0.5 for x in label_size], self.ui.Replay_tab, self.ui.bottom_vis_layout, sport, 2)
            
            # 右半邊graphic
            data_layout = QtWidgets.QFormLayout()
            self.data_layouts.append(data_layout)
            graphicview, graphicscene, canvas, axes, table = self.rpbf.creat_graphic(self.ui.Replay_tab, data_layout, (9, 7), 4)
            self.graph = {'graphicview' : graphicview, 'graphicscene' : graphicscene, 'canvas' : canvas, 'axes' : axes}
            self.ui.data_ctrl_layout_V.addLayout(data_layout)
                
            self.ui.bottom_vis_layout.setSpacing(10)
            self.ui.bottom_vis_layout.setContentsMargins(0, 0, 10, 10)
        
            self.rpbf.Deadlift_btn_pressed(
                self.ui.rp_Deadlift_btn, self.ui.rp_Benchpress_btn, self.ui.rp_Squat_btn, self.ui.Play_btn, self.icons, self.ui.Stop_btn, 
                self.ui.Frameslider, self.ui.fast_forward_combobox, self.ui.File_comboBox, self.ui.Replay_tab, self.ui.play_layout,
                self.head_Vis_label, self.bottom_Vis_labels, self.graph)
            
        elif sport == 'Benchpress':
            label_size = [640, 480]
            # 影片攤平成三個平行
            self.head_Vis_label, self.V_sliders, self.H_sliders, _ = self.rpbf.creat_vision_labels_pixmaps([x * 0.95 for x in label_size], self.ui.Replay_tab, self.ui.head_vis_layout, sport, 3, type='rp')
            self.bottom_Vis_labels = []
            
            # 移除右側的資料曲線圖
            self.graph = None
            
            self.ui.head_vis_layout.setSpacing(60)
            self.ui.head_vis_layout.setContentsMargins(10, 0, 10, 0)
                
            self.rpbf.Benchpress_btn_pressed(
                self.ui.rp_Deadlift_btn, self.ui.rp_Benchpress_btn, self.ui.rp_Squat_btn, self.ui.Play_btn, self.icons, self.ui.Stop_btn, 
                self.ui.Frameslider, self.ui.fast_forward_combobox, self.ui.File_comboBox, self.ui.Replay_tab, self.ui.play_layout,
                self.head_Vis_label, self.bottom_Vis_labels, self.graph)
            
        elif sport == 'Squat':
            label_size = [480, 640]
            # 影片攤平成三個平行
            self.head_Vis_label, self.V_sliders, self.H_sliders, _ = self.rpbf.creat_vision_labels_pixmaps([x * 0.95 for x in label_size], self.ui.Replay_tab, self.ui.head_vis_layout, sport, 3, type='rp')
            self.bottom_Vis_labels = []
            
            # 移除右側的資料曲線圖
            self.graph = None
                
            self.ui.head_vis_layout.setSpacing(60)
            self.ui.head_vis_layout.setContentsMargins(10, 0, 10, 0)
        
            self.rpbf.Squat_btn_pressed(
                self.ui.rp_Deadlift_btn, self.ui.rp_Benchpress_btn, self.ui.rp_Squat_btn, self.ui.Play_btn, self.icons, self.ui.Stop_btn, 
                self.ui.Frameslider, self.ui.fast_forward_combobox, self.ui.File_comboBox, self.ui.Replay_tab, self.ui.play_layout,
                self.head_Vis_label, self.bottom_Vis_labels, self.graph)
            
            
    def layout_clear(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def create_recording_button(self, parent, text, object_name, callback=None):
        btn = QtWidgets.QPushButton(parent)
        btn.setObjectName(object_name)
        btn.setText(text)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {BG_SURFACE}, stop:0.6 {BG_RAISED}, stop:1 {BG_BASE});
                color: {TEXT_BRIGHT};
                font-family: {FONT_UI};
                font-size: {S(22)}px;
                font-weight: 800;
                letter-spacing: 6px;
                text-transform: uppercase;
                border: 1px solid {BORDER_MID};
                border-left: 4px solid {CYAN};
                border-radius: 10px;
                padding-left: 28px;
                text-align: left;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {CYAN_DARK}, stop:1 {BG_RAISED});
                border-left: 4px solid {CYAN};
                border-color: {CYAN};
                color: {CYAN};
            }}
            QPushButton:pressed {{
                background: {CYAN_DARK};
            }}
        """)
        btn.setFixedSize(S(800), S(120))
        if callback:
            btn.clicked.connect(callback)
        return btn
