from src.dns_server import DNSServer
from src.http_server import app
from platform import system
import os

def has_privileges():
    """Check if the program is run with superuser privileges."""
    if system() == 'Darwin' or system() == 'Linux':
        if os.geteuid() != 0:
            print('Program must be run as superuser.')
            return False
    return True

if has_privileges():
    dns_server = DNSServer()
    dns_server.start()

    app.run(host='0.0.0.0', port=80, debug=False)

