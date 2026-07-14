import sys
from PyQt5 import QtWidgets
from ui_frontend import Mainwindow
from app_config import CONFIG

class MockMainwindow(Mainwindow):
    def __init__(self):
        super().__init__()
        # Mock YOLO to avoid PyTorch crash
        self.rcbf.model_select = lambda sport: [None, None]
        
app = QtWidgets.QApplication(sys.argv)
window = MockMainwindow()
window.rc_Squat_clicked()

print("Before click:")
print("data_produce_btn enabled:", window.data_produce_btn.isEnabled())
window.recording_ctrl_btn.click()
print("After click:")
print("data_produce_btn enabled:", window.data_produce_btn.isEnabled())
