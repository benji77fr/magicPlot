# -*- coding: utf-8 -*-

"""
Created on 2020/04/06

Author: Benjamin Girard

Copyright: SoftBank Robotics 2020
"""

from PyQt5 import QtWidgets, QtCore, QtGui
import qtawesome as qta

import sys
import pandas as pd
import os

import pyqtgraph as pg
from pyqtgraph import exporters

from graph import CustomPlotWidget
from mousetracking import Crosshair
from csvmod import CSVMod
from reportgenerator import Report


class MainWindow(QtGui.QMainWindow):
    '''
    Class MainWindow

    Génération de l'IHM
    '''

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUI()

        self.source_files = []
        self.selected_plot = []
        self.curves = {}
        self.files_path = ""
        self.max_df = pd.DataFrame()

        self.list_plot.itemChanged.connect(self.checked_plot)

    def setupUI(self):
        self.setWindowTitle("Magic Plot for CEM")

        self.graph = CustomPlotWidget()
        self.csv_mod = CSVMod()
        self.mouse_tracking = Crosshair(self.graph.plot_item)

        layout = QtGui.QGridLayout()
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        action_open = QtWidgets.QAction(
            qta.icon('fa.folder-open', color='#ffc47d'), "&Ouvrir", self)
        action_open.setShortcut('Ctrl+O')
        action_open.setStatusTip("Ouvre un ou plusieurs fichiers")
        action_open.triggered.connect(self.open_files)

        action_save_max = QtWidgets.QAction(
            qta.icon('mdi.content-save'), "Sauvegarder Max", self)
        action_save_max.setStatusTip(
            "Sauvegarde le maximum pour chaque point dans un fichier CSV")
        action_save_max.triggered.connect(self.save_max)

        action_plot = QtWidgets.QAction(
            qta.icon('mdi.chart-bell-curve-cumulative'), "&Tracer", self)
        action_plot.setStatusTip("Trace une ou plusieurs courbes")
        action_plot.triggered.connect(self.read_and_plot)

        action_plotMax = QtWidgets.QAction("Tracer Max", self)
        action_plotMax.setStatusTip(
            "Trace la courbe représentant le maximum pour chaque point mesuré")
        action_plotMax.triggered.connect(self.find_max)

        action_add_classeA = QtWidgets.QAction("Classe A à 1m", self)
        action_add_classeA.setStatusTip(
            "Ajoute le gabarit de la classe A à 1m")
        action_add_classeA.triggered.connect(
            lambda: self.graph.add_gabarit('A1'))

        action_add_classeB = QtWidgets.QAction("Classe B à 1m", self)
        action_add_classeB.setStatusTip(
            "Ajoute le gabarit de la classe B à 1m")
        action_add_classeB.triggered.connect(
            lambda: self.graph.add_gabarit('B1'))

        action_add_classeA10 = QtWidgets.QAction("Classe A à 10m", self)
        action_add_classeA10.setStatusTip(
            "Ajoute le gabarit de la classe A à 10m")
        action_add_classeA10.triggered.connect(
            lambda: self.graph.add_gabarit('A10'))

        action_add_classeB10 = QtWidgets.QAction("Classe B à 10m", self)
        action_add_classeB10.setStatusTip(
            "Ajoute le gabarit de la classe B à 10m")
        action_add_classeB10.triggered.connect(
            lambda: self.graph.add_gabarit('B10'))

        action_add_classeBECAVG = QtWidgets.QAction(
            "Classe B EC Moyenne", self)
        action_add_classeBECAVG.setStatusTip(
            "Ajoute le gabarit de la Classe B en EC valeur moyenne")
        action_add_classeBECAVG.triggered.connect(
            lambda: self.graph.add_gabarit('BECAVG'))

        action_add_classeBECQPK = QtWidgets.QAction("Classe B EC QPeak", self)
        action_add_classeBECQPK.setStatusTip(
            "Ajoute le gabarit de la Classe B en EC valeur QPeak")
        action_add_classeBECQPK.triggered.connect(
            lambda: self.graph.add_gabarit('BECQPK'))

        range_ER = QtWidgets.QAction("Mesure ER", self)
        range_ER.setStatusTip(
            "Change l'ordre de grandeur en abscisse pour les mesures en ER")
        range_ER.triggered.connect(lambda: self.graph.change_range('ER'))

        range_EC = QtWidgets.QAction("Mesure EC", self)
        range_EC.setStatusTip(
            "Change l'ordre de grandeur en abscisse pour les mesures en EC")
        range_EC.triggered.connect(lambda: self.graph.change_range('EC'))

        action_remove_CA = QtWidgets.QAction("Enlever Classe A", self)
        action_remove_CA.triggered.connect(
            lambda: self.graph.remove_gabarit('Classe A'))

        action_remove_CB = QtWidgets.QAction("Enlever Classe B", self)
        action_remove_CB.triggered.connect(
            lambda: self.graph.remove_gabarit('Classe B'))

        action_CSV = QtWidgets.QAction(
            qta.icon('fa5s.file-csv', color='#3a9c55'), "Traiter les fichiers", self)
        action_CSV.triggered.connect(self.csv_mod.open_file)

        export_image = QtWidgets.QAction(
            qta.icon('mdi.file-export-outline'), "Exporter image", self)
        export_image.triggered.connect(self.export_image)

        clear_plot = QtWidgets.QAction("Nettoyer la zone de tracer", self)
        clear_plot.triggered.connect(self.plot_clear)

        export_doc = QtWidgets.QAction(
            qta.icon('fa5.file-pdf'), "Exporter résultat en PDF", self)
        export_doc.triggered.connect(self.print_doc)

        clear_selection = QtWidgets.QAction(
            "Nettoyer la liste des tracer", self)
        clear_selection.triggered.connect(self.clear_file_and_plot)

        action_background_white = QtWidgets.QAction("Fond Blanc", self)
        action_background_white.triggered.connect(
            lambda: self.change_background_color('white'))

        action_background_black = QtWidgets.QAction("Fond Noir", self)
        action_background_black.triggered.connect(
            lambda: self.change_background_color('black'))

        change_color = QtWidgets.QAction(qta.icon('mdi.chart-bell-curve-cumulative', 'mdi.format-color-fill', options=[
            {'scale_factor': 1.2}, {'color': 'red'}]), "Changer la couleur d'une courbe", self)
        change_color.triggered.connect(self.change_plot_color)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&Fichier')
        file_menu.addAction(action_open)
        file_menu.addAction(action_save_max)
        file_menu.addAction(action_CSV)
        file_menu.addAction(export_image)
        file_menu.addAction(export_doc)
        plot_menu = menu_bar.addMenu('&Tracer')
        plot_menu.addAction(action_plot)
        plot_menu.addAction(action_plotMax)
        plot_menu.addAction(clear_plot)
        plot_menu.addAction(clear_selection)
        add_gabarit_menu = plot_menu.addMenu('Ajouter gabarit')
        add_gabarit_menu.addAction(action_add_classeA)
        add_gabarit_menu.addAction(action_add_classeA10)
        add_gabarit_menu.addAction(action_add_classeB)
        add_gabarit_menu.addAction(action_add_classeB10)
        add_gabarit_menu.addAction(action_add_classeBECAVG)
        add_gabarit_menu.addAction(action_add_classeBECQPK)
        remove_gabarit_menu = plot_menu.addMenu('Enlever gabarit')
        remove_gabarit_menu.addAction(action_remove_CA)
        remove_gabarit_menu.addAction(action_remove_CB)
        change_range_menu = plot_menu.addMenu("Changer l'abscisse")
        change_range_menu.addAction(range_ER)
        change_range_menu.addAction(range_EC)
        setting_menu = menu_bar.addMenu('&Réglages')
        change_background = setting_menu.addMenu('Changer le Fond')
        change_background.addAction(action_background_white)
        change_background.addAction(action_background_black)

        file_tool_bar = self.addToolBar("Fichier")
        file_tool_bar.addAction(action_CSV)
        file_tool_bar.addAction(action_open)
        file_tool_bar.addAction(export_image)
        file_tool_bar.addSeparator()
        file_tool_bar.addAction(change_color)

        self.label_plot = QtWidgets.QLabel("Liste de courbes")
        font_label = QtGui.QFont()
        font_label.setPointSize(15)
        font_label.setBold(True)
        self.label_plot.setFont(font_label)
        self.label_plot.setAlignment(QtCore.Qt.AlignCenter)

        self.list_plot = QtWidgets.QListWidget()

        layout_left = QtGui.QVBoxLayout()
        layout_left.addWidget(self.label_plot)
        layout_left.addWidget(self.list_plot)

        layout.addLayout(layout_left, 0, 0)
        layout.addWidget(self.graph, 0, 1)
        layout.setColumnStretch(1, 3)

        self.setStatusBar(QtWidgets.QStatusBar(self))

        self.setCentralWidget(widget)

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
                if not self.list_plot.findItems(item.text(), QtCore.Qt.MatchExactly):
                    self.list_plot.addItem(item)
                    self.selected_plot.append(item)
            else:
                continue

    def open_files(self):
        '''
        Ouvre une fenêtre de dialogue pour sélectionner le ou les fichiers
        à ouvrir
        '''
        file_name, _ = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                              "Ouvrir un fichier CSV", "",
                                                              "All Files (*);;CSV Files (*.csv)")

        if file_name:
            for f in file_name:
                if f not in self.source_files:
                    self.source_files.append(f)

        self.read_and_plot(self.source_files)
        self.source_files.clear()

    def checked_plot(self):
        '''
        Fonction appelée lorque l'on coche/décoche un élément de
        list_plot(ListWidget)
        Permet d'afficher ou non les courbes présente dans la liste
        Permet de garder une trace des courbes tracées
        '''
        model = self.list_plot.model()
        for index in range(model.rowCount()):
            item = self.list_plot.item(index)
            if item.checkState() == QtCore.Qt.Checked and item not in self.selected_plot:
                self.selected_plot.append(item)
                self.graph.plot_item.addItem(self.curves[item.text()])
                self.mouse_tracking.update()
            if item.checkState() == QtCore.Qt.Unchecked and item in self.selected_plot:
                self.selected_plot.remove(item)
                self.graph.plot_item.removeItem(self.curves[item.text()])
                self.mouse_tracking.update()

    def read_and_plot(self, source_files):
        '''
        Extrait les données présente dans les fichiers sélectionnés
        et ajoute une courbe dans le PlotItem
        '''
        index_color = 0
        source_files = source_files

        for item in source_files:
            df = pd.read_csv((os.path.dirname(item) +
                              "/" + os.path.basename(item)), sep=";")

            data_x = df['frequence']
            data_y = df['level']

            pencil = pg.mkPen(color=pg.intColor(index_color))
            curve_name = os.path.basename(item).split('.')[0]

            self.graph.plot_item.plot(
                data_x, data_y, pen=pencil, name=curve_name, clickable=True)
            index_color = index_color + 2

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
        self.selected_plot.clear()
        self.list_plot.clear()

    def save_max(self):
        '''
        Sauvegarde dans un fichier CSV les valurs de la courbe générer
        en cherchant le maximum (find_max)
        '''
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                             "Enregistrer un fichier CSV", "",
                                                             "CSV Files (*.csv)")
        self.max_df.to_csv(file_name, index=False, header=True, sep=";")

    def find_max(self):
        '''
        Permet de trouver les valeurs max en fonction d'une fréquence donnée
        en comparant X fichier
        '''
        is_first_file = True
        list_of_dfs = []
        source_files = []

        file_name, _ = QtWidgets.QFileDialog.getOpenfile_names(self,
                                                               "Ouvrir un fichier CSV", "",
                                                               "All Files (*);;CSV Files (*.csv)")

        if file_name:
            for f in file_name:
                source_files.append(f)

        for item in source_files:
            if is_first_file:
                df = pd.read_csv(
                    (os.path.dirname(item) + "/" + os.path.basename(item)), sep=";")
                list_of_dfs.append(df)
                is_first_file = False
            else:
                df = pd.read_csv(
                    (os.path.dirname(item) + "/" + os.path.basename(item)), sep=";", usecols=[1])
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

    def print_doc(self):

        exporter = exporters.ImageExporter(self.graph.plot_item)

        file_image, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                              "Exporter un tracer", "",
                                                              "Jpeg Files (*.jpg);; PNG Files (*.png)")
        exporter.parameters()[
            'width'] = 1600
        exporter.parameters()['antialias'] = True
        exporter.export(file_image)

        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export docx", None, "docx files (.docx);;All Files()"
        )

        text, _ = QtWidgets.QInputDialog.getText(
            self, "Titre du PDF", "Titre", QtWidgets.QLineEdit.Normal, "")
        doc = Report(plot=file_image, data=self.mouse_tracking.dict_values,
                     title=text, file_name=file_name)
        doc.generate_document()

    def export_image(self):
        exporter = exporters.ImageExporter(self.graph.plot_item)

        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                             "Exporter un tracer", "",
                                                             "Jpeg Files (*.jpg);; PNG Files (*.png)")
        if file_name:
            if QtCore.QFileInfo(file_name).suffix() == "":
                file_name += ".jpg"

        exporter.parameters()[
            'width'] = 1600
        exporter.parameters()['antialias'] = True
        exporter.export(file_name)

    def change_background_color(self, choice: str):
        if choice == "white":
            self.graph.plot_widget.setBackground(pg.mkColor('#FFF'))
            self.mouse_tracking.hline.setPen({'color': "#000"})
            self.mouse_tracking.vline.setPen({'color': "#000"})
            self.mouse_tracking.text.setColor("#000")
        if choice == "black":
            self.graph.plot_widget.setBackground(pg.mkColor('#000'))
            self.mouse_tracking.hline.setPen({'color': "#FFF"})
            self.mouse_tracking.vline.setPen({'colr': "#FFF"})
            self.mouse_tracking.text.setColor("#FFF")

    def change_plot_color(self):
        color = QtGui.QColorDialog.getColor()
        for item in self.list_plot.selectedItems():
            self.curves[item.text()].setPen(color)
