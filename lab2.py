import socket
from threading import Thread
import Tkinter as tk
from plansza import HexGrid


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit',
            command=self.quit)
        self.quitButton.grid()


def parse_data(data):
    wsp = {};
    lista = data.split(" ")
    if len(lista) > 3 and lista[0] in ('strzel', 'rusz'):
        for el in lista[1:4]:
            try:
                if int(el) > 0 and int(el) < 11:
                    wsp['x'] = int(el) - 1
            except ValueError:
                pass
            try:
                if (el.upper() >= 'A' and el.upper() <= 'J'):
                    wsp['y'] = ord(el.upper()) - ord('A')
                elif (el.upper() >= 'Q' and el.upper() <= 'Z'):
                    wsp['z'] = ord(el.upper()) - ord('Q')
            except TypeError:
                pass
    return wsp;


def naslucher(ip, port):
    global myTurn
    TCP_IP = ip
    TCP_PORT = port
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print 'Polaczonod z', addr
    myTurn = conn.recv(BUFFER_SIZE)
    data = [];
    while data != 'q':
       data = conn.recv(BUFFER_SIZE)
       wsp = parse_data(data)
       print "rec_wsp:", wsp
       conn.send(data)  # echo
    conn.close()


def sender(ip, port):
    TCP_IP = ip
    TCP_PORT = port
    BUFFER_SIZE = 1024
    MESSAGE = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send('JESTEM')
    while MESSAGE != 'q':
        MESSAGE = raw_input()
        s.send(MESSAGE)
        data = s.recv(BUFFER_SIZE)
        print "ack:", data
    s.close()

def ryser():
    global repaint
    while True:
        if repaint:
            plansza.rysuj()
            repaint = False

if __name__ == "__main__":
    myTurn = 1
    repaint = True
    plansza = HexGrid(10,10)
    plansza.rysuj()
    """
    try:
        r = Thread(target=ryser, args=())
        r.start()
        s = Thread(target=naslucher, args=('localhost',50000))
        s.start()
        print ("Podaj ip:")
        ip = raw_input()
        k = Thread(target=sender, args=(ip,50001))
        k.start()
    except:
        print "watek nie zastartowal"
            """