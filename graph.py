# I am using Pyqt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator, QKeySequence, QMovie, QTextCursor
from PyQt5.QtWidgets import QDialog, QInputDialog, QLineEdit, QFileDialog, QMainWindow, QPushButton, QShortcut, QAbstractItemView, QSizePolicy, QCheckBox, QStatusBar, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QProgressBar
from PyQt5.QtCore import QObject, Q_ARG, Qt, QTimer, QDateTime, pyqtSignal, QThread
import csv
import os
import datetime
import numpy as np
import pandas as pd
import matplotlib
from time import sleep
from tqdm import tqdm
import io
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """
            initialize chart library
        """

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        """
            initialize app interface
        """

        self.MW = MainWindow
        path = os.path.dirname(os.path.abspath(__file__))
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)
        MainWindow.setBaseSize(QtCore.QSize(285, 260))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet("QMainWindow{background-color: qlineargradient(x2:2 y2:2, x1:0 y1:2, stop:0 #485563, stop:1 #29323c);}")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        # self.centralwidget = QtWidgets.QStackedWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setStyleSheet("QWidget{background-color: qlineargradient( x2:2 y2:2, x1:2 y1:0, stop:0 #303030, stop:1 #6e6e6e);}")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(9, 9, -1, -1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        MainWindow.setWindowIcon(QtGui.QIcon(os.path.join(path, r"icons\spec1.png")))

        # fonts
        # font1 = QtGui.QFont('Bookman Old Style')
        font1 = QtGui.QFont('Montserrat')
        font1.setPointSize(15)
        font = QtGui.QFont('Retro Gaming')
        font.setPointSize(11)
        font2 = QtGui.QFont('Retro Gaming')
        font2.setPointSize(7)
        fonttb = QtGui.QFont('Montserrat Medium')
        fonttb.setPointSize(8)
        fontbtn = QtGui.QFont('Montserrat')
        fontbtn.setPointSize(8)
        fontlam = QtGui.QFont('Montserrat')
        fontlam.setPointSize(8)
        
        # lbl
        self.lbl = QtWidgets.QLabel("RBD")
        self.lbl.setFont(font1)
        self.lbl.setStyleSheet("color: #ffffff; background: None")
        self.lbl.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.lbl, 1, 0)

        # lbl1
        self.lbl1 = QtWidgets.QLabel("Absorbance")
        self.lbl1.setFont(font1)
        self.lbl1.setStyleSheet("color: #ffffff; background: None")
        self.lbl1.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.lbl1, 1, 1)

        # lbl2
        self.lbl2 = QtWidgets.QLabel("Kinetics")
        self.lbl2.setFont(font1)
        self.lbl2.setStyleSheet("color: #ffffff; background: None")
        self.lbl2.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.lbl2, 1, 2)

        self.lbl3 = QtWidgets.QLabel("Files:")
        self.lbl3.setFont(fonttb)
        self.lbl3.setStyleSheet("color: white; background: None")
        self.lbl3.setAlignment(Qt.AlignCenter)

        self.lbl4 = QtWidgets.QLabel("Time step:")
        self.lbl4.setFont(fonttb)
        self.lbl4.setStyleSheet("color: white; background: None")
        self.lbl4.setAlignment(Qt.AlignCenter)

        self.lbl5 = QtWidgets.QLabel("Lambda:")
        self.lbl5.setFont(fonttb)
        self.lbl5.setStyleSheet("color: white; background: None")
        self.lbl5.setAlignment(Qt.AlignCenter)

        self.onlyInt = QIntValidator()
        self.files_cnt_le = QtWidgets.QLineEdit("")
        self.files_cnt_le.setFont(font1)
        self.files_cnt_le.setStyleSheet("color: black; background: None")
        self.files_cnt_le.setAlignment(Qt.AlignCenter)
        self.files_cnt_le.setFixedSize(80, 35)
        self.files_cnt_le.setValidator(self.onlyInt)

        self.time_step_le = QtWidgets.QLineEdit("")
        self.time_step_le.setFont(font1)
        self.time_step_le.setStyleSheet("color: black; background: None")
        self.time_step_le.setAlignment(Qt.AlignCenter)
        self.time_step_le.setFixedSize(80, 35)
        # self.time_step_le.setValidator(self.onlyInt)

        self.lambda_le = QtWidgets.QLineEdit("")
        self.lambda_le.setFont(fontlam)
        self.lambda_le.setStyleSheet("color: black; background: None")
        self.lambda_le.setAlignment(Qt.AlignCenter)
        self.lambda_le.setFixedSize(80, 35)

        self.settimeBtn = QtWidgets.QPushButton("Set Time")
        # self.settimeBtn.setStyleSheet("color: black; background: grey; border-radius: 7px;")
        self.settimeBtn.setStyleSheet("QPushButton{background-color: qlineargradient( x2:2 y2:2, x1:0 y1:2, stop:0 #485563, stop:1 #29323c);\n"
                                   "color:#ffffff; border-radius: 7px;}")
        self.settimeBtn.setFont(fontbtn)
        self.settimeBtn.setFixedSize(80, 35)

        self.openchartBtn = QtWidgets.QPushButton("Open\nchart")
        self.openchartBtn.setStyleSheet("QPushButton{background-color: qlineargradient( x2:2 y2:2, x1:0 y1:2, stop:0 #485563, stop:1 #29323c);\n"
                                   "color:#ffffff; border-radius: 7px;}")
        self.openchartBtn.setFont(fontbtn)
        self.openchartBtn.setFixedSize(80, 50)

        # rbdTbl
        self.rbdTbl = QtWidgets.QTableWidget(self.centralwidget)
        self.rbdTbl.setColumnCount(3)
        self.rbdTbl.setHorizontalHeaderLabels(['Reference', 'Black', 'Data'])
        rbdTbl_header = self.rbdTbl.horizontalHeader()
        rbdTbl_header.setFont(fonttb)
        self.rbdTbl.setFont(fonttb)
        rbdTbl_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        rbdTbl_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        rbdTbl_header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.rbdTbl.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        self.rbdTbl.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        self.rbdTbl.horizontalHeaderItem(2).setTextAlignment(Qt.AlignCenter)


        # self.rbd.setFont(font)
        self.rbdTbl.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.rbdTbl.setAutoFillBackground(False)
        self.rbdTbl.setStyleSheet("QWidget{background-color: #ffffff;}")
        self.rbdTbl.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.rbdTbl.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.rbdTbl.setLineWidth(1)
        self.rbdTbl.setObjectName("rbdTbl")
        self.gridLayout.addWidget(self.rbdTbl, 2, 0, 1, 1)
        self.rbdTbl.setAcceptDrops(True)
        self.rbdTbl.setDragEnabled(True)
        self.rbdTbl.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.rbdTbl.setDropIndicatorShown(True)
        self.rbdTbl.setSelectionMode(1)

        # inprogressList
        self.resultTbl = QtWidgets.QTableWidget(self.centralwidget)
        self.resultTbl.setColumnCount(2)
        self.resultTbl.setHorizontalHeaderLabels(['lambda', 'Abs'])
        resultTbl_header = self.resultTbl.horizontalHeader()
        resultTbl_header.setFont(fonttb)
        self.resultTbl.setFont(fonttb)
        resultTbl_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        resultTbl_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.resultTbl.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        self.resultTbl.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        self.resultTbl.setItem(0, 0, QTableWidgetItem("t1"))
        self.resultTbl.setItem(0, 1, QTableWidgetItem("t2"))
        self.resultTbl.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.resultTbl.setAutoFillBackground(False)
        self.resultTbl.setStyleSheet("QWidget{background-color: #ffffff;}")
        self.resultTbl.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.resultTbl.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.resultTbl.setLineWidth(1)
        self.resultTbl.setObjectName("result")
        self.gridLayout.addWidget(self.resultTbl, 2, 1, 1, 1)
        self.resultTbl.setAcceptDrops(True)
        self.resultTbl.setDragEnabled(True)
        self.resultTbl.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.resultTbl.setSelectionMode(1)


        self.timelambdaTbl = QtWidgets.QTableWidget(self.centralwidget)
        self.timelambdaTbl.setColumnCount(2)
        self.timelambdaTbl.setHorizontalHeaderLabels(['Time', 'Abs'])
        timelambdaTbl_header = self.timelambdaTbl.horizontalHeader()
        timelambdaTbl_header.setFont(fonttb)
        self.timelambdaTbl.setFont(fonttb)
        timelambdaTbl_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        timelambdaTbl_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.timelambdaTbl.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        self.timelambdaTbl.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        self.timelambdaTbl.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.timelambdaTbl.setAutoFillBackground(False)
        self.timelambdaTbl.setStyleSheet("QWidget{background-color: #ffffff;}")
        self.timelambdaTbl.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.timelambdaTbl.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.timelambdaTbl.setLineWidth(1)
        self.timelambdaTbl.setFixedWidth(600)
        self.timelambdaTbl.setObjectName("timelambdaTbl")
        self.gridLayout.addWidget(self.timelambdaTbl, 2, 2, 1, 1)
        self.timelambdaTbl.setAcceptDrops(True)
        self.timelambdaTbl.setDragEnabled(True)
        self.timelambdaTbl.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.timelambdaTbl.setSelectionMode(1)

        self.canvas1 = MplCanvas(self, width=5, height=4, dpi=100)
        self.gridLayout.addWidget(self.canvas1, 3, 0, 1, 2)

        self.canvas2 = MplCanvas(self, width=5, height=4, dpi=100)
        self.gridLayout.addWidget(self.canvas2, 3, 2, 1, 1)

        self.stat = QtWidgets.QStatusBar(MainWindow)
        self.stat.setObjectName('stat')
        MainWindow.setStatusBar(self.stat)
        self.stat.setFont(fonttb)
        self.stat.showMessage('Ready')
        self.stat.setStyleSheet("color: #ffffff; background: None")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 288, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.menubar.setStyleSheet("QMenuBar{background-color: qlineargradient( x2:2 y2:2, x1:0 y1:2, stop:0 #1c1c1c, stop:1 #4a4a4a);\n"
                                   "color:#ffffff}")
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont('Retro Gaming')
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.menuFile.setFont(font)
        self.menuFile.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.menuFile.setStyleSheet("QMenu {background-color:#485563;\n"
                                    "color:#FFFFFF;} QMenu:selected {background-color: #29323c;}")
        self.menuFile.setToolTipsVisible(True)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.toolBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolBar.setStyleSheet("QToolBar{background-color: qlineargradient( x2:2 y2:2, x1:2 y1:0, stop:0 #1c1c1c, stop:1 #4a4a4a);\n"
                                   "border:#e41234;\n"
                                   "padding:2px;\n"
                                   "color:#e41234;}")
        self.toolBar.setMovable(True)
        self.toolBar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.toolBar.setOrientation(QtCore.Qt.Vertical)
        self.toolBar.setIconSize(QtCore.QSize(49, 63))
        self.toolBar.setFloatable(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)

        self.toolBar1 = QtWidgets.QToolBar(MainWindow)
        self.toolBar1.setEnabled(True)
        sizePolicy.setHeightForWidth(self.toolBar1.sizePolicy().hasHeightForWidth())
        # sizePolicy.setWidthForHeight(self.toolBar1.sizePolicy().hasWidthForHeight())
        self.toolBar1.setSizePolicy(sizePolicy)
        # self.toolBar1.setFixedWidth(100)
        self.toolBar1.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.toolBar1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolBar1.setStyleSheet("QToolBar{background-color: qlineargradient( x2:2 y2:2, x1:2 y1:0, stop:0 #1c1c1c, stop:1 #4a4a4a);\n"
                                   "border:#e41234;\n"
                                   "padding:2px;\n"
                                   "color:#e41234;}")
        self.toolBar1.setMovable(True)
        self.toolBar1.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.toolBar1.setOrientation(QtCore.Qt.Vertical)
        # self.toolBar1.setIconSize(QtCore.QSize(35, 49))
        self.toolBar1.setFloatable(True)
        self.toolBar1.setObjectName("toolBar1")
        MainWindow.addToolBar(QtCore.Qt.RightToolBarArea, self.toolBar1)

        self.actionAdd = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r"icons\plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd.setIcon(icon)
        self.actionAdd.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionAdd.setAutoRepeat(True)
        self.actionAdd.setVisible(True)
        self.actionAdd.setMenuRole(QtWidgets.QAction.TextHeuristicRole)
        self.actionAdd.setIconVisibleInMenu(True)
        self.actionAdd.setShortcutVisibleInContextMenu(False)
        self.actionAdd.setObjectName("actionAdd")

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(r"icons\export_csv.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setIcon(icon1)
        self.actionSave.setAutoRepeat(True)
        self.actionSave.setVisible(True)
        self.actionSave.setIconVisibleInMenu(True)
        self.actionSave.setShortcutVisibleInContextMenu(False)
        self.actionSave.setObjectName("actionSave")

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(r"icons\chart.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionChart = QtWidgets.QAction(MainWindow)
        self.actionChart.setIcon(icon2)
        self.actionChart.setAutoRepeat(True)
        self.actionChart.setVisible(True)
        self.actionChart.setIconVisibleInMenu(True)
        self.actionChart.setShortcutVisibleInContextMenu(False)
        self.actionChart.setObjectName("actionChart")

        self.hen = QtWidgets.QLabel(alignment=QtCore.Qt.AlignBottom)
        self.hen.setMinimumSize(QtCore.QSize(10, 10))
        self.hen.setMaximumSize(QtCore.QSize(40, 40))
        self.hen.setAlignment(QtCore.Qt.AlignBottom)
        self.hen.setObjectName("hen")
        self.movie = QMovie(r"icons\floppy2.gif")
        self.movie.setCacheMode(QMovie.CacheNone)
        
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionAdd)
        
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionAdd)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionChart)
        self.toolBar.addWidget(self.hen)

        self.toolBar1.addWidget(self.lbl3)
        self.toolBar1.addWidget(self.files_cnt_le)
        self.toolBar1.addSeparator()
        self.toolBar1.addWidget(self.lbl4)
        self.toolBar1.addWidget(self.time_step_le)
        self.toolBar1.addSeparator()
        self.toolBar1.addWidget(self.lbl5)
        self.toolBar1.addWidget(self.lambda_le)
        self.toolBar1.addSeparator()
        self.toolBar1.addWidget(self.settimeBtn)
        self.toolBar1.addSeparator()
        self.toolBar1.addWidget(self.openchartBtn)

        self.retranslateUi(MainWindow)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        """
            Menu naming
        """

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Spectroconverter"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.toolBar1.setWindowTitle(_translate("MainWindow", "toolBar1"))
        self.actionSave.setText(_translate("MainWindow", "Export to CSV"))
        self.actionChart.setText(_translate("MainWindow", "Create a chart"))
        self.actionAdd.setText(_translate("MainWindow", "Add"))


    def was_changed(self):
        """
            Mark for asking about saving file if something was changed
        """

        self.changesCB.setChecked(True)



