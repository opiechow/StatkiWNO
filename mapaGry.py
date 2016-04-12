from PyQt4 import QtCore,QtGui
from PyQt4.QtGui import QMouseEvent
from hex import Hex
from gameState import GameState

class mapaGry(QtGui.QWidget):
    def __init__(self, gameState, ourMap, update_ui):
        super(mapaGry, self).__init__()
        self._ourMap = ourMap
        self._selection = []
        self._hexy = {}
        for c in range(10):
            for r in range(10):
                self._hexy[c,r] = Hex(c,r)
        self._gameState = gameState
        self._lastSel = (10,10)
        self._update_ui = update_ui;

    def is_selection_adjacent(self, sel):
        allowed = False
        for key in self._selection:
            n = self._hexy[key].get_neighbours()
            if sel in n:
                allowed = True
        if not allowed:
            raise Exception

    def is_adjacent_to_ship(self, sel):
        adjacent = False
        for ship in self._gameState.get_my_ships():
            for pole in ship.get_pola():
                if sel in self._hexy[pole.get_key()].get_neighbours():
                    adjacent = True
                    ship.shout()
        return adjacent

    def _map_mouse_cords_to_hex(self, p):
        sel = None
        for key in self._hexy:
            if self._hexy[key].in_hex(p.x(), p.y()):
                sel = key
        return sel

    def _validate_our_selection(self, sel):
        if self.is_adjacent_to_ship(sel):
            raise Exception
        if self._selection:
            self.is_selection_adjacent(sel)

    def _handle_left_click(self,p):
        if self._ourMap:
            maxLen = 4
        else:
            maxLen = 1
        sel = self._map_mouse_cords_to_hex(p)
        try:
            self._validate_our_selection(sel)
            if sel not in self._selection:
                if len(self._selection) < maxLen:
                    self._selection.append(sel)
                    self._lastSel = sel
                else:
                    print str.format('Selector: Max {} selected ', maxLen)
            else:
                self._selection.remove(sel)
                self._lastSel = sel
        except:
            print ('Selector: not a valid selection')

        self._update_ui(self._lastSel);
        self.repaint()

    def mousePressEvent(self, MouseEvent):
        p = QtGui.QCursor.pos()
        p = self.mapFromGlobal(p)
        if MouseEvent.button() == 1:
            self._handle_left_click(p)
        elif MouseEvent.button() == 2:
            self._handle_right_click(p)


    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        for k in self._hexy:
            if not k in self._selection:
                self.draw_hex(qp, self._hexy[k])
        for k in self._selection:
            self.draw_hex(qp, self._hexy[k])
        self.paint_statki(qp)
        qp.end()

    def draw_hex(self, qp, hexik):
        if hexik.get_key() in self._selection:
            qp.setPen(QtCore.Qt.red)
        else:
            qp.setPen(QtCore.Qt.black)
        p = hexik.r_get_corners()
        for i in range(len(p)-1):
            qp.drawLine(p[i]["x"],p[i]["y"],p[i+1]["x"],p[i+1]["y"])
        qp.drawLine(p[len(p)-1]["x"],p[len(p)-1]["y"],p[0]["x"],p[0]["y"])

    def paint_statki(self, qp):
        if self._ourMap:
            lista_statkow =  self._gameState.get_my_ships()
        else:
            lista_statkow = self._gameState.get_enemy_ships()
        for statek in lista_statkow:
            for pole in statek.get_pola():
                key = pole.get_key()
                x,y = self._hexy[key].r_get_center()
                if key in self._selection:
                    qp.setPen(QtCore.Qt.red)
                else:
                    qp.setPen(QtCore.Qt.black)
                if pole.is_shot():
                    qp.drawLine(x-5,y-5,x+5,y+5)
                    qp.drawLine(x)
                else:
                    qp.drawEllipse(x-5,y-5,10,10)

    def get_selection(self):
        return self._selection

    def clear_selection(self):
        self._selection = []

    def add_new_ship(self):
        assert self._ourMap == True
        if self._selection:
            self._gameState.add_my_ship(self._selection)
            self.clear_selection()
        else:
            print "Shipyard: we don't know where to deploy ship"


