import struct
import threading

import time
from flask import Flask, request, send_from_directory, make_response, url_for
import first_file as tools
import socket


app = Flask(__name__)
clients = []
main_socket = None

# %x0 denotes a continuation frame

'''      *  %x1 denotes a text frame

      *  %x2 denotes a binary frame

      *  %x3-7 are reserved for further non-control frames

      *  %x8 denotes a connection close

      *  %x9 denotes a ping

      *  %xA denotes a pong

      *  %xB-F are reserved for further control frames'''






a = '''Connection:Upgrade
Sec-WebSocket-Accept:FpSN9QBOlPHD2+9GJaWu+5tEY2Y=
Sec-WebSocket-Extensions:permessage-deflate
Upgrade:websocket'''


def listen_for_client(connection, address):
    if handshake(connection):
        get_messages(connection)


def handshake(connection):
    try:
        message = str(connection.recv(1024))
        start = message.find('Sec-WebSocket-Key')
        client_key = message[start + 43 - 24:start + 43]
        if client_key is None:
            connection.close()
            return False
        print('client_key')
        print(client_key)

        return_key = tools.encode(client_key)

        # todo: status code 1002 MUST quit connection
        # connection.send(
        c = bytearray(('HTTP/1.1 101 Switching Protocols\n'
                       'Upgrade: Websocket\n'
                       'Connection: Upgrade\n'
                       'Sec-WebSocket-Accept: ' + str(return_key.decode('utf-8')) + '\r\n\r\n'), 'utf8')
        connection.send(c)
        clients.append(connection)
        return True
    except: print('error')


def get_messages(connection):
    while True:
        msg = connection.recv(1024)
        if len(msg) > 1:
            finished = False
            answ = ''
            while not finished:
                temp, finished = tools.decode_message(msg)
                answ += temp
                # asw = asw.decode('utf8')
            print('message from client')
            print(answ)


def start_server():
    print('starting web server!')
    main_socket = socket.socket()
    # main_socket.sendall()
    main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    main_socket.bind(('0.0.0.0', 3001))
    main_socket.listen()
    while True:
        connection, address = main_socket.accept()
        threading.Thread(target=listen_for_client, args=(connection, address)).start()


# start_server()





