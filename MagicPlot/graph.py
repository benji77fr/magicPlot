# -*- coding: utf-8 -*-

"""
Created on 2020/04/06

Author: Benjamin Girard

Copyright: SoftBank Robotics 2020
"""

import pyqtgraph as pg
from PyQt5 import QtCore, QtGui

CLASSE_A_B_X = [30000000,230000000, 230000000,1000000000]
CLASSE_A_Y = [60,60,67,67]
CLASSE_B_Y = [50,50,57,57]
CLASSE_A_Y_10M = [40,40,47,47]
CLASSE_B_Y_10M = [30,30,37,37]

CLASSE_B_X_EC = [150000, 500000, 5000000, 5000000, 30000000]
CLASSE_B_Y_EC_AVG = [56, 46, 46, 50, 50]
CLASSE_B_Y_EC_QPK = [66, 56, 56, 60, 60]

class CustomPlotWidget(QtGui.QWidget):
    '''
    Class CustomPlotWidget

    Création d'un objet de type PlotWidget
    Cet objet nous permet d'avoir une fenêtre de graphique custom
    prête à l'emploi.

    :param
        title: Titre du Graph (pas encore implémenter pour le moment)
    '''
    def __init__(self, title=None):
        super(CustomPlotWidget, self).__init__()

        self.plot_widget = pg.PlotWidget()
        self.plot_item = self.plot_widget.getPlotItem()
        self.plot_vb = pg.ViewBox()
        self.title = title
        self.gabarit = {}

        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.plot_widget, 0, 0, 2, 1)
        self.plot_widget.setBackground("w")
        self.plot_item.scene().addItem(self.plot_vb)
        self.plot_item.setLogMode(True,False)
        self.plot_item.showGrid(True,True)
        self.plot_item.getAxis('left').setLabel('Niveau [dBµV]')
        self.plot_item.getAxis('bottom').setLabel('Fréquence [HZ]')
        self.plot_item.setRange(xRange=(7.4,9.1), yRange=(25,65), padding=0)
        self.plot_widget.addLegend()
        self.setCursor(QtCore.Qt.BlankCursor)


    def add_gabarit(self, classe):
        if classe == 'A1':
            name = 'Classe A'
            self.gabarit[name] = self.plot_item.plot(x=CLASSE_A_B_X, y=CLASSE_A_Y, pen=pg.mkPen('b', width=3), name=name)
        if classe == 'B1':        
            name = 'Classe B'
            self.gabarit[name] = self.plot_item.plot(x=CLASSE_A_B_X, y=CLASSE_B_Y, pen=pg.mkPen('r', width=3), name=name)
        if classe == 'A10':
            name = 'Classe A'
            self.gabarit[name] = self.plot_item.plot(x=CLASSE_A_B_X, y=CLASSE_A_Y_10M, pen=pg.mkPen('b', width=3), name=name)
        if classe == 'B10':        
            name = 'Classe B'
            self.gabarit[name] = self.plot_item.plot(x=CLASSE_A_B_X, y=CLASSE_B_Y_10M, pen=pg.mkPen('r', width=3), name=name)
        if classe == 'BECAVG':
            name = 'Classe B Average'
            self.gabarit[name] = self.plot_item.plot(x=CLASSE_B_X_EC, y=CLASSE_B_Y_EC_AVG, pen=pg.mkPen('r', width=3), name=name)
        if classe == 'BECQPK':
            name = 'Classe B QPeak'
            self.gabarit[name] = self.plot_item.plot(x=CLASSE_B_X_EC, y=CLASSE_B_Y_EC_QPK, pen=pg.mkPen('b', width=3), name=name)
 
    def remove_gabarit(self, classe):
        if classe == 'Classe A':
            self.plot_item.removeItem(self.gabarit['Classe A'])
        if classe == 'Classe B':
            self.plot_item.removeItem(self.gabarit['Classe B'])
        if classe == 'BECAVG':
            self.plot_item.removeItem(self.gabarit['Classe B Average'])
        if classe == 'BECQPK':
            self.plot_item.removeItem(self.gabarit['Classe B QPeak'])
    
    def change_range(self, range):
        if range == 'EC':
            self.plot_item.setRange(xRange=(5,7.5), yRange=(10,90), padding=0)
        if range == 'ER':
            self.plot_item.setRange(xRange=(7.4,9.1), yRange=(10,90), padding=0)
