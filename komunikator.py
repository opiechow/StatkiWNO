import socket
from gameState import GameState
from msgParser import Parser

class Komunikator:
    def __init__(self, game_state):
        self._msg_to_send = ""
        self._game_state = game_state
        self._msg_parser = Parser(game_state)
        self._tx_socket = None
        self._rx_socket = None
        self._rx_port = 5000
        self._tx_port = 5001
        self._connection = False
        self._recieve_Thread = None

    def send_shoot(self, sel):
        assert self._connection
        self._game_state.next_turn()
        msg = self._msg_parser.get_shoot_message(sel)
        self.send(msg)

    def send_move(self):
        assert self._connection
        self._game_state.next_turn()

    def send_surrender(self):
            pass

    def recv_loop(self):
        self._connection = True
        # print "Recive loop starting"
        data = []
        BUFFER_SIZE = 50  # Normally 1024, but we want fast response
        try:
            while self._connection:
                data = self._rx_socket.recv(BUFFER_SIZE)
                self._rx_socket.send(data)  # echo
                new_msg = self._msg_parser.parse(data)
                if new_msg:
                    self.send(new_msg)
        except:
            pass
            # print "RecvLoopDies..."

    def server_init(self):
        # try:
        assert isinstance(self._game_state, GameState)
        self._game_state.s_my_turn(True)
        self._game_state.start_game()
        rx_listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rx_listen_socket.bind(('localhost', self._rx_port))
        print "Server: awaiting connection"
        rx_listen_socket.listen(1)
        self._rx_socket, (ip,port) = rx_listen_socket.accept()
        print 'Server: Connection with', (ip,port)
        self._tx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ok = self._rx_socket.recv(2)
        if ok == "ok":
            self._tx_port = int(self._tx_port)
            self._tx_socket.connect((ip,self._tx_port))
            self._tx_socket.send("ok")
        self.recv_loop()
        # except:
        #     print "Server: init failed"

    def client_init(self, ip):
        #TCP Connection
        self._game_state.s_my_turn(False)
        self._game_state.start_game()
        self._tx_port, self._rx_port = self._rx_port, self._tx_port
        self._tx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            addr = (ip,self._tx_port)
            self._tx_socket.connect(addr)
            rx_listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            rx_listen_socket.bind(('localhost', self._rx_port))
            print "Client: awaiting connection..."
            rx_listen_socket.listen(1)
            self._tx_socket.send("ok")
            self._rx_socket, (ip, port) = rx_listen_socket.accept()
            ok = self._rx_socket.recv(2)
            assert ok == "ok"
        except socket.error:
            print "Client: Init failed!"
            self.cleanup()
        else:
            print "Client: Init ok."
            self.recv_loop()

    def cleanup(self):
        self._connection = False;
        try:
            self._tx_socket.close()
        except AttributeError:
            print "TX Socket: Not initialized"
        try:
            self._rx_socket.close()
        except AttributeError:
                print "RX Socket: Not initialized"

    def send(self, msg):
        buf_size = len(msg)
        self._tx_socket.send(msg)
        data = self._tx_socket.recv(buf_size)
        if data == msg:
            print "ACK: OK"
        else:
            raise Exception