# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\views\designer\mainwindow.ui'
#
# Created: Wed May  1 02:21:54 2019
#      by: pyside2-uic 2.0.0 running on PySide2 5.6.0~a1
#
# WARNING! All changes made in this file will be lost!

import src.views.resources_rc
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtWidgets import QHBoxLayout, QGridLayout, QGroupBox, QListView
from PySide2.QtWidgets import QSizePolicy, QAbstractItemView
from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton, QTextBrowser
from PySide2.QtWidgets import QMenu, QMenuBar, QAction, QStatusBar

from src.views.graph_view import GraphView


class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 700)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            ":/res/designer/icons/01_Warning_48x48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.mainLayout = QHBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName("mainLayout")

        # Left Group

        self.explorerGroup = QGroupBox(self.centralwidget)
        self.explorerGroup.setObjectName("explorerGroup")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        self.explorerGroup.setSizePolicy(sizePolicy)

        self.gridExplorer = QGridLayout(self.explorerGroup)
        self.gridExplorer.setObjectName("gridExplorer")
        self.isoExplorer = QListView(self.explorerGroup)
        self.isoExplorer.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        self.isoExplorer.setSelectionMode(
            QAbstractItemView.ExtendedSelection)
        self.isoExplorer.setObjectName("isoExplorer")
        self.gridExplorer.addWidget(self.isoExplorer, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.explorerGroup)

        # Middle Group

        self.propertiesGroup = QGroupBox(self.centralwidget)
        self.propertiesGroup.setObjectName("propertiesGroup")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        self.propertiesGroup.setSizePolicy(sizePolicy)
        self.gridProperties = QGridLayout(self.propertiesGroup)
        self.gridProperties.setObjectName("gridProperties")

        self.materialNameLabel = QLabel(self.propertiesGroup)
        self.materialNameLabel.setObjectName("materialNameLabel")
        self.gridProperties.addWidget(self.materialNameLabel, 0, 0, 1, 1)
        self.materialNameLineEdit = QLineEdit(self.propertiesGroup)
        self.materialNameLineEdit.setObjectName("materialNameLineEdit")
        self.gridProperties.addWidget(self.materialNameLineEdit, 0, 1, 1, 1)
        self.materialBatchLabel = QLabel(self.propertiesGroup)
        self.materialBatchLabel.setObjectName("materialBatchLabel")
        self.gridProperties.addWidget(self.materialBatchLabel, 1, 0, 1, 1)
        self.materialBatchLineEdit = QLineEdit(self.propertiesGroup)
        self.materialBatchLineEdit.setObjectName("materialBatchLineEdit")
        self.gridProperties.addWidget(self.materialBatchLineEdit, 1, 1, 1, 1)
        self.temperatureLabel = QLabel(self.propertiesGroup)
        self.temperatureLabel.setObjectName("temperatureLabel")
        self.gridProperties.addWidget(self.temperatureLabel, 3, 0, 1, 1)
        self.temperatureLineEdit = QLineEdit(self.propertiesGroup)
        self.temperatureLineEdit.setObjectName("temperatureLineEdit")
        self.gridProperties.addWidget(self.temperatureLineEdit, 3, 1, 1, 1)
        self.adsorbateLabel = QLabel(self.propertiesGroup)
        self.adsorbateLabel.setObjectName("adsorbateLabel")
        self.gridProperties.addWidget(self.adsorbateLabel, 2, 0, 1, 1)
        self.adsorbateLineEdit = QLineEdit(self.propertiesGroup)
        self.adsorbateLineEdit.setObjectName("adsorbateLineEdit")
        self.gridProperties.addWidget(self.adsorbateLineEdit, 2, 1, 1, 1)
        self.textInfo = QTextBrowser(self.propertiesGroup)
        self.textInfo.setObjectName("textInfo")
        self.gridProperties.addWidget(self.textInfo, 4, 0, 1, 2)
        self.dataButton = QPushButton(self.propertiesGroup)
        self.dataButton.setObjectName("dataButton")
        self.gridProperties.addWidget(self.dataButton, 5, 0, 1, 1)
        self.freezeButton = QPushButton(self.propertiesGroup)
        self.freezeButton.setObjectName("freezeButton")
        self.gridProperties.addWidget(self.freezeButton, 5, 1, 1, 1)
        self.mainLayout.addWidget(self.propertiesGroup)

        # Right group

        self.graphGroup = QGroupBox(self.centralwidget)
        self.graphGroup.setObjectName("graphGroup")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        self.graphGroup.setSizePolicy(sizePolicy)

        self.gridGraph = QGridLayout(self.graphGroup)
        self.gridGraph.setObjectName("gridGraph")
        self.graphicsView = GraphView(self.graphGroup)
        self.graphicsView.setObjectName("graphicsView")
        self.gridGraph.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.graphGroup)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuCharact = QMenu(self.menubar)
        self.menuCharact.setObjectName("menuCharact")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuModel = QMenu(self.menubar)
        self.menuModel.setObjectName("menuModel")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionOpen = QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(
            ":/res/icons/10_Search_48x48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setObjectName("actionOpen")

        self.actionSave = QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/res/icons/04_Save_48x48.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionSave.setObjectName("actionSave")

        self.actionQuit = QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(
            ":/res/icons/14_Delete_48x48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon3)
        self.actionQuit.setObjectName("actionQuit")

        self.actionAbout = QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/res/icons/15_Tick_48x48.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon4)
        self.actionAbout.setObjectName("actionAbout")

        self.actionBET_Surface_Area = QAction(MainWindow)
        self.actionBET_Surface_Area.setObjectName("actionBET_Surface_Area")
        self.actionLangmuir_Surface_Area = QAction(MainWindow)
        self.actionLangmuir_Surface_Area.setObjectName(
            "actionLangmuir_Surface_Area")
        self.actiont_plot = QAction(MainWindow)
        self.actiont_plot.setObjectName("actiont_plot")
        self.actionalpha_s_plot = QAction(MainWindow)
        self.actionalpha_s_plot.setObjectName("actionalpha_s_plot")
        self.actionMicroporous_PSD = QAction(MainWindow)
        self.actionMicroporous_PSD.setObjectName("actionMicroporous_PSD")
        self.actionMesoporous_PSD = QAction(MainWindow)
        self.actionMesoporous_PSD.setObjectName("actionMesoporous_PSD")
        self.actionDFT_Kernel_PSD = QAction(MainWindow)
        self.actionDFT_Kernel_PSD.setObjectName("actionDFT_Kernel_PSD")
        self.actionModel_By = QAction(MainWindow)
        self.actionModel_By.setObjectName("actionModel_By")
        self.actionGuess_Model = QAction(MainWindow)
        self.actionGuess_Model.setObjectName("actionGuess_Model")

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuCharact.addAction(self.actionBET_Surface_Area)
        self.menuCharact.addAction(self.actionLangmuir_Surface_Area)
        self.menuCharact.addSeparator()
        self.menuCharact.addAction(self.actiont_plot)
        self.menuCharact.addAction(self.actionalpha_s_plot)
        self.menuCharact.addSeparator()
        self.menuCharact.addAction(self.actionMicroporous_PSD)
        self.menuCharact.addAction(self.actionMesoporous_PSD)
        self.menuCharact.addAction(self.actionDFT_Kernel_PSD)
        self.menuModel.addAction(self.actionModel_By)
        self.menuModel.addAction(self.actionGuess_Model)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCharact.menuAction())
        self.menubar.addAction(self.menuModel.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QApplication.translate(
            "MainWindow", "pyGAPS-gui", None, -1))
        self.propertiesGroup.setTitle(QApplication.translate(
            "MainWindow", "Isotherm Properties", None, -1))
        self.temperatureLabel.setText(QApplication.translate(
            "MainWindow", "Temperature (K)", None, -1))
        self.materialBatchLabel.setText(QApplication.translate(
            "MainWindow", "Material Batch", None, -1))
        self.adsorbateLabel.setText(QApplication.translate(
            "MainWindow", "Adsorbate", None, -1))
        self.materialNameLabel.setText(QApplication.translate(
            "MainWindow", "Material Name", None, -1))
        self.dataButton.setText(QApplication.translate(
            "MainWindow", "Data", None, -1))
        self.freezeButton.setText(QApplication.translate(
            "MainWindow", "Freeze ->", None, -1))
        self.graphGroup.setTitle(QApplication.translate(
            "MainWindow", "Isotherm Overlay", None, -1))
        self.menuFile.setTitle(QApplication.translate(
            "MainWindow", "File", None, -1))
        self.menuCharact.setTitle(QApplication.translate(
            "MainWindow", "Characterization", None, -1))
        self.menuHelp.setTitle(QApplication.translate(
            "MainWindow", "Help", None, -1))
        self.menuModel.setTitle(QApplication.translate(
            "MainWindow", "Model", None, -1))
        self.actionOpen.setText(QApplication.translate(
            "MainWindow", "Open", None, -1))
        self.actionSave.setText(QApplication.translate(
            "MainWindow", "Save", None, -1))
        self.actionQuit.setText(QApplication.translate(
            "MainWindow", "Quit", None, -1))
        self.actionAbout.setText(QApplication.translate(
            "MainWindow", "About", None, -1))
        self.actionBET_Surface_Area.setText(QApplication.translate(
            "MainWindow", "BET Surface Area", None, -1))
        self.actionLangmuir_Surface_Area.setText(QApplication.translate(
            "MainWindow", "Langmuir Surface Area", None, -1))
        self.actiont_plot.setText(QApplication.translate(
            "MainWindow", "t-plot", None, -1))
        self.actionalpha_s_plot.setText(QApplication.translate(
            "MainWindow", "alpha-s plot", None, -1))
        self.actionMicroporous_PSD.setText(QApplication.translate(
            "MainWindow", "Microporous PSD", None, -1))
        self.actionMesoporous_PSD.setText(QApplication.translate(
            "MainWindow", "Mesoporous PSD", None, -1))
        self.actionDFT_Kernel_PSD.setText(QApplication.translate(
            "MainWindow", "DFT Kernel PSD", None, -1))
        self.actionModel_By.setText(QApplication.translate(
            "MainWindow", "Model Using", None, -1))
        self.actionGuess_Model.setText(QApplication.translate(
            "MainWindow", "Model Guess", None, -1))
