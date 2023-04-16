import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt,QTimer, QModelIndex, QAbstractTableModel
from PyQt5.QtWidgets import QProgressBar

from PyQt5.QtWidgets import QDialogButtonBox, QApplication, QMainWindow, QListView, QAbstractItemView, QSplashScreen, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap

from Sample import Ui_MainWindow

from codelib import *

from tqdm import tqdm
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
        return index.column()==1 

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, win=False, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)
        self.setFixedSize(840, 580)
        self.listfiles = []

        self.pixmap = QPixmap("gif.gif")
        self.splash = QSplashScreen(self.pixmap)

        self.addbtn.clicked.connect(self.filesGet)
        self.indexbtn.clicked.connect(self.startIndex)
        self.prevbtn.clicked.connect(self.changePage)
        # self.label_1.setText("")
        self.mainLabel.setMaximumSize(1000, 1000)
        self.mainLabel.setStyleSheet("image : url(logo.png) ;background-position: center;background-repeat: no-repeat;")

        self.pushButton_2.clicked.connect(self.goSearch)

        self.keyEntry.textChanged.connect(self.changeLabel)
        self.addKey.clicked.connect(self.addKeywords)                                                           # to add the keyword from lineEdit text

        self.keyList= os.listdir('./AutoNBS/keywords/')
        self.keyList= [i[:-8] for i in self.keyList]
        self.model1= QStandardItemModel()                                                                       # model for availableKey listView, no multiple selection
        self.availableKeys.setModel(self.model1)
        self.availableKeys.doubleClicked.connect(self.addKeyDirectly)                                           # signal and slot func for adding new keyword on double click
        self.availableKeys.clicked[QModelIndex].connect(self.noticeKey)                                         # signal and slot func for deciding the key to be added
        self.checkSuggestions.stateChanged.connect(self.provideSuggestions)                                     # to toggle keyword suggestion feature

        self.model = QStandardItemModel()                                                                       # model for selectedKey listView
        self.mode= QAbstractItemView.MultiSelection                                                             # selection model for selectedKey listView
        self.selectedKeys.setSelectionMode(self.mode)
        self.selectedKeys.setModel(self.model)
        self.selectedKeys.clicked[QModelIndex].connect(self.on_clicked)                                         # to toggle the selection of keywords in selectedKeys
        self.indexList= []                                                                                      # list of item index in selected list

        self.buttonBox.button(QDialogButtonBox.Discard).clicked.connect(self.discard)
        self.buttonBox.button(QDialogButtonBox.Close).clicked.connect(self.quit)      
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(self.reset)   
        self.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.startSearch)             

        self.searchpixmap = QPixmap("./attempt1/wait.png")
        self.searchsplash = QSplashScreen(self.searchpixmap)                                                                # splash screen resource     

        self.fileLocations.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.fileLocations.doubleClicked.connect(self.OpenLink)      

        self.goBackHome.clicked.connect(self.quit)
        self.searchAgain.clicked.connect(self.goSearch)


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


    def goSearch(self):
        self.reset()
        self.stackedWidget.setCurrentIndex(2)
        # window.show()

    def changeLabel(self, text):
        if text!="":                                                                                            # when no text is given to lineEdit initially, no suggestions
            keySet= [name for name in self.keyList if text.lower() in name]                                     # list of keywords which have current text as substring
            self.provideSuggestions(keySet=keySet)
        else:
            self.provideSuggestions(keySet=[])
    
    def addKeywords(self):
        text= self.keyEntry.text()
        text= text.lower()                                                                                      # minimize risk with case sensitivity
        self.model.appendRow(QStandardItem(text))                                                               # adding new keyword in selectedKey


    def addKeyDirectly(self):                                                                                   # to add key from suggestions
        text=self.model1.itemFromIndex(self.noticedKey).text()                                                  # converting ModelIndex obj to StandardItem to text
        self.model.appendRow(QStandardItem(text))

    def noticeKey(self, index):                                                                                 # to remember the keyword selected from availableKeys
        self.noticedKey= index

    def provideSuggestions(self, keySet= []):
        if self.checkSuggestions.isChecked:
            self.model1.clear()                                                                                 # clear the list before appending data
            if(type(keySet)!=int and len(keySet)>0):                                                            # add suggestive keywords if keySet is a list 
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
        print(self.indexList)

    def discard(self):
        self.indexList.sort(reverse=True)
        # print(self.selectedKeys.model)
        # print(self.indexList[0].row())
        for i in self.indexList:
            self.selectedKeys.model().removeRow(i)
        self.indexList.clear()
    
    def quit(self):
        self.stackedWidget.setCurrentIndex(0)

    def reset(self):
        self.indexList.clear()
        self.model.clear()
        self.model1.clear()
        self.checkSuggestions.setChecked(False)

    def startSearch(self):
        self.stackedWidget.setCurrentIndex(3)
        self.searchsplash.show()
        QTimer.singleShot(2000, self.initiateSearch)

    def initiateSearch(self):
        length= self.model.rowCount()
        itemList= set()
        for i in range(length):
            item= self.selectedKeys.model().item(i).text()
            itemList.add(item)
            print(item)
        keywords_list= list(itemList)
        import Search_Module

        try:
            keywords_list = [key for key in keywords_list if key +
                            ".parquet" in os.listdir("./AutoNBS/keywords")]
            start = time.time()
            result = Search_Module.searchForDocuments(
                "./AutoNBS/keywords", keywords_list)
            end = time.time()

            self.res= result.select("location").to_numpy()
            print(os.path.basename(self.res[0][0]))
            self.path= np.array(([os.path.basename(self.res[i][0]) for i in range(len(self.res))]))
            self.path= self.path.reshape(len(self.path),1)
            print(np.shape(self.path), np.shape(self.res))
            self.res= np.hstack((self.path,self.res))

            print("Result fetched in :", end-start, "sec")

            Search_Module.updateSearchHistory(keywords_list)
            # self.model= QStandardItemModel()
            self.searchsplash.close()
            self.tablemodel = MyTableModel(self.res)
            self.fileLocations.setModel(self.tablemodel)
            self.timeLabel.setText("Time taken to Search: "+str(end-start)+' seconds')
            # for i in range(len(self.res)):
            #     self.model.appendRow([QStandardItem(i+1), QStandardItem(self.res[i]) ])
        except Exception as e:
        # with open('./AutoNBS/log.txt', 'a') as f:
        #     f.write('\n\n'+time.ctime()+"\n"+str(e)+"\n\n")
        #     f.close()
            print("Search Failed\n",e)

    def OpenLink(self, item):
            # dat= 
            if(self.tablemodel.isUrl(item)):
                value= self.tablemodel.data(item, Qt.DisplayRole)
                webbrowser.open(value)

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()