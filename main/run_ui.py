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
    
    # 修正 qt_material 2.17 不支援 PyQt5 導致無法載入 icon 的問題
    import os
    from PyQt5.QtCore import QDir
    QDir.addSearchPath("icon", os.path.join(os.path.expanduser("~"), ".qt_material", "theme"))
    
    apply_stylesheet(app, theme='dark_amber.xml')
    win = Mainwindow()
    win.showMaximized()
    sys.exit(app.exec_())