class Progress(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        """
            Progress bar in console
        """

        sleep(3)
        for i in range(5):
            sleep(1)
            self.progress.emit(i+1)
        self.finished.emit()



class MyMainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        """
            Initialize actions
        """

        path = os.path.dirname(os.path.abspath(__file__))
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    
        actionSave = self.ui.actionSave
        actionSave.triggered.connect(lambda: self.save_csv())
        self.shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut.activated.connect(lambda: self.save_csv())
        
        actionAdd = self.ui.actionAdd
        actionAdd.triggered.connect(self.actAdd)

        actionChart = self.ui.actionChart
        actionChart.triggered.connect(self.create_chart)

        settimeBtn = self.ui.settimeBtn
        settimeBtn.clicked.connect(self.set_time)

        openchartBtn = self.ui.openchartBtn
        openchartBtn.clicked.connect(self.open_chart)

    alambda1 = []
    def actAdd(self):
        """
            Adding DATA files and calculate. 
            Reference and black files are constant for one group of calculations from spectrophotometer.
            Firstly, you need to write quantity of files, set time and write lambda value. Then, choose all DATA files from group and
            wait until it`s done.
        """

        rbdTbl = self.ui.rbdTbl
        resultTbl = self.ui.resultTbl
        timelambdaTbl = self.ui.timelambdaTbl
        chart1 = self.ui.canvas1
        arrA_selected_stored = self.alambda1
        lambda_le = self.ui.lambda_le
        gridLayout = self.ui.gridLayout
        stat = self.ui.stat
        actionAdd = self.ui.actionAdd

        self.thread = QThread()
        self.progress = Progress()
        self.progress.moveToThread(self.thread)
        self.thread.started.connect(self.progress.run)
        self.progress.finished.connect(self.thread.quit)
        self.progress.finished.connect(self.progress.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.progress.progress.connect(self.report_progress)

        actionAdd.setEnabled(False)
        self.thread.finished.connect(lambda: actionAdd.setEnabled(True))
        

        self.thread.finished.connect(lambda: stat.showMessage("Long-Running Step: 0"))
        
        ref_list_formated = []
        ref_list = []
        bl_list_formated = []
        bl_list = []
        lam_list_formated = []
        lam_list = []
        ll = []
        s = io.StringIO()

        
        with open('reference.txt', 'r') as fs:
            reader = csv.reader(fs, delimiter='\t')
            for line in fs:
                if line[0] == '>':
                    for ref_row in reader:
                        ref_list.append(ref_row[1])
                        lam_list.append(ref_row[0])
        
        for item in ref_list:
            ref_list_formated.append((item.replace(',','.')))
        for item in lam_list:
            lam_list_formated.append((item.replace(',','.')))

        rowCount = len(ref_list_formated)
        rbdTbl.setRowCount(rowCount)
        resultTbl.setRowCount(rowCount)

        for ref_row, one_ref_val in enumerate(ref_list_formated):
            ref_newItem = QTableWidgetItem(one_ref_val)
            rbdTbl.setItem(ref_row, 0, ref_newItem)
                
        for ref_row, one_ref_val1 in enumerate(lam_list_formated):
            ref_newItem1 = QTableWidgetItem(one_ref_val1)
            resultTbl.setItem(ref_row, 0, ref_newItem1)


        with open('black.txt', 'r') as fs1:
            black_reader = csv.reader(fs1, delimiter='\t')
            for line1 in fs1:
                if line1[0] == '>':
                    for bl_row in black_reader:
                        bl_list.append(bl_row[1])
        
        
        for item in bl_list:
            bl_list_formated.append((item.replace(',','.')))

        for bl_row, one_bl_val in enumerate(bl_list_formated):
            bl_newItem = QTableWidgetItem(one_bl_val)
            rbdTbl.setItem(bl_row, 1, bl_newItem)

        # stat.showMessage('In progress..')
        self.thread.start()
        fnames, _ = QFileDialog.getOpenFileNames(self, 'Open data files', '')
        
        # for i in tqdm(fnames):
        
        for fname in tqdm(fnames):
            data_list_formated = []
            data_list = []
            fmla_value_list = []
            with open(fname) as input_file:
                data_reader = csv.reader(input_file, delimiter='\t')
                for line2 in input_file:
                    if line2[0] == '>':
                        for data_row in data_reader:
                            data_list.append(data_row[1])
            
            for item in data_list:
                data_list_formated.append((item.replace(',','.')))

            for data_row, one_data_val in enumerate(data_list_formated):
                data_newItem = QTableWidgetItem(one_data_val)
                rbdTbl.setItem(data_row, 2, data_newItem)


            arrDn = np.array(data_list_formated, dtype=np.float32)
            arrY = np.array(bl_list_formated, dtype=np.float32)
            arrX = np.array(ref_list_formated, dtype=np.float32)
            arrLam = np.array(lam_list_formated, dtype=np.float32)
            fmla_value_list = -(np.log10(np.subtract(arrDn, arrY) / (np.subtract(arrX, arrY))))
            fmla_value_list_tformated = ['{:.2f}'.format(x) for x in fmla_value_list]

            for fmla_value_row, one_fmla_value in enumerate(fmla_value_list_tformated):
                av_newItem = QTableWidgetItem(one_fmla_value)
                resultTbl.setItem(fmla_value_row, 1, av_newItem)

            arrA = np.array(fmla_value_list_tformated, dtype=np.float32)
            chart1.axes.plot(arrLam, arrA)
            chart1.axes.set_xlabel('lambda')
            chart1.axes.set_ylabel('Abs')
            toolbar1 = NavigationToolbar(chart1, self)
            gridLayout.addWidget(toolbar1, 4, 0, 2, 2)
            chart1.draw()
            # 650,015
            # 520,274
            if lambda_le.text() in lam_list:
                arrA_selected_stored.append(fmla_value_list_tformated[lam_list.index(lambda_le.text())])
                for arrA_s_s_row, one_arrA_s_s_val in enumerate(arrA_selected_stored):
                    arrA_s_s_newItem = QTableWidgetItem(one_arrA_s_s_val)
                    timelambdaTbl.setItem(arrA_s_s_row, 1, arrA_s_s_newItem)
                    # print(arrA_selected_stored)
            # stat.showMessage(s.getvalue())
            # # print(s.getvalue())
            # sleep(.1)
                
        # stat.showMessage('Done!')
        # for i in tqdm(range(100), file=s):
        #     stat.showMessage(s.getvalue())
        #     stat.clearMessage()
        #     sleep(.1)
    
    def report_progress(self, file):
        """
            Checking progress
        """

        stat = self.ui.stat
        stat.showMessage(f"Current file: {file}")


    def set_time(self):
        """
            Set time for 3rd column (secs). First you need to write quantity of DATA files
        """
        
        timelambdaTbl = self.ui.timelambdaTbl
        files_cnt_le = self.ui.files_cnt_le
        time_step_le = self.ui.time_step_le
        time_step_list = []

        timelambdaTbl.setRowCount(int(files_cnt_le.text()))
        time_point = datetime.datetime(100, 1, 1, 0, 00, 00)

        for _ in range(0, int(files_cnt_le.text())):
            time_step_list.append('{:02}'.format(int(time_point.minute))+':'+'{:02}'.format(int(time_point.second)))
            time_point = time_point + datetime.timedelta(0, int(time_step_le.text()))       
        
        for tm_row, one_tm_val in enumerate(time_step_list):
            tm_newItem = QTableWidgetItem(one_tm_val)
            timelambdaTbl.setItem(tm_row, 0, tm_newItem)


    def create_chart(self):
        """
            Creating chart by values from 3rd column
        """

        rbdTbl = self.ui.rbdTbl
        resultTbl = self.ui.resultTbl
        timelambdaTbl = self.ui.timelambdaTbl
        chart2 = self.ui.canvas2
        gridLayout = self.ui.gridLayout

        timeX = []
        lambdaY = []
        rowCount = timelambdaTbl.rowCount()

        for row in range(rowCount):
            for col in range(timelambdaTbl.columnCount()):
                timeX.append(timelambdaTbl.item(row, 0).text())
                lambdaY.append(float(timelambdaTbl.item(row, 1).text()))
        chart2.axes.plot(timeX, lambdaY)
        chart2.axes.set_xlabel('time')
        chart2.axes.set_ylabel('Abs')
        toolbar = NavigationToolbar(chart2, self)
        gridLayout.addWidget(toolbar, 4, 2, 1, 1)
        chart2.draw()


    def open_chart(self):
        """
            Open chart in fullsized mode
        """
        
        gridLayout = self.ui.gridLayout
        chart2 = self.ui.canvas2

        self.setCentralWidget(chart2)

        
    def save_csv(self):
        """
            Save calculated values from 3rd column to csv file
        """

        resultTbl = self.ui.resultTbl
        timelambdaTbl = self.ui.timelambdaTbl
        # path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV(*.csv)')
        # if not path.isEmpty():
        datetime = QDateTime.currentDateTime()
        cur_date = datetime.toString('dd.MM.yyyy hh.mm.ss')
        with open('result '+cur_date+'.csv', 'w') as stream:
            writer = csv.writer(stream, dialect='excel', delimiter=';', lineterminator='\n')
            for row in range(timelambdaTbl.rowCount()):
                rowdata = []
                for column in range(timelambdaTbl.columnCount()):
                    item = timelambdaTbl.item(row, column)
                    if item is not None:
                        rowdata.append(item.text())
                    else:
                        rowdata.append('')
                writer.writerow(rowdata)



    # def closeEvent(self, event):
        
    #     changesCB = self.ui.changesCB
    #     if changesCB.isChecked():
    #         should_save = QtWidgets.QMessageBox.question(self, "Save data", 
    #                                                     "Should the data be saved?",
    #                                                     defaultButton = QtWidgets.QMessageBox.Yes)
    #         if should_save == QtWidgets.QMessageBox.Yes:
    #             self.write_to_file(self.save_file)
    #         return super().closeEvent(event)

# class Log(QtWidgets.QStatusBar):

# class LogTextEdit(QtWidgets.QStatusBar):
#     def write(self, message):
#         if not hasattr(self, "flag"):
#             self.flag = False
#         message = message.replace('\r', '').rstrip()
#         if message:
#             method = "replace_last_line" if self.flag else "appendPlainText"
#             QtCore.QMetaObject.invokeMethod(self, method, QtCore.Qt.QueuedConnection, QtCore, Q_ARG(str, message))
#             self.flag = True
#         else:
#             self.flag = False

#     @QtCore.pyqtSlot(str)
#     def replace_last_line(self, text):
#         cursor = self.textCursor()
#         cursor.movePosition(QtGui.QTextCursor.End)
#         cursor.select(QtGui.QTextCursor.BlockUnderCursor)
#         cursor.removeSelectedText()
#         cursor.insertBlock()
#         self.setTextCursor(cursor)
#         self.insertPlainText(text)

# def foo(w):
#     for i in tqdm(range(100), file=w):
#         sleep(0.1)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # w = LogTextEdit()
    # threading.Thread(target=foo, args=(w,), daemon=True).start()
    MainWindow = MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())