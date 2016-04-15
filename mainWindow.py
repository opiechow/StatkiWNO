from threading import Thread

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QMainWindow, QApplication, QInputDialog, QWidget, QLabel
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
        QMainWindow.__init__(self)
        self._logger = StateLogger()
        self._game_state = GameState(self._logger, self.hit_sound)
        self._kom = Komunikator(self._game_state)
        self._rx_thread = None

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
        self.b_connect.clicked.connect(self.client_init)
        self.b_listen.clicked.connect(self.server_init)
        self.b_lose.clicked.connect(self.instant_lose)
        self.b_save_log.clicked.connect(self.log_popup)
        self.b_load_log.clicked.connect(self.help_popup)
        self.b_send.clicked.connect(self.send_message)
        self.b_strzel.clicked.connect(self.shoot)
        self.b_ustaw.clicked.connect(self.add_statek)
        self.b_next.clicked.connect(self.get_next_state)
        self.b_prev.clicked.connect(self.get_prev_state)

        #sounds
        self.s_splash  = QtGui.QSound("res/splash.wav")
        self.s_explode = QtGui.QSound("res/bombexpl.wav")
        self.s_lose    = QtGui.QSound("res/loser.wav")

        self.startTimer(1000)
        self.state_view_update()

    def get_prev_state(self):
        self._game_state.set_logged_state(self._logger.get_prev_state())

    def get_next_state(self):
        self._game_state.set_logged_state(self._logger.get_next_state())

    def timerEvent(self, *args, **kwargs):
        if self._game_state.get_state_change():
            self.state_view_update()
            self.repaint()

    def onParseEvent(self, event):
        print event

    def shoot(self):
        sel_list = self.mapaWroga.get_selection()
        if sel_list:
            self.mapaWroga.clear_selection()
            sel = sel_list[0]
            self.repaint()
            self._kom.send_shoot(sel)
        else:
            print "Brak zaznaczenia!"

    def add_statek(self):
        assert self._game_state.get_turn_no() == 0
        try:
            self.mapaNasza.add_new_ship()
        except AssertionError:
            print "Shipyard: Not enough parts for that kind of ship"
        self.repaint()

    def state_view_update(self):
        if self._game_state.get_turn_no() == 0:
            self.l_turn_indicator.setText("Rozmieszczanie statkow")
        else:
            if self._game_state.is_my_turn():
                self.l_turn_indicator.setText("Nasza kolej")
            else:
                self.l_turn_indicator.setText("Ich kolej")

        self.l_turn_no.setText(" ".join(["Numer tury:",
                                         str(self._game_state.get_turn_no())]))
        self.l_my_ile_1.setText(str(self._game_state.get_ship_count(1)))
        self.l_my_ile_2.setText(str(self._game_state.get_ship_count(2)))
        self.l_my_ile_3.setText(str(self._game_state.get_ship_count(3)))
        self.l_my_ile_4.setText(str(self._game_state.get_ship_count(4)))
        self.l_oni_ile_1.setText(str(self._game_state.get_enemy_ship_count(1)))
        self.l_oni_ile_2.setText(str(self._game_state.get_enemy_ship_count(2)))
        self.l_oni_ile_3.setText(str(self._game_state.get_enemy_ship_count(3)))
        self.l_oni_ile_4.setText(str(self._game_state.get_enemy_ship_count(4)))

    def refresh_selection(self, selection):
        try:
            x, y = selection;
            self.l_wsp_x.setText(str.format("X:{}", x))
            self.l_wsp_y.setText(str.format("Y:{}", y))
            self.repaint()
        except TypeError:
            print "No new selections allowed."

    def send_message(self):
        try:
            self._kom.send(self._komunikat)
        except AttributeError:
            print("Sender: not initialized")

    def log_popup(self):
        logFile = QtGui.QFileDialog.getOpenFileName()
        self._logger.save_logger(logFile)

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
        self._rx_thread = Thread()
        self._kom.cleanup()
        event.accept()

    def client_init(self):
        self.setWindowTitle("Statki - Klient")
        if 1: #self._game_state.ready_for_battle():
            # text, ok = QtGui.QInputDialog.getText(self, 'Wybor celu',
            #                                       'Podaj wody na ktore '
            #                                       'chcesz wyplynac (ip):')
            if 1: #ok:
                text = "localhost"

                self._rx_thread = Thread(target=self._kom.client_init, args=(text,))
                self._rx_thread.start()
        else:
            print "Generals: We're not ready to fight yet, commander!"

    def server_init(self):
        self.setWindowTitle("Statki - Serwer")
        if 1: #self._game_state.ready_for_battle():
            self._rx_thread = Thread(target=self._kom.server_init, args=())
            self._rx_thread.start()
        else:
            print "Generals: We're not ready to fight yet, commander!"



    def instant_lose(self):
        self.s_lose.play()
        sleep(6)
        #        winsound.PlaySound("res/loser.wav",(winsound.SND_ALIAS))
        self.socket_cleanup()
        qApp.exit(0)

    def hit_sound(self,hit):
        if hit:
            self.s_explode.play()
        else:
            self.s_splash.play()

if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    mw = MyWin()
    mw.show()
    sys.exit(qApp.exec_())

    # http://zetcode.com/gui/pyqt4/drawing
