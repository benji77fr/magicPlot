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
    install_requires = ['PyQT5==5.15.4', 
                        'pyqt5-tools==5.15.2.3',
                        'pyqt5-plugins==5.15.2.2.1.0', 
                        'pyqtgraph==0.12.1',
                        'qtawesome==1.0.2', 
                        'pandas==1.2.3', 
                        'jinja2==2.11.3',
                        'weasyprint==52.4'
    ],
    include_package_data = True,
    url = 'https://gitlab.aldebaran.lan/bgirard1/magicPlot',
    entry_points = {
        'console_scripts': [
            'magicplot = MagicPlot.main:main',
        ],
    }
)