import magicplot
from PyQt5 import QtWidgets
import sys


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = magicplot.MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
