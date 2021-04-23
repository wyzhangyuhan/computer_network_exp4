import sys

# PYQT
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5 import QtCore, QtGui
import Ui_main


if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     host = sys.argv[0]
    # else:
    #     host = "localhost"
    # port = 5001

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    mainw  = QMainWindow()
    main_ui = Ui_main.Ui_MainWindow()
    main_ui.setupUi(mainw)
    mainw.show()

    sys.exit(app.exec_())