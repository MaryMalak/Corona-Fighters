import sys
from PyQt5 import QtGui ,QtCore ,QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog,QMessageBox, \
    QApplication, QListWidget, QListView, QHBoxLayout, QListWidgetItem
from PyQt5.uic import loadUi


import main


class Mainwindow(QDialog):

    def __init__(self):
        self.browseflag=0
        super(Mainwindow, self).__init__()
        loadUi("corona fighter.ui", self)
        self.showFullScreen()
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.browse.clicked.connect(self.browsevideo)
        self.start.clicked.connect(self.startfn)
    def browsevideo(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file','E:', 'video files (*.mp4)')
        self.lineEdit.setText(fname[0])
        if len(fname[0]) != 0:
            self.browseflag = 1
    def startfn(self):
        if self.browseflag ==0 :
            self.error("error message", "please choose a video first ")
            return
        else:
            path=self.lineEdit.text()
            main.main(path)


    # Show Error Message Popup
    def error(self, title, text):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon("icon.ico"))
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)

        show_msg = msg.exec_()
if __name__=='__main__':
    app = QApplication(sys.argv)
    mainwindow = Mainwindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.show()
    sys.exit(app.exec_())
