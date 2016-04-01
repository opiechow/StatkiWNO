from PyQt4 import QtCore,QtGui, uic
from PyQt4.QtGui import QMainWindow,QApplication, QInputDialog, QWidget, QLabel
from threading import Thread
import sys
import komunikator
import winsound
import mapaGry as mg
import gameState


class LogDialog(QtGui.QDialog):
    def __init__(self):
        super(LogDialog, self).__init__()
        self.setWindowTitle("Dziennik Bitwy")


class HelpDialog(QtGui.QDialog):
    def __init__(self):
        super(HelpDialog, self).__init__()
        self.setWindowTitle("Pomoc")


class MyWin(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('untitled.ui',self)
        self.setWindowTitle("Statki")
        self.mapaWroga = mg.mapaGry(self)
        self.mapaNasza = mg.mapaGry(self)
        #buttons
        self.b_connect.clicked.connect(self.senderInit)
        self.b_listen.clicked.connect(self.listenerInit)
        self.b_lose.clicked.connect(self.instant_lose)
        self.b_log.clicked.connect(self.log_popup)
        self.b_help.clicked.connect(self.help_popup)
        self.b_send.clicked.connect(self.send_message)
        self.b_strzel.clicked.connect(self.temp)
        self.b_ustaw.clicked.connect(self.add_statek)

        self.mapEnemy.addWidget(self.mapaWroga)
        self.mapOur.addWidget(self.mapaNasza)
        self._kom = komunikator.Komunikator()
        self._game_state = gameState.GameState();
        self._komunikat = "q"
        self.refresh_ships()

    def temp(self):
        print self.mapaNasza.selected;

    def add_statek(self):
        self.mapaNasza.statki.append(self.mapaNasza.selected)
        self._game_state.reset_ships()
        for statek in self.mapaNasza.statki:
            try:
                self._game_state.add_ship(len(statek))
            except KeyError:
                print "Not a valid selection!"
                print self.mapaNasza.statki
        self.mapaNasza.deselect_selected()
        self.mapaNasza.selected = []
        self.refresh_ships()
        self.repaint()

    def refresh_ships(self):
        self.l_my_ile_1.setText(str(self._game_state.get_ship(1)))
        self.l_my_ile_2.setText(str(self._game_state.get_ship(2)))
        self.l_my_ile_3.setText(str(self._game_state.get_ship(3)))
        self.l_my_ile_4.setText(str(self._game_state.get_ship(4)))




        pass

    def send_message(self):
        try:
            self._kom.sender_send(self._komunikat)
        except AttributeError:
            print("Sender: not initialized")

    def log_popup(self):
        popup = LogDialog()
        popup.exec_()

    def help_popup(self):
        popup = HelpDialog()
        popup.exec_()

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
        lose = QtGui.QSound("res/loser.wav")
        lose.setLoops(2)
        lose.play()
#        winsound.PlaySound("res/loser.wav",(winsound.SND_ALIAS))
        self.socket_cleanup()
        qApp.exit(0)



if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    mw = MyWin()
    mw.show()
    sys.exit(qApp.exec_())

#http://zetcode.com/gui/pyqt4/drawing