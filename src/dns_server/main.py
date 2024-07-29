import os

from dns_server import DNSServer


def main():
    ip = os.environ.get('IP')
    dns_server = DNSServer(prox_ip=ip)
    dns_server.start()


if __name__ == '__main__':
    main()