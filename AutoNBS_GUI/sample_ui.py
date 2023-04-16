# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sample.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialogButtonBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QListView, QMainWindow, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QStackedWidget, QTableView,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background-color: rgb(255, 170, 127);\n"
"color: rgb(49, 49, 49);")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.mainLabel = QLabel(self.page)
        self.mainLabel.setObjectName(u"mainLabel")
        font = QFont()
        font.setFamilies([u"Algerian"])
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        self.mainLabel.setFont(font)
        self.mainLabel.setStyleSheet(u"color: rgb(6, 6, 6);")
        self.mainLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.mainLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addbtn = QPushButton(self.page)
        self.addbtn.setObjectName(u"addbtn")
        self.addbtn.setMinimumSize(QSize(0, 150))
        font1 = QFont()
        font1.setPointSize(15)
        self.addbtn.setFont(font1)
        self.addbtn.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"background-color: rgb(254, 222, 205);\n"
"border-left-color: rgb(0, 0, 0);\n"
"border-top-color: rgb(0, 0, 0);")

        self.horizontalLayout.addWidget(self.addbtn)

        self.pushButton_2 = QPushButton(self.page)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(0, 150))
        self.pushButton_2.setFont(font1)
        self.pushButton_2.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"background-color: rgb(254, 222, 205);\n"
"border-left-color: rgb(0, 0, 0);\n"
"border-top-color: rgb(0, 0, 0);")

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.page_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.page_2)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setPointSize(15)
        font2.setBold(False)
        self.label.setFont(font2)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.prevbtn = QPushButton(self.page_2)
        self.prevbtn.setObjectName(u"prevbtn")
        self.prevbtn.setMaximumSize(QSize(150, 50))
        self.prevbtn.setFont(font1)
        self.prevbtn.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"background-color: rgb(254, 222, 205);\n"
"border-left-color: rgb(0, 0, 0);\n"
"border-top-color: rgb(0, 0, 0);")

        self.horizontalLayout_2.addWidget(self.prevbtn)

        self.indexbtn = QPushButton(self.page_2)
        self.indexbtn.setObjectName(u"indexbtn")
        self.indexbtn.setMaximumSize(QSize(300, 50))
        self.indexbtn.setFont(font1)
        self.indexbtn.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"background-color: rgb(254, 222, 205);\n"
"border-left-color: rgb(0, 0, 0);\n"
"border-top-color: rgb(0, 0, 0);")

        self.horizontalLayout_2.addWidget(self.indexbtn)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_21 = QVBoxLayout(self.page_3)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.docLabel = QLabel(self.page_3)
        self.docLabel.setObjectName(u"docLabel")
        font3 = QFont()
        font3.setFamilies([u"Cambria"])
        font3.setPointSize(35)
        font3.setBold(True)
        self.docLabel.setFont(font3)
        self.docLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_21.addWidget(self.docLabel)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_21.addItem(self.verticalSpacer)

        self.horizontalLayout1 = QHBoxLayout()
        self.horizontalLayout1.setObjectName(u"horizontalLayout1")
        self.keyEntry = QLineEdit(self.page_3)
        self.keyEntry.setObjectName(u"keyEntry")
        self.keyEntry.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
" color: rgb(0, 0, 0);")

        self.horizontalLayout1.addWidget(self.keyEntry)

        self.addKey = QPushButton(self.page_3)
        self.addKey.setObjectName(u"addKey")
        self.addKey.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"background-color: rgb(254, 222, 205);\n"
"border-left-color: rgb(0, 0, 0);\n"
"border-top-color: rgb(0, 0, 0);")

        self.horizontalLayout1.addWidget(self.addKey)


        self.verticalLayout_21.addLayout(self.horizontalLayout1)

        self.docScroll = QScrollArea(self.page_3)
        self.docScroll.setObjectName(u"docScroll")
        self.docScroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 754, 345))
        self.verticalLayout_31 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.availableKeys = QListView(self.scrollAreaWidgetContents_2)
        self.availableKeys.setObjectName(u"availableKeys")
        self.availableKeys.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_31.addWidget(self.availableKeys)

        self.selectedKeys = QListView(self.scrollAreaWidgetContents_2)
        self.selectedKeys.setObjectName(u"selectedKeys")
        self.selectedKeys.setStyleSheet(u"background-color: rgb(0, 255, 0);\n"
" background-color: rgb(0, 255, 127);")

        self.verticalLayout_31.addWidget(self.selectedKeys)

        self.docScroll.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_21.addWidget(self.docScroll)

        self.checkSuggestions = QCheckBox(self.page_3)
        self.checkSuggestions.setObjectName(u"checkSuggestions")

        self.verticalLayout_21.addWidget(self.checkSuggestions)

        self.buttonBox = QDialogButtonBox(self.page_3)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"background-color: rgb(254, 222, 205);\n"
