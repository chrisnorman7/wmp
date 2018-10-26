"""Provides the WebSocket class."""

from autobahn.twisted.websocket import WebSocketServerProtocol
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.python.log import msg
from .connection_states import ConnectionStates
from .tcp import TCPConnection


class TCPFactory(ClientFactory):
    """Match TCP connections to websockets."""

    protocol = TCPConnection


class WebSocket(WebSocketServerProtocol):
    """Handles messages between users and MUD connections."""

    def output(self, message):
        """Output a line of text."""
        for line in message.splitlines():
            self.sendMessage(line)

    def output_special(self, message, surrounding=b'***'):
        """Output a line which is surrounded by the contents of the surrounding
        variable."""
        line = surrounding + b' ' + message + b' ' + surrounding
        return self.output(line)

    def onOpen(self):
        """Set up initial variables."""
        self.log_kwargs = dict(peer=self.transport.getPeer())
        self.mud_state = ConnectionStates.disconnected
        self.hostname = None
        self.tcp = None
        self.log_message('Conected.')

    def log_message(self, message, **kwargs):
        """Log something to the logger."""
        kwargs.update(**self.log_kwargs)
        msg(message, **kwargs)

    def onMessage(self, payload, binary):
        """A message has been received, let's do something useful."""
        if binary:
            raise RuntimeError('Binary payloads not supported.')
        elif self.hostname is None:
            self.hostname = payload
            self.log_message('MUD Hostname', mud_hostname=self.hostname)
        elif self.mud_state is ConnectionStates.connecting:
            self.output_special('Not connected yet.')
        elif self.mud_state is ConnectionStates.disconnected:
            self.mud_state = ConnectionStates.connecting
            port = int(payload)
            self.log_message('MUD Port', mud_port=port)
            factory = TCPFactory()
            self.log_message('MUD Connecting', factory=factory)
            factory.websocket = self
            reactor.connectTCP(self.hostname, port, factory)
        else:
            self.tcp.sendLine(payload)
            self.log_message('MUD Command', command=payload)

    def onClose(self, clean, code, reason):
        """Socket is closed. Close the TCP connection to."""
        self.log_message(reason, code=code)
        if self.tcp is not None:
            self.tcp.transport.loseConnection()

    def disconnect(self, reason):
        """Close this socket cleanly."""
        self.sendClose(code=self.CLOSE_STATUS_CODE_NORMAL, reason=reason)
