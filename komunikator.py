import socket
from msgParser import Parser

class Komunikator:
    def __init__(self):
        self._msg_to_send = ""
        self._msg_parser = Parser()
        self._tx_socket = None
        self._rx_socket = None

    def send_shoot(self):
            pass

    def send_move(self):
            pass

    def send_surrender(self):
            pass

    def recv_terminate(self):
        self._conn.close()
        print "Reciever: socket closed."

    def recv_loop(self):
        data = []
        BUFFER_SIZE = 20  # Normally 1024, but we want fast response
        while data != 'q':
            data = self._conn.recv(BUFFER_SIZE)
            wsp = self.parse_data(data)
            print "Reciever: rec_wsp:", wsp
            self._conn.send(data)  # echo
        self.recv_terminate()

    def recv_init(self, ip, port):
        TCP_IP = ip
        TCP_PORT = port
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((TCP_IP, TCP_PORT))
            print "Reciever: awaiting connection..."
            s.listen(1)
            self._conn, addr = s.accept()
        except:
            print "Reciever: init failed!"

        print 'Reciever: Polaczonod z', addr
        self.recv_loop()


    def sender_init(self, ip, port):
        #TCP Connection
        self._tx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._tx_socket.connect((ip, port))
        except socket.error:
            print "TX: Init failed!"
        else:
            print "TX: Init ok."

    def send(self, msg):
        buf_size = 100
        self._tx_socket.send(msg)
        data = self._tx_socket.recv(buf_size)
        if data == msg:
            print "ACK: OK"
        else:
            raise Exception

    def sender_terminate(self):
        self._sender.close()
        print "TX: Socket closing..."