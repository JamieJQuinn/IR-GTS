from src.dns_server import DNSServer
from src.http_server import app, runAsHttp, runAsHttps
from platform import system
import os, threading

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
    
    httpServer = threading.Thread(target=runAsHttp)
    httpsServer = threading.Thread(target=runAsHttps)
    httpServer.start()
    httpsServer.start()
