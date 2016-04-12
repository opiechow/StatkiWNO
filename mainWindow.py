from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QMainWindow, QApplication, QInputDialog, QWidget, QLabel
from threading import Thread
import sys
from time import sleep

import winsound
from mapaGry import mapaGry
from gameState import GameState
from stateLogger import StateLogger
from komunikator import Komunikator


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
        self._logger = StateLogger()
        self._game_state = GameState(self._logger, self.state_view_update)
        self._kom = Komunikator()

        QMainWindow.__init__(self)
        uic.loadUi('untitled.ui', self)
        self.setWindowTitle("Statki")

        self.mapaWroga = mapaGry(self._game_state,
                                 False,
                                 self.refresh_selection)
        self.mapaNasza = mapaGry(self._game_state,
                                 True,
                                 self.refresh_selection)
        self.mapEnemy.addWidget(self.mapaWroga)
        self.mapOur.addWidget(self.mapaNasza)

        # Associate buttons
        self.b_connect.clicked.connect(self.senderInit)
        self.b_listen.clicked.connect(self.listenerInit)
        self.b_lose.clicked.connect(self.instant_lose)
        self.b_log.clicked.connect(self.log_popup)
        self.b_help.clicked.connect(self.help_popup)
        self.b_send.clicked.connect(self.send_message)
        self.b_strzel.clicked.connect(self.shoot)
        self.b_ustaw.clicked.connect(self.add_statek)

        self.state_view_update()

    def shoot(self):
        print self.mapaNasza.get_selection();

    def add_statek(self):
        try:
            self.mapaNasza.add_new_ship()
        except AssertionError:
            print "Shipyard: Not enough parts for that kind of ship"
        self.repaint()

    def state_view_update(self):
        self.l_my_ile_1.setText(str(self._game_state.get_ship_count(1)))
        self.l_my_ile_2.setText(str(self._game_state.get_ship_count(2)))
        self.l_my_ile_3.setText(str(self._game_state.get_ship_count(3)))
        self.l_my_ile_4.setText(str(self._game_state.get_ship_count(4)))

    def refresh_selection(self, selection):
        try:
            x, y = selection;
            self.l_wsp_x.setText(str.format("X:{}", x))
            self.l_wsp_y.setText(str.format("Y:{}", y))
        except TypeError:
            print "No new selections allowed."

    def send_message(self):
        try:
            self._kom.send(self._komunikat)
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
            self._kom.send("q")
            self._kom.sender_terminate()
        except AttributeError:
            print("Sender: not initialized")

    def closeEvent(self, event):
        self.socket_cleanup()
        event.accept()

    def senderInit(self):
        if self._game_state.ready_for_battle():
            text, ok = QtGui.QInputDialog.getText(self, 'Wybor celu',
                                                  'Podaj wody na ktore '
                                                  'chcesz wyplynac (ip:port):')
            if ok:
                ip, port = str(text).split(':')
            self.k = Thread(target=self._kom.sender_init, args=(ip, int(port)))
            self.k.start()
        else:
            print "Generals: We're not ready to fight yet, commander!"

    def listenerInit(self):
        if self._game_state.ready_for_battle():
            self.s = Thread(target=self._kom.recv_init, args=('localhost', port))
            self.s.start()
        else:
            print "Generals: We're not ready to fight yet, commander!"



    def instant_lose(self):
        lose = QtGui.QSound("res/loser.wav")
        lose.play()
        sleep(6)
        #        winsound.PlaySound("res/loser.wav",(winsound.SND_ALIAS))
        self.socket_cleanup()
        qApp.exit(0)


if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    mw = MyWin()
    mw.show()
    sys.exit(qApp.exec_())

    # http://zetcode.com/gui/pyqt4/drawing
