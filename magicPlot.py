import sys
import pandas as pd
import time
import os
import numpy

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pyqtgraph as pg

from MainWindow import Ui_MainWindow
from graph import Ui_Form
from csvMod import csvMod

class CustomTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.load_data(data)

    def load_data(self, data):
        self.input_freq = data[0].values
        self.input_level = data[1].values

        self.column_count = 2
        self.row_count = len(self.input_freq)

    def rowCount(self, parent=QModelIndex()):
        return self.row_count
    
    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("Frequence","Niveau")[section]
        else:
            return "{}".format(section)
    
    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if column == 0:
                return "{}".format(self.input_freq[row])
            elif column == 1:
                return "{:.2f}".format(self.input_level[row])
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight
        
        return None

class Graph(QMainWindow, Ui_Form):

    def __init__(self, *args, **kwargs):
        super(Graph, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.graphicsView.setBackground('w')


                

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.csvmod = csvMod()

        self.actionOpen.triggered.connect(lambda: self.open_file())
        self.actionExit.triggered.connect(lambda: self.exit_app())
        self.actionPlot.triggered.connect(lambda: self.open_graph())
        self.actionClose_tab.triggered.connect(lambda: self.clean_tab())
        self.actionPlot_max.triggered.connect(lambda: self.find_max())
        self.actionCSV_Modification.triggered.connect(lambda: self.csv_modification())

    def find_max(self):

        self.graphWindow = Graph()

        isFirstFile = True
        list_of_dfs = []

        fileName, _ = QFileDialog.getOpenFileNames(self,
                                                  "Ouvrir un fichier CSV", "",
                                                  "All Files (*);;CSV Files (*.csv)")


        if fileName:
            for f in fileName:
                if isFirstFile == True:
                    df = pd.read_csv(f, sep=";")
                    list_of_dfs.append(df)
                    isFirstFile = False
                elif isFirstFile == False:
                    df = pd.read_csv(f, sep=";", usecols=[1])
                    list_of_dfs.append(df)
           
        combine_df = pd.concat(list_of_dfs, axis=1)
        print(combine_df)

        temp_df = combine_df.loc[:, 'level']
        maxLevel_df = pd.DataFrame({'level': temp_df.max(axis=1)})

        data_x = combine_df["frequence"]
        data_y = maxLevel_df["level"]

        self.plot(data_x, data_y, 'b')
        self.graphWindow.show()

    def open_file(self):

        i = 0

        fileName, _ = QFileDialog.getOpenFileNames(self,
                                                  "Ouvrir un fichier CSV", "",
                                                  "All Files (*);;CSV Files (*.csv)")
       
        if fileName:

            for f in fileName:

                df = pd.read_csv(f, sep=";")

                freq = df["frequence"]
                lvl = df["level"]
                fname = fileName
                data = freq, lvl

                if i == 0:
                    self.tableView.setEnabled(True)
                    self.model = CustomTableModel(data)
                    self.tableView.setModel(self.model)
                    self.tabWidget.setTabText(i,os.path.basename(fname[i]))
                    display_table_view(self.tableView)
                elif i == 1:
                    self.tableView2.setEnabled(True)
                    self.model = CustomTableModel(data)
                    self.tableView2.setModel(self.model)
                    self.tabWidget.setTabText(i,os.path.basename(fname[i]))
                    display_table_view(self.tableView2)
                elif i == 2:
                    self.tableView3.setEnabled(True)
                    self.model = CustomTableModel(data)
                    self.tableView3.setModel(self.model)
                    self.tabWidget.setTabText(i,os.path.basename(fname[i]))
                    display_table_view(self.tableView3)
                
                i = i + 1

    def open_graph(self):

        data_x = []
        data_y = []

        self.graphWindow = Graph()

        if self.tableView.isEnabled():
            
            for i in  range(self.tableView.model().rowCount()):
                x = float(self.tableView.model().index(i, 0).data())
                y = float(self.tableView.model().index(i, 1).data())

                if x > 0 and y > 0:
                    data_x.append(x)
                    data_y.append(y)
            
            self.plot(data_x, data_y, 'r')

            data_y.clear()
            data_x.clear()

        if self.tableView2.isEnabled():
            
            for i in  range(self.tableView2.model().rowCount()):
                x = float(self.tableView2.model().index(i, 0).data())
                y = float(self.tableView2.model().index(i, 1).data())

                if x > 0 and y > 0:
                    data_x.append(x)
                    data_y.append(y)

            self.plot(data_x, data_y, 'b')

            data_y.clear()
            data_x.clear()
        
        if self.tableView3.isEnabled():
            
            for i in  range(self.tableView3.model().rowCount()):
                x = float(self.tableView3.model().index(i, 0).data())
                y = float(self.tableView3.model().index(i, 1).data())

                if x > 0 and y > 0:
                    data_x.append(x)
                    data_y.append(y)

            self.plot(data_x, data_y, 'g')

            data_y.clear()
            data_x.clear()
        
        self.graphWindow.show()
    
    def plot(self, x, y, color):
        pen = pg.mkPen(color=color)
        self.graphWindow.graphicsView.plotItem.plot(x, y,pen=pen)

    def clean_tab(self):

        self.model.beginResetModel()
        self.model.endResetModel()

    def csv_modification(self):

        fileName, _ = QFileDialog.getOpenFileNames(self,
                                                  "Ouvrir un fichier CSV", "",
                                                  "All Files (*)")
        
        print(fileName)

        extFileChanged = self.csvmod.change_extension(fileName)

        print(extFileChanged)

        
    @pyqtSlot()
    def exit_app(self):
        sys.exit()

def display_table_view(tableView):

    resize = QHeaderView.ResizeToContents
    horizontal_header = tableView.horizontalHeader()
    vertical_header = tableView.verticalHeader()
    horizontal_header.setSectionResizeMode(resize)
    vertical_header.setSectionResizeMode(resize)
    horizontal_header.setStretchLastSection(True)

    tableView.resizeColumnsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show() 

    sys.exit(app.exec_()) 

