# -*- coding: utf-8 -*-

"""
Created on 2020/04/06

Author: Benjamin Girard

Copyright: SoftBank Robotics 2020
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtCore, QtGui

import os
import sys
from pathlib import Path

class csvMod():

    def __init__(self, *args, **kwargs):

        super(csvMod, self).__init__(*args, **kwargs)
        self.extChanged = []

    def open_file(self):

        fileName, _ = QtWidgets.QFileDialog.getOpenFileNames(None,
                                                "Ouvrir un fichier", "",
                                                "All Files (*)")

        self.change_extension(fileName)

    def change_extension(self, filename):
        
        if filename:
            for f in filename:
                p = Path(f)
                p.rename(p.with_suffix('.csv'))