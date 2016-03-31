from PyQt4 import QtCore,QtGui, uic
from PyQt4.QtGui import QMainWindow,QApplication, QInputDialog, QWidget
from threading import Thread
import sys
import komunikator
import winsound
import mapaGry as mg

class MyWin(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('untitled.ui',self)
        self.mapaWroga = mg.mapaGry(self)
        self.mapaNasza = mg.mapaGry(self)
        self.b_connect.clicked.connect(self.senderInit)
        self.b_listen.clicked.connect(self.listenerInit)
        self.b_lose.clicked.connect(self.instant_lose)
        self.mapEnemy.addWidget(self.mapaWroga)
        self.mapOur.addWidget(self.mapaNasza)
        self._kom = komunikator.Komunikator()

    def socket_cleanup(self):
        try:
            self._kom.sender_send("q")
            self._kom.sender_terminate()
        except AttributeError:
            print("Sender: not initialized")

    def closeEvent(self, event):
        self.socket_cleanup()
        event.accept()

    def senderInit(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Wybor celu',
            'Podaj wody na ktore chcesz wyplynac (ip:port):')

        if ok:
            ip, port = str(text).split(':')
        self.k = Thread(target=self._kom.sender_init, args=(ip,int(port)))
        self.k.start()

    def listenerInit(self):
        port, ok = QtGui.QInputDialog.getText(self, 'Terytorium',
                                              'Podaj port:')
        if ok:
            port = int(port)
        self.s = Thread(target=self._kom.recv_init, args=('localhost',port))
        self.s.start()

    def instant_lose(self):
        winsound.PlaySound("./res/loser.wav",(winsound.SND_ALIAS))
        self.socket_cleanup()
        qApp.exit(0)



if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    mw = MyWin()
    mw.show()
    sys.exit(qApp.exec_())

#http://zetcode.com/gui/pyqt4/drawing