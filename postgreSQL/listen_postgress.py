from pgnotify import await_pg_notifications
import websocket

ws = websocket.WebSocket()
ws.connect("ws://127.0.0.1:5000/api")

for notification in await_pg_notifications(
        'postgresql://web_exchange:password@localhost:5432/myproject',
        ['db_notifications', ]):
    ws.send(notification.payload)
    # print(notification.channel)
    # print()