# -*- coding: utf-8 -*-

"""
Created on 2020/04/06

Author: Benjamin Girard

Copyright: SoftBank Robotics 2020
"""

from PyQt5 import QtWidgets

import pandas as pd
import zipfile
import os
from pathlib import Path


class CSVMod():

    def __init__(self):

        super(CSVMod, self).__init__()
        self.file_changed = []

    def open_file(self):

        file_name, _ = QtWidgets.QFileDialog.getOpenFileNames(None,
                                                             "Ouvrir le/les fichiers à traiter", "",
                                                             "All Files (*)")
        self.file_changed = file_name.copy()
        self.zip_original(file_name)
        self.delete_cols_change_ext(self.file_changed)

    def zip_original(self, original):

        with zipfile.ZipFile(os.path.dirname(original[0]) + "/" + "Originaux.zip", "w") as zipMe:
            for file in original:
                zipMe.write(file, os.path.basename(file),
                            compress_type=zipfile.ZIP_DEFLATED)

    def delete_cols_change_ext(self, file_name):

        col_name = ['frequence', 'level']
        for file in file_name:

            p = Path(file)
            file_rename = p.rename(p.with_suffix('.csv'))

            df = pd.read_csv(file_rename, encoding='unicode escape', usecols=[
                             0, 1], sep=';', header=None, skiprows=lambda x: x in range(28))
            df_final = pd.DataFrame(df.values, columns=col_name)
            df_final.to_csv(file_rename, sep=";", index=False)
