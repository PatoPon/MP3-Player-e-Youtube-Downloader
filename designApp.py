# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designApp.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(847, 496)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("TubeTunes.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(66, 0, 66);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 851, 501))
        self.tabWidget.setStyleSheet("QTabWidget {\n"
"    border: 0;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"  background: purple;\n"
"  color: white;\n"
"  padding: 5px;\n"
" }\n"
"\n"
" QTabBar::tab:selected {\n"
"  background: rgb(166, 0, 166);\n"
" }")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setStyleSheet("")
        self.tab.setObjectName("tab")
        self.musicaTocando = QtWidgets.QLabel(self.tab)
        self.musicaTocando.setGeometry(QtCore.QRect(5, -5, 911, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.musicaTocando.setFont(font)
        self.musicaTocando.setStyleSheet("color: rgb(255, 255, 255)")
        self.musicaTocando.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.musicaTocando.setObjectName("musicaTocando")
        self.listWidget = QtWidgets.QListWidget(self.tab)
        self.listWidget.setGeometry(QtCore.QRect(0, 30, 771, 351))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(9)
        font.setUnderline(False)
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet("QListWidget {\n"
"    background-color: #800080; /* Dark background color */\n"
"    border: none; /* Remove the default border */\n"
"    padding: 3px; /* Internal padding for the list */\n"
"}\n"
"\n"
"QListWidget::item {\n"
"    background: transparent;\n"
"    color: white; /* Text color in the list */\n"
"    padding: 1px; /* Internal padding for each item in the list */\n"
"}\n"
"\n"
"QListWidget::item:selected {\n"
"    background: #4169E1; /* Background color when an item is selected (dark blue) */\n"
"    color: white; /* Text color of the selected item */\n"
"    outline: none; /* Remove the focus outline */\n"
"}\n"
"\n"
"QListWidget::item:hover {\n"
"    background: #666; /* Background color when the mouse hovers over an item */\n"
"}")
        self.listWidget.setObjectName("listWidget")
        self.volumeSlider = QtWidgets.QSlider(self.tab)
        self.volumeSlider.setGeometry(QtCore.QRect(805, 30, 16, 351))
        self.volumeSlider.setStyleSheet("QSlider {\n"
"    border: none; /* Remove a borda padrão do slider */\n"
"    background: purple; /* Cor de fundo escura */\n"
"    width: 50px; /* Altura do slider */\n"
"    border-radius: 10px; /* Borda arredondada */\n"
"}\n"
"\n"
"QSlider::handle:vertical {\n"
"    height: 4px;\n"
"    background-color:rgb(170, 0, 255);\n"
"    border-radius: 8px;\n"
"    height: 8px;\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    background: #4169E1; /* Cor da área da barra de música */\n"
"    border: 3px solid #800080; /* Borda da área da barra de música */\n"
"    width: 10px; /* Altura da área da barra de música */\n"
"    border-radius: 5px; /* Borda arredondada */\n"
"}")
        self.volumeSlider.setProperty("value", 80)
        self.volumeSlider.setOrientation(QtCore.Qt.Vertical)
        self.volumeSlider.setObjectName("volumeSlider")
        self.musicaSlider = QtWidgets.QSlider(self.tab)
        self.musicaSlider.setGeometry(QtCore.QRect(340, 440, 291, 22))
        self.musicaSlider.setStyleSheet("QSlider {\n"
"    border: none; /* Remove a borda padrão do slider */\n"
"    background: purple; /* Cor de fundo escura */\n"
"    height: 10px; /* Altura do slider */\n"
"    border-radius: 10px; /* Borda arredondada */\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    height: 4px;\n"
"    background-color:rgb(170, 0, 255);\n"
"    border-radius: 8px;\n"
"    width: 8px;\n"
"}\n"
"\n"
"QSlider::groove:horizontal {\n"
"    background: #4169E1; /* Cor da área da barra de música */\n"
"    border: 3px solid #800080; /* Borda da área da barra de música */\n"
"    height: 10px; /* Altura da área da barra de música */\n"
"    border-radius: 5px; /* Borda arredondada */\n"
"}")
        self.musicaSlider.setOrientation(QtCore.Qt.Horizontal)
        self.musicaSlider.setObjectName("musicaSlider")
        self.botaoEscolherPasta = QtWidgets.QPushButton(self.tab)
        self.botaoEscolherPasta.setGeometry(QtCore.QRect(10, 390, 141, 32))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        self.botaoEscolherPasta.setFont(font)
        self.botaoEscolherPasta.setStyleSheet("QPushButton {\n"
"    background-color: #800080;\n"
"    color: white; \n"
"    border: none; \n"
"    border-radius: 5px;\n"
"    padding: 10px 20px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #4169E1; \n"
"}")
        self.botaoEscolherPasta.setObjectName("botaoEscolherPasta")
        self.botaoEscolher = QtWidgets.QPushButton(self.tab)
        self.botaoEscolher.setGeometry(QtCore.QRect(10, 430, 141, 32))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        self.botaoEscolher.setFont(font)
        self.botaoEscolher.setStyleSheet("QPushButton {\n"
"    background-color: #800080;\n"
"    color: white; \n"
"    border: none; \n"
"    border-radius: 5px;\n"
"    padding: 10px 20px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #4169E1; \n"
"}")
        self.botaoEscolher.setObjectName("botaoEscolher")
        self.botaoPular = QtWidgets.QPushButton(self.tab)
        self.botaoPular.setGeometry(QtCore.QRect(520, 400, 31, 32))
        self.botaoPular.setStyleSheet("QPushButton {\n"
"    color: white; \n"
"    border: none; \n"
"    border-radius: 5px;\n"
"    padding: 10px 20px;\n"
"}")
        self.botaoPular.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("fim.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.botaoPular.setIcon(icon1)
        self.botaoPular.setIconSize(QtCore.QSize(48, 48))
        self.botaoPular.setObjectName("botaoPular")
        self.botaoTocar = QtWidgets.QPushButton(self.tab)
        self.botaoTocar.setGeometry(QtCore.QRect(470, 400, 32, 32))
        self.botaoTocar.setAutoFillBackground(False)
        self.botaoTocar.setStyleSheet("QPushButton {\n"
"    color: white; \n"
"    border: none; \n"
"    border-radius: 5px;\n"
"    padding: 10px 20px;\n"
"}")
        self.botaoTocar.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("reproduzir.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.botaoTocar.setIcon(icon2)
        self.botaoTocar.setIconSize(QtCore.QSize(64, 64))
        self.botaoTocar.setObjectName("botaoTocar")
        self.botaoAnterior = QtWidgets.QPushButton(self.tab)
        self.botaoAnterior.setGeometry(QtCore.QRect(420, 400, 31, 32))
        self.botaoAnterior.setStyleSheet("QPushButton {\n"
"    color: white; \n"
"    border: none; \n"
"    border-radius: 5px;\n"
"    padding: 10px 20px;\n"
"}")
        self.botaoAnterior.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("inicio.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.botaoAnterior.setIcon(icon3)
        self.botaoAnterior.setIconSize(QtCore.QSize(48, 48))
        self.botaoAnterior.setObjectName("botaoAnterior")
        self.botaoEmbaralhar = QtWidgets.QPushButton(self.tab)
        self.botaoEmbaralhar.setGeometry(QtCore.QRect(220, 410, 41, 31))
        self.botaoEmbaralhar.setStyleSheet("QPushButton {\n"
"    color: white; \n"
"    border: none; \n"
"    border-radius: 5px;\n"
"    padding: 10px 20px;\n"
"}")
        self.botaoEmbaralhar.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("embaralhar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.botaoEmbaralhar.setIcon(icon4)
        self.botaoEmbaralhar.setIconSize(QtCore.QSize(64, 64))
        self.botaoEmbaralhar.setObjectName("botaoEmbaralhar")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.BarraDeProgresso = QtWidgets.QProgressBar(self.tab_2)
        self.BarraDeProgresso.setGeometry(QtCore.QRect(79, 40, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Courier")
        self.BarraDeProgresso.setFont(font)
        self.BarraDeProgresso.setStyleSheet("QProgressBar {\n"
"    color: white;\n"
"    text-align: center;\n"
"    border: 1px solid #800080; /* Borda da barra de progresso */\n"
"    border-radius: 5px; /* Borda arredondada da barra de progresso */\n"
"    background: #800080; /* Cor de fundo da barra de progresso */\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background: #9932CC; /* Cor do preenchimento da barra de progresso */\n"
"}")
        self.BarraDeProgresso.setProperty("value", 100)
        self.BarraDeProgresso.setObjectName("BarraDeProgresso")
        self.progressoLabel = QtWidgets.QLabel(self.tab_2)
        self.progressoLabel.setGeometry(QtCore.QRect(80, 20, 229, 20))
        self.progressoLabel.setStyleSheet("color: white;\n"
"background-color: #800080;")
        self.progressoLabel.setTextFormat(QtCore.Qt.AutoText)
        self.progressoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.progressoLabel.setObjectName("progressoLabel")
        self.botaoBaixar = QtWidgets.QPushButton(self.tab_2)
        self.botaoBaixar.setGeometry(QtCore.QRect(136, 90, 111, 71))
        self.botaoBaixar.setMaximumSize(QtCore.QSize(16777215, 1600000))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        self.botaoBaixar.setFont(font)
        self.botaoBaixar.setStyleSheet("QPushButton {\n"
"    background-color: #800080;\n"
"    color: white; \n"
"    border: none; \n"
"    border-radius: 5px;\n"
"    padding: 10px 20px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #4169E1; \n"
"}")
        self.botaoBaixar.setObjectName("botaoBaixar")
        self.downloadList = QtWidgets.QListWidget(self.tab_2)
        self.downloadList.setGeometry(QtCore.QRect(410, 10, 421, 451))
        self.downloadList.setStyleSheet("background-color: #800080;\n"
"color: rgb(255, 255, 255)")
        self.downloadList.setObjectName("downloadList")
        self.botaoDownloadFolder = QtWidgets.QPushButton(self.tab_2)
        self.botaoDownloadFolder.setGeometry(QtCore.QRect(140, 180, 101, 81))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        self.botaoDownloadFolder.setFont(font)
        self.botaoDownloadFolder.setStyleSheet("QPushButton {\n"
"    background-color: #800080;\n"
"    color: white; \n"
"    border: none; \n"
"    border-radius: 5px;\n"
"    padding: 10px 20px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #4169E1; \n"
"}")
        self.botaoDownloadFolder.setObjectName("botaoDownloadFolder")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TubeTunes"))
        self.musicaTocando.setText(_translate("MainWindow", "Carregando..."))
        self.botaoEscolherPasta.setText(_translate("MainWindow", "Escolher Pasta"))
        self.botaoEscolher.setText(_translate("MainWindow", "Escolher Arquivos"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Player"))
        self.progressoLabel.setText(_translate("MainWindow", "Progresso"))
        self.botaoBaixar.setText(_translate("MainWindow", "Baixar"))
        self.botaoDownloadFolder.setText(_translate("MainWindow", "Escolher\n"
"Pasta"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Downloader"))
