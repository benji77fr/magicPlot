# -*- coding: utf-8 -*-

"""
Created on 2020/04/06

Author: Benjamin Girard

Copyright: SoftBank Robotics 2020
"""

from PyQt5 import QtWidgets, QtCore, QtGui

import pandas as pd
from pathlib import Path

class csvMod():

    def __init__(self, *args, **kwargs):

        super(csvMod, self).__init__(*args, **kwargs)
        self.extChanged = []

    def open_file(self):

        fileName, _ = QtWidgets.QFileDialog.getOpenFileNames(None,
                                                "Ouvrir un fichier", "",
                                                "All Files (*)")

        self.delete_cols_change_ext(fileName)
            
    def delete_cols_change_ext(self, filename):

        colName = ['frequence','level']
        for file in filename:

            p = Path(file)
            fileRename = p.rename(p.with_suffix('.csv'))

            df = pd.read_csv(fileRename, encoding='unicode escape', usecols=[0,1], sep=';', header=None, skiprows=lambda x: x in range(28))
            dfFinal = pd.DataFrame(df.values, columns=colName)
            dfFinal.to_csv(fileRename, sep=";", index=False)