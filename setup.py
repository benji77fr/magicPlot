from setuptools import setup
import os
import MagicPlot

setup(
    name = 'MagicPlot',
    version = MagicPlot.__version__,
    packages = ['MagicPlot'],
    author = "Benjamin Girard",
    author_email = "bgirard@softbankrobotics.com",
    description = "Outil de traitement de données pour la CEM",
    install_requires = ['PyQT5', 'pyqtgraph==0.11.0', 'numpy', 'pandas'],
    include_package_data = True,
    url = 'https://gitlab.aldebaran.lan/int-mecatro/magicplot/-/tree/beta',
    entry_points = {
        'console_scripts': [
            'magicplot = MagicPlot.magicplot:main',
        ],
    }
)