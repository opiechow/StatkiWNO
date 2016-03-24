import socket

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