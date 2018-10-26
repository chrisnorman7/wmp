"""Provides the ConnectionStates enum."""

from enum import Enum


class ConnectionStates(Enum):
    """Contains all possible connection states."""

    disconnected = 0
    connecting = 1
    connected = 2
