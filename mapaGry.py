from PyQt4 import QtCore,QtGui
from PyQt4.QtGui import QLabel
import math

class mapaGry(QtGui.QWidget):
    def __init__(self, parent):
        super(mapaGry, self).__init__()
        self._hexy = {}
        self._hex_size = 17
        self.selected = []
        self.gen_hexy(10,10)
        self.statki = []
        self.parent = parent

    def mousePressEvent(self, QMouseEvent):
        p = QtGui.QCursor.pos()
        p = self.mapFromGlobal(p)
#        print str.format('Clicked: x:{}',p.x())
#        print str.format('Clicked: y:{}',p.y())
        for key in self._hexy:
            if abs(self._hexy[key]["x"] - p.x()) < self._hex_size and abs(self._hexy[key]["y"] - p.y()) < self._hex_size:
                self._hexy[key]["sel"] = not self._hexy[key]["sel"]
                if self._hexy[key]["sel"]:
                    self.selected.append(key);
                else:
                    self.selected.remove(key)
                self.parent.l_wsp_x.setText(str.format("X:{}",key[0]+1))
                self.parent.l_wsp_y.setText(str.format("Y:{}", key[1]+1))
                break
        self.repaint()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        for k in self._hexy:
            self.drawHex(qp, self._hexy[k])
        self.paint_statki(qp)
        qp.end()

    def gen_hexy(self, cols, rows):
        x_off = self._hex_size
        y_off = self._hex_size
        height = self._hex_size*2;
        width = math.sqrt(3)/2 * height
        for c in range(cols):
            for r in range(rows):
                self._hexy[(c,r)] = ({'x': x_off + (c+1)*width-(r%2)*width/2,
                                'y': y_off + 1/2*height+(r+1)*(height*3/4),
                                'sel': False})

    def drawHex(self, qp, hex):
        if hex['sel'] == True:
            qp.setPen(QtCore.Qt.red)
        else:
            qp.setPen(QtCore.Qt.black)
        size = self.size()
        for i in range(6):
            curHex = self.hex_corner(hex['x'],hex['y'],self._hex_size,i)
            nextHex = self.hex_corner(hex['x'],hex['y'],self._hex_size,i+1%6)
            qp.drawLine(curHex[0],curHex[1],nextHex[0],nextHex[1])

    def paint_statki(self, qp):
        for statek in self.statki:
            for klucz in statek:
                x = self._hexy[klucz]["x"]
                y = self._hexy[klucz]["y"]
                qp.drawEllipse(x,y,5,5)

    def deselect_selected(self):
        for statek in self.statki:
            for klucz in statek:
                self._hexy[klucz]["sel"] = False


    def hex_corner(self, x, y, size, i):
        angle_deg = 60 * i + 30
        angle_rad = math.pi / 180 * angle_deg
        return [x + size * math.cos(angle_rad),y + size * math.sin(angle_rad)]
