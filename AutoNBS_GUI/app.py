import sys
from PyQt5.QtCore import Qt, QTimer, QModelIndex, QAbstractTableModel,QSize

from PyQt5.QtWidgets import QDialogButtonBox, QApplication, QMainWindow, QAbstractItemView, QSplashScreen, QHeaderView, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap,QIcon

from appGui import Ui_MainWindow

from codelib import *

import time
import os
import webbrowser
import numpy as np


class MyTableModel(QAbstractTableModel):
    def __init__(self, data=[[]], parent=None):
        super().__init__(parent)
        self.data1 = data

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return "File Paths"
            else:
                return str(section)

    def columnCount(self, parent=None):
        return len(self.data1[0])

    def rowCount(self, parent=None):
        return len(self.data1)

    def data(self, index: QModelIndex, role: int):
        # print("Qt.DisplayRole: ",Qt.DisplayRole,role)
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            # print(type(self.data1[row][col]), self.data1[row][col])
            return str(self.data1[row][col])

    def isUrl(self, index: QModelIndex):
        return index.column() == 1


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, win=False, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)
        self.setFixedSize(940, 680)
        self.listfiles = []

        self.pixmap = QPixmap("./photos/loading.png")
        self.splash = QSplashScreen(self.pixmap)

        pagebtnstyle = "QPushButton { background-color: #2980B9  ; color: white; border-radius:20px; border:2px solid  #522f02; } QPushButton:hover {background-color:#49abeb }"
        page4btnstyle = "QPushButton {border-color: #000000);background-color: #ff9514; border-radius:15px;}  QPushButton:hover {background-color: #f7af57 }"
        addkeybtnstyle = "QPushButton {  color : black; background-color: #27ff52 } QPushButton:hover {background-color: #71f58b }"

        self.addbtn.clicked.connect(self.filesGet)
        self.indexbtn.clicked.connect(self.startIndex)
        self.prevbtn.clicked.connect(self.changePage)
        self.pushButton_2.clicked.connect(self.goSearch)
        
        self.addbtn.setStyleSheet(pagebtnstyle)
        self.pushButton_2.setStyleSheet(pagebtnstyle)
        self.prevbtn.setStyleSheet(pagebtnstyle)
        self.indexbtn.setStyleSheet(pagebtnstyle)
        self.addKey.setStyleSheet(addkeybtnstyle)
        

        self.goBackHome.setStyleSheet(page4btnstyle)
        self.searchAgain.setStyleSheet(page4btnstyle)
        
        icon = QIcon("./photos/upload.png")
        self.addbtn.setIcon(icon)
        self.addbtn.setIconSize(QSize(40, 40))
        self.addbtn.setText(" ADD FILES")
        
        icon = QIcon("./photos/home.png")
        self.goBackHome.setIcon(icon)
        self.goBackHome.setIconSize(QSize(40, 40))
        self.goBackHome.setText("BACK TO HOME")
        
        icon = QIcon("./photos/searchagain.png")
        self.searchAgain.setIcon(icon)
        self.searchAgain.setIconSize(QSize(40, 40))
        self.searchAgain.setText("SEARCH AGAIN")

        icon = QIcon("./photos/search.png")
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QSize(40, 40))
        self.pushButton_2.setText(" SEARCH FILES")
        

        icon = QIcon("./photos/plus.png")
        self.addKey.setIcon(icon)
        self.addKey.setIconSize(QSize(25,25))
        self.addKey.setText(" ADD")
        
        icon = QIcon("./photos/left.png")
        self.prevbtn.setIcon(icon)
        self.prevbtn.setIconSize(QSize(30,30))
        self.prevbtn.setText(" Previous")

        self.mainLabel.setText("")
        self.mainLabel.setMaximumSize(1000, 1000)
        self.mainLabel.setStyleSheet("image : url(./photos/logo.png) ;background-position: center;background-repeat: no-repeat;")

        self.keyEntry.textChanged.connect(self.changeLabel)
        # to add the keyword from lineEdit text
        self.addKey.clicked.connect(self.addKeywords)
        self.keyEntry.returnPressed.connect(self.addKeywords)

        self.keyList = os.listdir('./keywords/')
        self.keyList = [i[:-8] for i in self.keyList]

        # model for availableKey listView, no multiple selection
        self.model1 = QStandardItemModel()
        self.availableKeys.setModel(self.model1)
        # signal and slot func for adding new keyword on double click
        self.availableKeys.doubleClicked.connect(self.addKeyDirectly)
        # signal and slot func for deciding the key to be added
        self.availableKeys.clicked[QModelIndex].connect(self.noticeKey)
        # to toggle keyword suggestion feature
        self.checkSuggestions.stateChanged.connect(self.provideSuggestions)

        # model for selectedKey listView
        self.model = QStandardItemModel()
        # selection model for selectedKey listView
        self.mode = QAbstractItemView.MultiSelection
        self.selectedKeys.setSelectionMode(self.mode)
        self.selectedKeys.setModel(self.model)
        # to toggle the selection of keywords in selectedKeys
        self.selectedKeys.clicked[QModelIndex].connect(self.on_clicked)
        # list of item index in selected list
        self.indexList = []

        self.buttonBox.button(
            QDialogButtonBox.Discard).clicked.connect(self.discard)
        self.buttonBox.button(
            QDialogButtonBox.Close).clicked.connect(self.quit)
        self.buttonBox.button(
            QDialogButtonBox.Reset).clicked.connect(self.reset)
        self.buttonBox.button(
            QDialogButtonBox.Apply).clicked.connect(self.startSearch)

        self.searchpixmap = QPixmap("./photos/wait.png")
        # splash screen resource
        self.searchsplash = QSplashScreen(self.searchpixmap)

        self.fileLocations.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.fileLocations.doubleClicked.connect(self.OpenLink)

        self.goBackHome.clicked.connect(self.quit)
        self.searchAgain.clicked.connect(self.goSearch)

    def updateKeywords(self):
        self.keyList = os.listdir('./keywords/')
        self.keyList = [i[:-8] for i in self.keyList]

    def filesGet(self):
        self.listfiles = getFiles()

        self.addbtn.setEnabled(True)
        self.indexbtn.setText("Start Indexing")
        self.stackedWidget.setCurrentIndex(1)
        self.listfiles, self.removedfiles = checkDuplicate(self.listfiles)

        if len(self.listfiles) == 0:
            self.indexbtn.setEnabled(False)
            self.label.setText(
                "Duplicates file(s) found.\n\n Add Different file(s).")
        else:
            totalFiles= len(self.listfiles)+len(self.removedfiles)
            uniqueFiles= len(self.listfiles)
            self.indexbtn.setEnabled(True)
            self.label.setText(
                str(uniqueFiles)+"/"+str(totalFiles)+" files are unique.\n\n You can now start Indexing your files.")
        
        self.removedfiles= ', '.join(self.removedfiles)
        self.message= QMessageBox()
        self.message.setIcon(QMessageBox.Information)
        self.message.setText("Following Files already exist in our system.\n"+self.removedfiles)
        self.message.setWindowTitle("Duplicate files")
        self.message.setStandardButtons(QMessageBox.Ok)
        self.message.exec()

    def startIndex(self):
        self.label.setText("Indexing your file(s)...")
        self.indexbtn.setEnabled(False)
        self.prevbtn.setEnabled(False)
        self.splash.show()
        QTimer.singleShot(1000, self.fileIndex)

    def fileIndex(self):
        message, keyUnique = indexFiles(self.listfiles)
        self.splash.close()
        keyUnique= list(keyUnique)
        keyUnique= '\n'.join(keyUnique)
        if len(message) == 0:
            self.label.setText("Your File(s) are now indexed.")
            self.label_2.setText("Keywords Found: \n"+keyUnique)
            self.indexbtn.setText("Indexing Completed")

        else:
            self.label_2.setText(message)
        self.updateKeywords()
        self.prevbtn.setEnabled(True)

    def changePage(self):
        self.label_2.setText("")
        self.stackedWidget.setCurrentIndex(0)

    def goSearch(self):
        self.reset()
        if self.timeLabel.text != "":
            self.tablemodel = MyTableModel([])
            self.timeLabel.setText("")
        self.stackedWidget.setCurrentIndex(2)
        # window.show()

    def changeLabel(self, text):
        # when no text is given to lineEdit initially, no suggestions
        if text != "":
            # list of keywords which have current text as substring
            newKeywordIndex= text.rfind(',')
            if newKeywordIndex!=-1:
                newKeyword= text[newKeywordIndex+1:].strip()
            else:
                newKeyword= text

            keySet = [name for name in self.keyList if newKeyword.lower() in name]
            self.provideSuggestions(keySet=keySet)
        else:
            self.provideSuggestions(keySet=[])

    def addKeywords(self):
        text = self.keyEntry.text()
        # minimize risk with case sensitivity
        text = text.lower()
        textList= text.split(',')
        # adding new keyword in selectedKey
        for texts in textList:
            self.model.appendRow(QStandardItem(texts.strip()))
        self.keyEntry.setText("")

    # to add key from suggestions
    def addKeyDirectly(self):
        # converting ModelIndex obj to StandardItem to text
        text = self.model1.itemFromIndex(self.noticedKey).text()
        self.model.appendRow(QStandardItem(text))

    # to remember the keyword selected from availableKeys
    def noticeKey(self, index):
        self.noticedKey = index

    def provideSuggestions(self, keySet=[]):
        if self.checkSuggestions.isChecked():
            # clear the list before appending data
            self.model1.clear()
            # add suggestive keywords if keySet is a list
            if (type(keySet) != int and len(keySet) > 0):
                for i in keySet:
                    self.model1.appendRow(QStandardItem(i))
            else:
                for i in self.keyList:
                    self.model1.appendRow(QStandardItem(i))
        else:
            self.model1.clear()

    def on_clicked(self, index):
        if index.row() not in self.indexList:
            self.indexList.append(index.row())
        else:
            self.indexList.remove(index.row())

    def discard(self):
        self.indexList.sort(reverse=True)
        # print(self.selectedKeys.model)
        # print(self.indexList[0].row())
        for i in self.indexList:
            self.selectedKeys.model().removeRow(i)
        self.indexList.clear()

    def quit(self):
        
        self.timeLabel.setText("")
        self.stackedWidget.setCurrentIndex(0)

    def reset(self):
        self.indexList.clear()
        self.model.clear()
        self.model1.clear()
        self.checkSuggestions.setChecked(False)

    def startSearch(self):
        self.fileLocations.setModel(MyTableModel([[]]))
        self.stackedWidget.setCurrentIndex(3)
        self.searchsplash.show()
        QTimer.singleShot(1, self.initiateSearch)

    def initiateSearch(self):
        length = self.model.rowCount()
        itemList = set()
        for i in range(length):
            item = self.selectedKeys.model().item(i).text()
            itemList.add(item)
            # print(item)
        keyword_list = list(itemList)
        import Search_Module

        try:
            keywords_list = [key for key in keyword_list if key +
                             ".parquet" in os.listdir("./keywords")]
            start = time.time()
            result = Search_Module.searchForDocuments(
                "./keywords", keywords_list)
            end = time.time()

            self.res = result.select("location").to_numpy()
            # print(os.path.basename(self.res[0][0]))
            self.path = np.array(
                ([os.path.basename(self.res[i][0]) for i in range(len(self.res))]))
            self.path = self.path.reshape(len(self.path), 1)
            # print(np.shape(self.path), np.shape(self.res))
            self.res = np.hstack((self.path, self.res))

            print("Result fetched in :", end-start, "sec")

            Search_Module.updateSearchHistory(keywords_list)
            # self.model= QStandardItemModel()
            self.searchsplash.close()
            keysNotFound = filter(lambda i: i not in keywords_list, keyword_list)
            if keysNotFound:
                keysNotFound= ', '.join(keysNotFound)
                self.message= QMessageBox()
                self.message.setIcon(QMessageBox.Information)
                self.message.setText("Following keywords specified by the users does not exist in the system.\n"+str(keysNotFound))
                self.message.setWindowTitle("Keywords removed from search")
                self.message.setStandardButtons(QMessageBox.Ok)
                self.message.exec()
            self.tablemodel = MyTableModel(self.res)
            self.fileLocations.setModel(self.tablemodel)
            self.timeLabel.setText(
                "Time taken to Search: \n"+str(end-start)+' seconds')

            # for i in range(len(self.res)):
            #     self.model.appendRow([QStandardItem(i+1), QStandardItem(self.res[i]) ])
        except Exception as e:
            # if not keywords_list:
            self.searchsplash.close()
            self.message= QMessageBox()
            self.message.setIcon(QMessageBox.Warning)
            self.message.setText("No files with the specified keywords found. Please try again with valid keywords.")
            self.message.setWindowTitle("Search Failed")
            self.message.setStandardButtons(QMessageBox.Ok)
            self.message.buttonClicked.connect(self.msgButtonClick)
            if self.message.exec()== QMessageBox.Ok:
                self.goSearch()
            # with open('./log.txt', 'a') as f:
            #     f.write('\n\n'+time.ctime()+"\n"+str(e)+"\n\n")
            #     f.close()
            print("Search Failed\n", e)
    
    def msgButtonClick(self, option):
        print("Testing",option)

    def OpenLink(self, item):
        # dat=
        if (self.tablemodel.isUrl(item)):
            value = self.tablemodel.data(item, Qt.DisplayRole)
            webbrowser.open(value)

fileName= ['keywords','history','index']
for i in range(len(fileName)):
    if fileName[i] not in os.listdir():
        os.mkdir('./'+fileName[i])

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
