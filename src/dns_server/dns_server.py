from datetime import datetime
import socket, threading
import dns.message
import dns.query
import dns.resolver
import dns.reversename
from loguru import logger

start_time = datetime.now()
logger.add(f"/logs/{start_time.strftime('%Y%m%d%H%M%S')}")

class DNSServer:
    def __init__(self, dns_ip:str="178.62.43.212", prox_ip=None) -> None:
        self.dns_ip = dns_ip

        self._proxy_ip = prox_ip
        self.proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.proxy_socket.bind(("0.0.0.0", 53))


    @property
    def proxy_ip(self) -> str:
        if not self._proxy_ip:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((self.dns_ip, 53))
            self._proxy_ip = s.getsockname()[0]
        return self._proxy_ip


    def start(self) -> None:
        thread = threading.Thread(target=self.start_as_thread)
        thread.start()


    def start_as_thread(self):
        logger.info(f"DNSProxy server started.")
        logger.info(f"Primary DNS server: {self.proxy_ip}")
        while True:
            dns_query, client_address = self.proxy_socket.recvfrom(512)
            logger.debug(f"Received DNS query from {client_address}")
            self.handle_dns_query(dns_query, client_address)


    def handle_dns_query(self, dns_query, client_address) -> None:
        try:
            request = dns.message.from_wire(dns_query)
            # log all data in the request
            logger.debug(f"DNS query: {request.to_text()}")
            response = dns.query.udp(request, self.dns_ip)
            logger.debug(f"DNS response: {response.to_text()}")

            modified_response = self.modify_dns_response(response)
            self.proxy_socket.sendto(modified_response.to_wire(), client_address)
        except Exception as e:
            logger.error(f"Error handling DNS query: {e}")


    def modify_dns_response(self, response) -> dns.message.Message:
        for answer in response.answer:
            if answer.rdtype == dns.rdatatype.A:
                for rd in answer:
                    logger.debug(f"DNS returns IP {rd.address} for {answer.name}")
                    for domain in ["gamestats2.gs.nintendowifi.net"]: #  "dls1.ilostmymind.xyz", eventually..
                        if answer.name == dns.name.from_text(domain):
                            logger.debug(f"Changing IP for {answer.name} from {rd.address} to {self.proxy_ip}")
                            rd.address = self.proxy_ip
        return response

if __name__ == "__main__":
    proxy_server = DNSServer()
    proxy_server.start()