"border-left-color: rgb(0, 0, 0);\n"
"border-top-color: rgb(0, 0, 0);")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Close|QDialogButtonBox.Discard|QDialogButtonBox.Reset)

        self.verticalLayout_21.addWidget(self.buttonBox)

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_4 = QVBoxLayout(self.page_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.searchLabel = QLabel(self.page_4)
        self.searchLabel.setObjectName(u"searchLabel")
        self.searchLabel.setFont(font3)
        self.searchLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.searchLabel)

        self.notelabel = QLabel(self.page_4)
        self.notelabel.setObjectName(u"notelabel")
        self.notelabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.notelabel)

        self.resultScroll = QScrollArea(self.page_4)
        self.resultScroll.setObjectName(u"resultScroll")
        self.resultScroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 754, 452))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.fileLocations = QTableView(self.scrollAreaWidgetContents_3)
        self.fileLocations.setObjectName(u"fileLocations")
        self.fileLocations.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"gridline-color: rgb(255, 85, 0);\n"
"background-color: rgb(226, 255, 131);\n"
"border-color: rgb(0, 0, 0);")

        self.verticalLayout_5.addWidget(self.fileLocations)

        self.resultFooter = QHBoxLayout()
        self.resultFooter.setObjectName(u"resultFooter")
        self.timeLabel = QLabel(self.scrollAreaWidgetContents_3)
        self.timeLabel.setObjectName(u"timeLabel")

        self.resultFooter.addWidget(self.timeLabel)

        self.goBackHome = QPushButton(self.scrollAreaWidgetContents_3)
        self.goBackHome.setObjectName(u"goBackHome")
        self.goBackHome.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"background-color: rgb(254, 222, 205);\n"
"border-left-color: rgb(0, 0, 0);\n"
"border-top-color: rgb(0, 0, 0);")

        self.resultFooter.addWidget(self.goBackHome)

        self.searchAgain = QPushButton(self.scrollAreaWidgetContents_3)
        self.searchAgain.setObjectName(u"searchAgain")
        self.searchAgain.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"background-color: rgb(254, 222, 205);\n"
"border-left-color: rgb(0, 0, 0);\n"
"border-top-color: rgb(0, 0, 0);")

        self.resultFooter.addWidget(self.searchAgain)


        self.verticalLayout_5.addLayout(self.resultFooter)

        self.resultScroll.setWidget(self.scrollAreaWidgetContents_3)

        self.verticalLayout_4.addWidget(self.resultScroll)

        self.stackedWidget.addWidget(self.page_4)

        self.verticalLayout_3.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.mainLabel.setText(QCoreApplication.translate("MainWindow", u"AUTONBS", None))
        self.addbtn.setText(QCoreApplication.translate("MainWindow", u"ADD FILES", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"SEARCH FILES", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Checking for Duplicates...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u".", None))
        self.prevbtn.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.indexbtn.setText(QCoreApplication.translate("MainWindow", u"START INDEXING", None))
        self.docLabel.setText(QCoreApplication.translate("MainWindow", u"DOCUMENT FINDER", None))
        self.addKey.setText(QCoreApplication.translate("MainWindow", u"ADD", None))
        self.checkSuggestions.setText(QCoreApplication.translate("MainWindow", u"Load Keyword Suggestions", None))
        self.searchLabel.setText(QCoreApplication.translate("MainWindow", u"SEARCH RESULTS", None))
        self.notelabel.setText(QCoreApplication.translate("MainWindow", u"{Showing Upto Top 100 Search Results}", None))
        self.timeLabel.setText(QCoreApplication.translate("MainWindow", u"Time Taken to Search: ", None))
        self.goBackHome.setText(QCoreApplication.translate("MainWindow", u"Back To Home", None))
        self.searchAgain.setText(QCoreApplication.translate("MainWindow", u"Search Again", None))
    # retranslateUi

