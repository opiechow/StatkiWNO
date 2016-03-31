import socket

class Komunikator:
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
            s.listen(1)
            self._conn, addr = s.accept()
        except:
            print "Reciever: init failed!"

        print 'Reciever: Polaczonod z', addr
        self.recv_loop()


    def sender_init(self, ip, port):
        TCP_IP = ip
        TCP_PORT = port
        self._sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._sender.connect((TCP_IP, TCP_PORT))
        except:
            print "Sender: Init failed!"
        else:
            print "Sender: Init ok."

    def sender_send(self, MESSAGE):
        BUFFER_SIZE = 1024
        self._sender.send(MESSAGE)
        data = self._sender.recv(BUFFER_SIZE)
        print "Sender: ack:", data

    def sender_terminate(self):
        self._sender.close()
        print "Sender: Socket closing..."


    def parse_data(self,data):
        wsp = {}
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