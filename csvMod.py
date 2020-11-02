# -*- coding: utf-8 -*-

"""
Created on 2020/04/06

Author: Benjamin Girard

Copyright: SoftBank Robotics 2020
"""

from PyQt5 import QtWidgets, QtCore, QtGui

import csv
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

        startline, endline = 0, 28
        for file in filename:

            p = Path(file)
            fileRename = p.rename(p.with_suffix('.csv'))

            with open(fileRename, 'r', newline='', encoding='latin1') as f:
                content = [row for i,row in enumerate(csv.reader(f), 1)
                            if i not in range(startline, endline + 1)]

            with open(fileRename, 'w', newline='') as f:
                csv.writer(f).writerow(['frequence ; level'])
                csv.writer(f).writerows(content)