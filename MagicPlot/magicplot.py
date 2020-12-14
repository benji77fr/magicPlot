# -*- coding: utf-8 -*-

"""
Created on 2020/04/06

Author: Benjamin Girard

Copyright: SoftBank Robotics 2020
"""

from PyQt5 import QtWidgets, QtCore, QtGui

import sys
import pandas as pd
import os

import pyqtgraph as pg
import pyqtgraph.exporters

from graph import CustomPlotWidget
from mouse_tracking import Crosshair
from csvMod import csvMod

class MainWindow(QtGui.QMainWindow):
    '''
    Class MainWindow

    Génération de l'IHM
    '''
    def __init__(self):
        super(MainWindow, self).__init__()

        # Titre de la Fênetre principale
        self.setWindowTitle("Magic Plot for CEM")

        # Création d'un objet CustomPlotWidget
        self.graph = CustomPlotWidget()
        self.csvmod = csvMod()

        # Création du Layout et du Widget principal
        layout = QtGui.QGridLayout()
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        
        # Création des actions menu
        actionOpen = QtWidgets.QAction("&File", self)
        actionOpen.setShortcut('Ctrl+O')
        actionOpen.setStatusTip("Open one or multiple files")
        actionOpen.triggered.connect(self.open_files)

        actionSaveMax = QtWidgets.QAction("Save Max", self)
        actionSaveMax.setStatusTip("Save the max plot in a csv file")
        actionSaveMax.triggered.connect(self.save_max)

        actionPlot = QtWidgets.QAction("&Plot", self)
        actionPlot.setStatusTip("Plot one or multiple curves")
        actionPlot.triggered.connect(self.read_and_plot)

        actionPlotMax = QtWidgets.QAction("Plot max", self)
        actionPlotMax.setStatusTip("Plot the maximum value among the file set")
        actionPlotMax.triggered.connect(self.find_max)

        actionAddClasseA = QtWidgets.QAction("Classe A", self)
        actionAddClasseA.setStatusTip("Ajoute le gabarit de la classe A")
        actionAddClasseA.triggered.connect(lambda: self.graph.add_gabarit('A'))

        actionAddClasseB = QtWidgets.QAction("Classe B", self)
        actionAddClasseB.setStatusTip("Ajoute le gabarit de la classe B")
        actionAddClasseB.triggered.connect(lambda: self.graph.add_gabarit('B'))

        rangeER = QtWidgets.QAction("Mesure ER", self)
        rangeER.setStatusTip("Set range for ER")
        rangeER.triggered.connect(lambda: self.graph.change_range('ER'))

        rangeEC = QtWidgets.QAction("Mesure EC", self)
        rangeEC.setStatusTip("Set range for EC")
        rangeEC.triggered.connect(lambda: self.graph.change_range('EC'))

        actionRemoveCA = QtWidgets.QAction("Remove Classe A", self)
        actionRemoveCA.triggered.connect(lambda: self.graph.remove_gabarit('Classe A'))

        actionRemoveCB= QtWidgets.QAction("Remove Classe B", self)
        actionRemoveCB.triggered.connect(lambda: self.graph.remove_gabarit('Classe B'))

        actionCSV = QtWidgets.QAction("Change extension file", self)
        actionCSV.triggered.connect(self.csvmod.open_file)

        exportImg = QtWidgets.QAction("Export results as img", self)
        exportImg.triggered.connect(self.exportImg)

        clearPlot = QtWidgets.QAction("Clear plot zone", self)
        clearPlot.triggered.connect(self.plot_clear)

        clearSelection = QtWidgets.QAction("Clear Plot and File selection", self)
        clearSelection.triggered.connect(self.clear_file_and_plot)

        # Création du Menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(actionOpen)
        fileMenu.addAction(actionSaveMax)
        fileMenu.addAction(actionCSV)
        plotMenu = menubar.addMenu('&Plot')
        plotMenu.addAction(actionPlot)
        plotMenu.addAction(actionPlotMax)
        plotMenu.addAction(clearPlot)
        plotMenu.addAction(clearSelection)
        plotMenu.addAction(exportImg)
        addGabaritMenu = plotMenu.addMenu('Ajouter gabarit')
        addGabaritMenu.addAction(actionAddClasseA)
        addGabaritMenu.addAction(actionAddClasseB)
        removeGabaritMenu = plotMenu.addMenu('Remove gabarit')
        removeGabaritMenu.addAction(actionRemoveCA)
        removeGabaritMenu.addAction(actionRemoveCB)
        changeRangeMenu = plotMenu.addMenu('Change range')
        changeRangeMenu.addAction(rangeER)
        changeRangeMenu.addAction(rangeEC)
        

        
        # Création des Labels pour les listWidgets
        self.labelFile = QtWidgets.QLabel("Liste de fichiers")
        self.labelPlot = QtWidgets.QLabel("Liste de courbes")
        fontLabel = QtGui.QFont()
        fontLabel.setPointSize(15)
        fontLabel.setBold(True)
        self.labelFile.setFont(fontLabel)
        self.labelFile.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPlot.setFont(fontLabel)
        self.labelPlot.setAlignment(QtCore.Qt.AlignCenter)

        # Création des listWidgets qui contiendront les fichiers
        # et les plots
        self.listFile = QtWidgets.QListWidget()
        self.listPlot = QtWidgets.QListWidget()

        # Création de la partie gauche du layout
        # Ce layout contient les Labels et les listWidget
        layoutLeft = QtGui.QVBoxLayout()
        layoutLeft.addWidget(self.labelFile)
        layoutLeft.addWidget(self.listFile)
        layoutLeft.addWidget(self.labelPlot)
        layoutLeft.addWidget(self.listPlot)
        
        # Ajout des parties gauche et droite dans 
        # le layout principal
        layout.addLayout(layoutLeft, 0, 0)    
        layout.addWidget(self.graph, 0, 1)
        layout.setColumnStretch(1, 3)

        self.mouse_tracking = Crosshair(self.graph.plot_item)

        # Création d'une status bar    
        self.setStatusBar(QtWidgets.QStatusBar(self))

        # Définition du widget central de la Mainwindow
        # par notre widget principal
        self.setCentralWidget(widget)
        

        self.sourceFiles = []
        self.selectedFiles = []
        self.selectedPlot = []
        self.curves = {}
        self.filesPath = ""
        self.max_df = pd.DataFrame()

        # Signal émit quand on coche/décoche une case dans 
        # les ListWidget
        self.listFile.itemChanged.connect(self.checked_files)
        self.listPlot.itemChanged.connect(self.checked_plot)


    def populate_list_of_files(self, listFiles):
        '''
        Parcours la liste de fichiers ouvert et rempli la ListWidget
        en prenant le nom du fichier + extension

        param:
        listFiles: Contient les fichiers ouvert
        '''
        for f in listFiles:
            self.filesPath = os.path.dirname(f)
            f_name = os.path.basename(f)
            item = QtWidgets.QListWidgetItem(f_name)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            if not self.listFile.findItems(item.text(), QtCore.Qt.MatchExactly):
                self.listFile.addItem(item)
    
    def populate_list_of_plot(self):
        '''
        Parcours la liste d'item contenu dans le PlotItem et rempli la
        ListWidget en prenant le nom du plot
        '''
        for p in self.graph.plot_item.items:
            if type(p) is pg.graphicsItems.PlotDataItem.PlotDataItem:
                p_name = p.name()
                self.curves[p_name] = p
                item = QtWidgets.QListWidgetItem(p_name)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Checked)
                if not self.listPlot.findItems(item.text(), QtCore.Qt.MatchExactly):
                    self.listPlot.addItem(item)
                    self.selectedPlot.append(item)
            else:
                continue

    def open_files(self):
        '''
        Ouvre une fenêtre de dialogue pour sélectionner le ou les fichiers
        à ouvrir
        '''
        fileName, _ = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                  "Ouvrir un fichier CSV", "",
                                                  "All Files (*);;CSV Files (*.csv)")

        if fileName:
            for f in fileName:
                if f not in self.sourceFiles:
                    self.sourceFiles.append(f)

        self.populate_list_of_files(self.sourceFiles)
    
    def checked_files(self):
        '''
        Fonction appelée lorsque l'on coche/décoche un élément de
        listFile(ListWidget)
        Permet de garder une trace des fichiers sélectionnés dans la liste
        '''
        model = self.listFile.model()
        for index in range(model.rowCount()):
            item = self.listFile.item(index)
            if item.checkState() == QtCore.Qt.Checked and item not in self.selectedFiles:
                self.selectedFiles.append(item)
            if item.checkState() == QtCore.Qt.Unchecked and item in self.selectedFiles:
                self.selectedFiles.remove(item)

    def checked_plot(self):

        '''
        Fonction appelée lorque l'on coche/décoche un élément de
        listPlot(ListWidget)
        Permet d'afficher ou non les courbes présente dans la liste
        Permet de garder une trace des courbes tracées
        '''
        model = self.listPlot.model()
        for index in range(model.rowCount()):
            item = self.listPlot.item(index)
            if item.checkState() == QtCore.Qt.Checked and item not in self.selectedPlot:
                self.selectedPlot.append(item)
                self.graph.plot_item.addItem(self.curves[item.text()])
                self.mouse_tracking.update()
            if item.checkState() == QtCore.Qt.Unchecked and item in self.selectedPlot:
                self.selectedPlot.remove(item)
                self.graph.plot_item.removeItem(self.curves[item.text()])
                self.mouse_tracking.update()
        
        
    
    def read_and_plot(self):
        '''
        Extrait les données présente dans les fichiers sélectionnés
        et ajoute une courbe dans le PlotItem
        '''
        indexColor = 0

        for itemRead in self.selectedFiles:
            df = pd.read_csv((self.filesPath + "/" + itemRead.text()), sep=";")

            data_x = df['frequence']
            data_y = df['level']

            pencil = pg.mkPen(color=pg.intColor(indexColor))
            curveName = itemRead.text().split('.')[0]

            self.graph.plot_item.plot(data_x, data_y, pen=pencil, name=curveName)
            indexColor = indexColor + 2
        
        self.populate_list_of_plot()
        self.mouse_tracking.update()

    def plot_clear(self):
        self.graph.plot_item.clear()
        self.graph.plot_item.addItem(self.mouse_tracking.vline, ignoreBounds=True)
        self.graph.plot_item.addItem(self.mouse_tracking.hline, ignoreBounds=True)
        self.graph.plot_item.addItem(self.mouse_tracking.labelx, ignoreBounds=True)
        self.graph.plot_item.addItem(self.mouse_tracking.labely, ignoreBounds=True)

    def clear_file_and_plot(self):
        self.selectedFiles.clear()
        self.listFile.clear()
        self.selectedPlot.clear()
        self.listPlot.clear()

    def save_max(self):
        '''
        Sauvegarde dans un fichier CSV les valurs de la courbe générer
        en cherchant le maximum (find_max)
        '''
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                  "Enregistrer un fichier CSV", "", 
                                                  "CSV Files (*.csv)")
        self.max_df.to_csv(fileName, index=False, header=True, sep=";")
                                        
    def find_max(self):
        '''
        Permet de trouver les valeurs max en fonction d'une fréquence donnée
        en comparant X fichier
        '''
        isFirstFile = True
        list_of_dfs = []

        for itemRead in self.selectedFiles:
            if isFirstFile:
                df = pd.read_csv((self.filesPath + "/" + itemRead.text()), sep=";")
                list_of_dfs.append(df)
                isFirstFile = False
            else:
                df = pd.read_csv((self.filesPath + "/" + itemRead.text()), sep=";", usecols=[1])
                list_of_dfs.append(df)
           
        combine_df = pd.concat(list_of_dfs, axis=1)

        temp_df = combine_df.loc[:, 'level']
        maxLevel_df = pd.DataFrame({'level': temp_df.max(axis=1)})

        data_x = combine_df["frequence"]
        data_y = maxLevel_df["level"]

        self.graph.plot_item.plot(data_x, data_y, pen='b', name='Maximum')

        self.max_df = pd.DataFrame(list(zip(data_x,data_y)), columns=['frequence','level'])

    def exportImg(self):
        exporter = pg.exporters.ImageExporter(self.graph.plot_item)

        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                  "Exporter un tracer", "",
                                                  "Jpeg Files (*.jpg);; PNG Files (*.png)")

        exporter.parameters()['width'] = 1440

        exporter.export(fileName)

def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show() 

    sys.exit(app.exec_()) 

if __name__ == "__main__":
    main()