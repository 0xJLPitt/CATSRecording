import torch
_original_torch_load = torch.load
def _patched_torch_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return _original_torch_load(*args, **kwargs)
torch.load = _patched_torch_load

from ui_frontend import Mainwindow
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_amber.xml')
    win = Mainwindow()
    win.showMaximized()
    sys.exit(app.exec_())

