import sys
import pandas as pd
import time

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from MainWindow import Ui_MainWindow
from graph import Ui_Form

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


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.actionOpen.triggered.connect(lambda: self.open_file())
        self.actionExit.triggered.connect(lambda: self.exit_app())
        self.actionPlot.triggered.connect(lambda: self.open_graph())

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
                data = freq, lvl

                if i == 0:
                    self.model = CustomTableModel(data)
                    self.tableView.setModel(self.model)
                    displayTableView(self.tableView)
                elif i == 1:
                    self.model = CustomTableModel(data)
                    self.tableView2.setModel(self.model)
                    displayTableView(self.tableView2)
                elif i == 2:
                    self.model = CustomTableModel(data)
                    self.tableView3.setModel(self.model)
                    display_table_view(self.tableView3)
                
                i = i + 1

    def open_graph(self):

        self.graphWindow = Graph()
        self.graphWindow.show()
        self.graphWindow.exec_()
    
        
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

