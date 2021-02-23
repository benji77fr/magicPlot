# -*- coding: utf-8 -*-

"""
Created on 2020/04/06

Author: Benjamin Girard

Copyright: SoftBank Robotics 2020
"""

from PyQt5 import QtWidgets, QtCore, QtGui
import qrc_ressources
import qtawesome as qta

import sys
import pandas as pd
import os

import pyqtgraph as pg
from pyqtgraph import exporters

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
        self.mouse_tracking = Crosshair(self.graph.plot_item)

        # Création du Layout et du Widget principal
        layout = QtGui.QGridLayout()
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        # Création des actions menu
        actionOpen = QtWidgets.QAction(
            qta.icon('fa.folder-open', color='#ffc47d'), "&Ouvrir", self)
        actionOpen.setShortcut('Ctrl+O')
        actionOpen.setStatusTip("Ouvre un ou plusieurs fichiers")
        actionOpen.triggered.connect(self.open_files)

        actionSaveMax = QtWidgets.QAction(qta.icon('mdi.content-save'), "Sauvegarder Max", self)
        actionSaveMax.setStatusTip(
            "Sauvegarde le maximum pour chaque point dans un fichier CSV")
        actionSaveMax.triggered.connect(self.save_max)

        actionPlot = QtWidgets.QAction(qta.icon('mdi.chart-bell-curve-cumulative'), "&Tracer", self)
        actionPlot.setStatusTip("Trace une ou plusieurs courbes")
        actionPlot.triggered.connect(self.read_and_plot)

        actionPlotMax = QtWidgets.QAction("Tracer Max", self)
        actionPlotMax.setStatusTip(
            "Trace la courbe représentant le maximum pour chaque point mesuré")
        actionPlotMax.triggered.connect(self.find_max)

        actionAddClasseA = QtWidgets.QAction("Classe A à 1m", self)
        actionAddClasseA.setStatusTip("Ajoute le gabarit de la classe A à 1m")
        actionAddClasseA.triggered.connect(lambda: self.graph.add_gabarit('A1'))

        actionAddClasseB = QtWidgets.QAction("Classe B à 1m", self)
        actionAddClasseB.setStatusTip("Ajoute le gabarit de la classe B à 1m")
        actionAddClasseB.triggered.connect(lambda: self.graph.add_gabarit('B1'))

        actionAddClasseA10 = QtWidgets.QAction("Classe A à 10m", self)
        actionAddClasseA10.setStatusTip("Ajoute le gabarit de la classe A à 10m")
        actionAddClasseA10.triggered.connect(lambda: self.graph.add_gabarit('A10'))

        actionAddClasseB10 = QtWidgets.QAction("Classe B à 10m", self)
        actionAddClasseB10.setStatusTip("Ajoute le gabarit de la classe B à 10m")
        actionAddClasseB10.triggered.connect(lambda: self.graph.add_gabarit('B10'))

        rangeER = QtWidgets.QAction("Mesure ER", self)
        rangeER.setStatusTip(
            "Change l'ordre de grandeur en abscisse pour les mesures en ER")
        rangeER.triggered.connect(lambda: self.graph.change_range('ER'))

        rangeEC = QtWidgets.QAction("Mesure EC", self)
        rangeEC.setStatusTip(
            "Change l'ordre de grandeur en abscisse pour les mesures en EC")
        rangeEC.triggered.connect(lambda: self.graph.change_range('EC'))

        actionRemoveCA = QtWidgets.QAction("Enlever Classe A", self)
        actionRemoveCA.triggered.connect(
            lambda: self.graph.remove_gabarit('Classe A'))

        actionRemoveCB = QtWidgets.QAction("Enlever Classe B", self)
        actionRemoveCB.triggered.connect(
            lambda: self.graph.remove_gabarit('Classe B'))

        actionCSV = QtWidgets.QAction(qta.icon('fa5s.file-csv', color='#3a9c55'), "Traiter les fichiers", self)
        actionCSV.triggered.connect(self.csvmod.open_file)

        exportImg = QtWidgets.QAction(qta.icon('mdi.file-export-outline'), "Exporter", self)
        exportImg.triggered.connect(self.exportImg)

        clearPlot = QtWidgets.QAction("Nettoyer la zone de tracer", self)
        clearPlot.triggered.connect(self.plot_clear)

        clearSelection = QtWidgets.QAction(
            "Nettoyer la liste des tracer", self)
        clearSelection.triggered.connect(self.clear_file_and_plot)

        actionBackgroundWhite = QtWidgets.QAction("Fond Blanc", self)
        actionBackgroundWhite.triggered.connect(
            lambda: self.change_background_color('white'))

        actionBackgroundBlack = QtWidgets.QAction("Fond Noir", self)
        actionBackgroundBlack.triggered.connect(
            lambda: self.change_background_color('black'))
        
        changeColor = QtWidgets.QAction(qta.icon('mdi.chart-bell-curve-cumulative', 'mdi.format-color-fill', options=[{'scale_factor': 1.2}, {'color': 'red'}]), "Changer la couleur d'une courbe", self)
        changeColor.triggered.connect(self.change_plot_color)

        # Création du Menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Fichier')
        fileMenu.addAction(actionOpen)
        fileMenu.addAction(actionSaveMax)
        fileMenu.addAction(actionCSV)
        fileMenu.addAction(exportImg)
        plotMenu = menubar.addMenu('&Tracer')
        plotMenu.addAction(actionPlot)
        plotMenu.addAction(actionPlotMax)
        plotMenu.addAction(clearPlot)
        plotMenu.addAction(clearSelection)
        addGabaritMenu = plotMenu.addMenu('Ajouter gabarit')
        addGabaritMenu.addAction(actionAddClasseA)
        addGabaritMenu.addAction(actionAddClasseA10)
        addGabaritMenu.addAction(actionAddClasseB)
        addGabaritMenu.addAction(actionAddClasseB10)
        removeGabaritMenu = plotMenu.addMenu('Enlever gabarit')
        removeGabaritMenu.addAction(actionRemoveCA)
        removeGabaritMenu.addAction(actionRemoveCB)
        changeRangeMenu = plotMenu.addMenu("Changer l'abscisse")
        changeRangeMenu.addAction(rangeER)
        changeRangeMenu.addAction(rangeEC)
        settingsMenu = menubar.addMenu('&Réglages')
        changeBackground = settingsMenu.addMenu('Changer le Fond')
        changeBackground.addAction(actionBackgroundWhite)
        changeBackground.addAction(actionBackgroundBlack)

        # Création Toolbar

        fileToolBar = self.addToolBar("Fichier")
        fileToolBar.addAction(actionCSV)
        fileToolBar.addAction(actionOpen)
        fileToolBar.addSeparator()
        fileToolBar.addAction(changeColor)


        # Création des Labels pour les listWidgets
        self.labelPlot = QtWidgets.QLabel("Liste de courbes")
        fontLabel = QtGui.QFont()
        fontLabel.setPointSize(15)
        fontLabel.setBold(True)
        self.labelPlot.setFont(fontLabel)
        self.labelPlot.setAlignment(QtCore.Qt.AlignCenter)

        # Création des listWidgets qui contiendront les fichiers
        # et les plots
        self.listPlot = QtWidgets.QListWidget()

        # Création de la partie gauche du layout
        # Ce layout contient les Labels et les listWidget
        layoutLeft = QtGui.QVBoxLayout()
        layoutLeft.addWidget(self.labelPlot)
        layoutLeft.addWidget(self.listPlot)

        # Ajout des parties gauche et droite dans
        # le layout principal
        layout.addLayout(layoutLeft, 0, 0)
        layout.addWidget(self.graph, 0, 1)
        layout.setColumnStretch(1, 3)

        # Création d'une status bar
        self.setStatusBar(QtWidgets.QStatusBar(self))

        # Définition du widget central de la Mainwindow
        # par notre widget principal
        self.setCentralWidget(widget)

        self.sourceFiles = []
        self.selectedPlot = []
        self.curves = {}
        self.filesPath = ""
        self.max_df = pd.DataFrame()

        # Signal émit quand on coche/décoche une case dans
        # les ListWidget
        self.listPlot.itemChanged.connect(self.checked_plot)

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

        # self.populate_list_of_files(self.sourceFiles)
        self.read_and_plot(self.sourceFiles)

        self.sourceFiles.clear()

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

    def read_and_plot(self, sourceFiles):
        '''
        Extrait les données présente dans les fichiers sélectionnés
        et ajoute une courbe dans le PlotItem
        '''
        indexColor = 0
        sourceFiles = sourceFiles

        for itemRead in sourceFiles:
            df = pd.read_csv((os.path.dirname(itemRead) +
                              "/" + os.path.basename(itemRead)), sep=";")

            data_x = df['frequence']
            data_y = df['level']

            pencil = pg.mkPen(color=pg.intColor(indexColor))
            curveName = os.path.basename(itemRead).split('.')[0]

            self.graph.plot_item.plot(
                data_x, data_y, pen=pencil, name=curveName, clickable=True)
            indexColor = indexColor + 2

        self.populate_list_of_plot()
        self.mouse_tracking.update()

    def plot_clear(self):
        self.graph.plot_item.clear()
        self.graph.plot_item.addItem(
            self.mouse_tracking.vline, ignoreBounds=True)
        self.graph.plot_item.addItem(
            self.mouse_tracking.hline, ignoreBounds=True)
        self.graph.plot_item.addItem(
            self.mouse_tracking.labelx, ignoreBounds=True)
        self.graph.plot_item.addItem(
            self.mouse_tracking.labely, ignoreBounds=True)

    def clear_file_and_plot(self):
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
        sourceFiles = []

        fileName, _ = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                             "Ouvrir un fichier CSV", "",
                                                             "All Files (*);;CSV Files (*.csv)")

        if fileName:
            for f in fileName:
                sourceFiles.append(f)

        for itemRead in sourceFiles:
            if isFirstFile:
                df = pd.read_csv(
                    (os.path.dirname(itemRead) + "/" + os.path.basename(itemRead)), sep=";")
                list_of_dfs.append(df)
                isFirstFile = False
            else:
                df = pd.read_csv(
                    (os.path.dirname(itemRead) + "/" + os.path.basename(itemRead)), sep=";", usecols=[1])
                list_of_dfs.append(df)

        combine_df = pd.concat(list_of_dfs, axis=1)

        temp_df = combine_df.loc[:, 'level']
        maxLevel_df = pd.DataFrame({'level': temp_df.max(axis=1)})

        data_x = combine_df["frequence"]
        data_y = maxLevel_df["level"]

        self.graph.plot_item.plot(data_x, data_y, pen='b', name='Maximum')

        self.populate_list_of_plot()

        self.max_df = pd.DataFrame(list(zip(data_x, data_y)), columns=[
                                   'frequence', 'level'])

    def exportImg(self):
        exporter = exporters.ImageExporter(self.graph.plot_item)

        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                            "Exporter un tracer", "",
                                                            "Jpeg Files (*.jpg);; PNG Files (*.png)")

        exporter.parameters()['width'] = 1440

        exporter.export(fileName)

    def printPDF(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export PDF", None, "PDF files (.pdf);;All Files()"
        )
        if fileName:
            if QtCore.QFileInfo(fileName).suffix() == "":
                fileName += ".pdf"

        self.pdfExporter.export(fileName)

    def change_background_color(self, choice: str):
        if choice == "white":
            self.graph.plot_widget.setBackground(pg.mkColor('#FFF'))
            self.mouse_tracking.hline.setPen({'color': "#000"})
            self.mouse_tracking.vline.setPen({'color': "#000"})
        if choice == "black":
            self.graph.plot_widget.setBackground(pg.mkColor('#000'))
            self.mouse_tracking.hline.setPen({'color': "#FFF"})
            self.mouse_tracking.vline.setPen({'colr': "#FFF"})

    def change_plot_color(self):
        color = QtGui.QColorDialog.getColor()
        for item in self.listPlot.selectedItems():
            self.curves[item.text()].setPen(color)            


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
