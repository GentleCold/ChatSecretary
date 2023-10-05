import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from view.main_window import MainWindow

if __name__ == '__main__':
    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # create main window
    w = MainWindow()
    w.show()

    app.exec()
