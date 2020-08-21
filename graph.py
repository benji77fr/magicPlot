# -*- coding: utf-8 -*-

import pyqtgraph as pg
from pyqtgraph import GraphicsWidget
from PyQt5 import QtCore, QtWidgets, QtGui


CLASSE_A_B_X = [30000000,230000000, 230000000,1000000000]
CLASSE_A_Y = [60,60,67,67]
CLASSE_B_Y = [50,50,57,57]

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

        #layout.addWidget(self.title, 1, 1, 1, 2)
        layout.addWidget(self.plot_widget, 0, 0, 2, 1)
        self.plot_item.scene().addItem(self.plot_vb)
        self.plot_item.setLogMode(True,False)
        self.plot_item.showGrid(True,True)
        self.plot_item.getAxis('left').setLabel('Niveau [dBµV]')
        self.plot_item.getAxis('bottom').setLabel('Fréquence [HZ]')
        # self.plot_item.getAxis('bottom').linkToView(self.plot_vb)
        # self.plot_item.getAxis('left').linkToView(self.plot_vb)
        self.plot_item.setRange(xRange=(7.4,9.1), yRange=(10,90), padding=0)
        self.plot_vb.setLimits(xMin=30000000, xMax=1000000000)
        self.plot_vb.enableAutoRange(enable=True)
        self.plot_widget.addLegend()
        self.setCursor(QtCore.Qt.BlankCursor)

    def add_gabarit(self, classe):
        if classe == 'A':
            name = 'Classe A'
            self.gabarit[name] = self.plot_item.plot(x=CLASSE_A_B_X, y=CLASSE_A_Y, pen=pg.mkPen('b', width=3), name=name)
        if classe == 'B':
            name = 'Classe B'
            self.gabarit[name] = self.plot_item.plot(x=CLASSE_A_B_X, y=CLASSE_B_Y, pen=pg.mkPen('r', width=3), name=name)
 
    def remove_gabarit(self, classe):
        if classe == 'Classe A':
            self.plot_item.removeItem(self.gabarit['Classe A'])
        if classe == 'Classe B':
            self.plot_item.removeItem(self.gabarit['Classe B'])
