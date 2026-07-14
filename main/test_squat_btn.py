import sys
from PyQt5 import QtWidgets, QtCore
from ui_frontend import Mainwindow
from app_config import CONFIG

app = QtWidgets.QApplication(sys.argv)
window = Mainwindow()
window.rc_Squat_clicked()

print("Before click, data_produce_btn enabled:", window.data_produce_btn.isEnabled())
window.recording_ctrl_btn.click()
print("After click, data_produce_btn enabled:", window.data_produce_btn.isEnabled())

