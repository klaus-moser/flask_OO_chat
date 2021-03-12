import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': './public/'
})


@sio.event
def connect(sid: str, environ: dict) -> None:
    """
    Connect event from client to server.
    :param sid: Session id created by socket server.
    :param environ: Headers, cookies etc. from client.
    :return: None.
    """
    print(sid, 'connected')


@sio.event
def disconnect(sid: str) -> None:
    """
    Disconnect server from client.
    :param sid: Session id.
    :return: None.
    """
    print(sid, 'disconnected')
