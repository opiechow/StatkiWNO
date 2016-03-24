from PyQt4 import QtCore,QtGui, uic
from PyQt4.QtGui import QMainWindow,QApplication, QInputDialog, QWidget
from komunikacja import *
from threading import Thread
import sys


class OknoGry(QWidget):
    pass

class MyWin(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('untitled.ui',self)
        self.connButton.clicked.connect(self.buttonClick)

    def buttonClick(self):
        print('Klikniety przycisk')
        text, ok = QtGui.QInputDialog.getText(self, 'Wybor celu',
            'Podaj wody na ktore chcesz wyplynac (ip):')

        if ok:
            ip = text
        k = Thread(target=sender, args=(ip,50000))
        k.start()


if __name__ == '__main__':
    s = Thread(target=naslucher, args=('localhost',50000))
    s.start()
    qApp = QApplication(sys.argv)
    mw = MyWin()
    mw.show()
    sys.exit(qApp.exec_())

#http://zetcode.com/gui/pyqt4/drawing