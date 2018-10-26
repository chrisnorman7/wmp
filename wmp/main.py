"""Contains the main function."""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from autobahn.twisted.websocket import WebSocketServerFactory, listenWS
from .app import app
from .websocket import WebSocket

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

parser.add_argument(
    'host', nargs='?', default='0.0.0.0', help='Host to listen on'
)
parser.add_argument(
    'server_port', nargs='?', metavar='SERVER-PORT', type=int, default=1234,
    help='The port to run the web server on'
)
parser.add_argument(
    'websocket_port', nargs='?', metavar='WEBSOCKET-PORT', type=int,
    default=9000, help='The port to listen for websocket connections'
)


def main(args=None):
    if args is None:
        args = parser.parse_args()
    factory = WebSocketServerFactory(f'ws://{args.host}:{args.websocket_port}')
    factory.protocol = WebSocket
    listenWS(factory, interface=args.host)
    app.websocket_port = args.websocket_port
    app.run(host=args.host, port=args.server_port)
