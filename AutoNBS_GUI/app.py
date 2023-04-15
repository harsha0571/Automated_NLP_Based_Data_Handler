import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtWidgets import QProgressBar

from PyQt5.QtWidgets import QDialogButtonBox, QApplication, QMainWindow, QListView, QAbstractItemView, QSplashScreen
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap

from Sample import Ui_MainWindow

from codelib import *

from tqdm import tqdm
import time


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setFixedSize(840, 580)
        self.listfiles = []

        self.pixmap = QPixmap("gif.gif")
        self.splash = QSplashScreen(self.pixmap)

        self.addbtn.clicked.connect(self.filesGet)
        self.indexbtn.clicked.connect(self.startIndex)
        self.prevbtn.clicked.connect(self.changePage)
        self.label_1.setText("")
        self.label_1.setMaximumSize(1000, 1000)
        self.label_1.setStyleSheet("image : url(logo.png) ;background-position: center;background-repeat: no-repeat;")



    def filesGet(self):
        self.listfiles = getFiles()

        self.addbtn.setEnabled(True)
        self.stackedWidget.setCurrentIndex(1)
        self.listfiles = checkDuplicate(self.listfiles)

        if len(self.listfiles)==0:
            self.indexbtn.setEnabled(False)
            self.label.setText("Duplicates file(s) found.\n\n Add Different file(s).")
        else:
            self.indexbtn.setEnabled(True)
            self.label.setText("No Duplicates found.\n\n You can now start Indexing your files.")




    def startIndex(self):
        self.label.setText("Indexing your file(s)...")
        self.indexbtn.setEnabled(False)
        self.prevbtn.setEnabled(False)
        self.splash.show()
        QTimer.singleShot(1000, self.fileIndex)
        

    def fileIndex(self):
        message = indexFiles(self.listfiles)
        self.splash.close()

        if len(message) == 0:
            self.label.setText("Your File(s) are now indexed.")
            self.indexbtn.setEnabled(False)

        else:
            self.label.setText(message)

        self.indexbtn.setEnabled(True)
        self.prevbtn.setEnabled(True)


    def changePage(self):
        self.stackedWidget.setCurrentIndex(0)
        # self.addbtn.setEnabled(True)


   



app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()