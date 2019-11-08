import sys
import pandas as pd

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from MainWindow import Ui_MainWindow


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
        colunn = index.colunn()
        row = index.row()

        if role == Qt.DisplayRole:
            if column == 0:
                return "{:.2f}".format(self.input_freq[row])
            elif colunn == 1:
                return "{:.2f}".format(self.input_level[row])
        elif role == QtBackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight
        
        return None


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.data = self.actionOpen.triggered.connect(lambda: self.openFile())

        self.model = CustomTableModel(self.data)

        self.tableView.setModel(self.model)

        resize = QHeaderView.ResizeToContents
        self.horizontal_header = self.tableView.horizontalHeader()
        self.vertical_header = self.tableView.verticalHeader()
        self.horizontal_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.vertical_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontal_header.setStretchLastSection(True)

        self.mainLayout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        size.setHorizontalStretch(1)
        self.tableView.setSizePolicy(size)
        self.mainLayout.addWidget(self.tableView)
        self.setLayout(self.mainLayout)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Ouvrir un fichier CSV", "",
                                                  "All Files (*);;CSV Files (*.csv)")
        if fileName:
            df = pd.read_csv(fileName, sep=";")

        freq = df["frequence"]
        lvl = df["level"]

        return freq, lvl

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show() 

    sys.exit(app.exec_()) 

