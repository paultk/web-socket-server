from flask import Flask, request, send_from_directory, make_response, url_for
import first_file as tools
from ws4py.compat import py3k, get_connection, detach_connection


app = Flask(__name__)

a = tools.encode('d')
# print(a)

@app.route('/styles.css')
def styles():
    return send_from_directory('static', 'styles.css')


@app.route('/main.js')
def js():
    return send_from_directory('static', 'main.js')





@app.route('/')
def hello():

    url_for('static', filename='style.css')
    url_for('static', filename='main.js')

    a = request.headers
    b = []
    b.append(a)
    # print(b[0])
    # a = str(a)
    # d = a.find('Cookie')
    # print(a.get('cookie'))
    response = make_response(send_from_directory('static', 'index.html'), 200)
    response.headers['test_heades'] = 'testheader'
    return response

@app.route('/web-server-socket')
def wss():
    print('mainping\n')
    print(request.headers)
    resp = make_response()
    print('request.headers')
    sec_web_key = request.headers.get('Sec-WebSocket-Key')
    # print(sec_web_key)
    sec_web_key_acc = tools.encode(sec_web_key)
    resp.headers['Sec-WebSocket-Accept'] = sec_web_key_acc
    resp.headers['Connection'] = 'Upgrade'
    resp.headers['Sec-WebSocket-Extensions'] = 'permessage-deflate'
    resp.headers['Upgrade'] = 'websocket'

    print('resp')
    print(resp)
    return resp, 101


'''Connection:Upgrade
Sec-WebSocket-Accept:fZxpcbnd6tTtH4/kerUCyDZn0R0=
Sec-WebSocket-Extensions:permessage-deflate
Upgrade:websocket'''


def serve_pages():
    app.run('0.0.0.0', 3000)

