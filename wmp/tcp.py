"""Provides the TCPConnection class."""

from twisted.protocols.basic import LineReceiver
from .connection_states import ConnectionStates


class TCPConnection(LineReceiver):
    """Sends messages to and from MUD clients."""

    def connectionMade(self):
        """Let the websocket know we are connected."""
        self.websocket = self.factory.websocket
        self.websocket.output_special('Connected.'.encode())
        self.websocket.mud_state = ConnectionStates.connected
        self.websocket.tcp = self

    def connectionLost(self, reason):
        """Let the user know we're disconnected, then boot them off."""
        self.websocket.disconnect(reason.getErrorMessage())

    def lineReceived(self, line):
        """Send the line to the user."""
        self.websocket.output(
            line.decode('utf-8', 'ignore').encode('ascii', 'ignore')
        )
