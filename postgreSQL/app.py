# WebSocket ex.

from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.exceptions import WebSocketError
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, make_response

app = Flask(__name__)
# app.debug = True
ws_list = set()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api')
def api():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        ws_list.add(ws)
        while True:
            try:
                message = ws.receive()
                if message:
                    for ws_client in ws_list:
                        ws_client.send(message)
            except Exception as E:
                ws_list.remove(ws)
                break
    return make_response()


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()