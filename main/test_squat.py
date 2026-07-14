import sys
from PyQt5 import QtWidgets
from ui_frontend import Mainwindow

app = QtWidgets.QApplication(sys.argv)
window = Mainwindow()
window.rc_Squat_clicked()

# Give it 2 seconds to see if threads crash
import time
time.sleep(2)
print("Finished without crashing!")
