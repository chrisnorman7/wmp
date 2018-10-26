"""Provides the web portion of the app."""

import os.path
from socket import getfqdn
from jinja2 import Environment, FileSystemLoader
from klein import Klein
from twisted.web.static import File

hostname = getfqdn()
app = Klein()
environment = Environment(loader=FileSystemLoader('templates'))

client_js_template = os.path.join('templates', 'client.js')


def render_template(request, name, *args, **kwargs):
    """Return a Rendered emplate string."""
    template = environment.get_template(name)
    kwargs.setdefault('request', request)
    return template.render(*args, **kwargs)


@app.route('/')
def index(request):
    """Render the home page."""
    js_timestamp = os.path.getmtime(client_js_template)
    return render_template(request, 'index.html', js_timestamp=js_timestamp)


@app.route('/static/', branch=True)
def static(request):
    """Return the static directory."""
    return File('static')


@app.route('/client.js')
def client_js(request):
    return render_template(
        request, 'client.js', host=getfqdn(), port=app.websocket_port
    )
