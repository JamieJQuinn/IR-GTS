import socket, threading
import dns.message
import dns.query
import dns.resolver
import dns.reversename
from .loghandler import LogHandler

dns_logging = LogHandler('dns_server', 'network.log').get_logger()

class DNSServer:
    def __init__(self, dns_ip:str="178.62.43.212") -> None:
        self.dns_ip = dns_ip

        self.proxy_ip = self.get_proxy_ip()
        self.proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Binding to a specific IP solves a problem when a device has 2 network interfaces.
        #It may be possible that the source IP address of the DNS answers is not the same as the told DNS address.
        #This leads to the DS not accepting the answer.
        self.proxy_socket.bind((self.proxy_ip, 53))


    def get_proxy_ip(self) -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((self.dns_ip, 53))
        s_name = s.getsockname()[0]
        return s_name


    def start(self) -> None:
        thread = threading.Thread(target=self.start_as_thread)
        thread.start()


    def start_as_thread(self):
        dns_logging.info(f"DNSProxy server started. ")
        dns_logging.info(f"Primary DNS server: {self.proxy_ip}")
        while True:
            dns_query, client_address = self.proxy_socket.recvfrom(512)[:2]
            dns_logging.debug(f"Received DNS query from {client_address}")
            self.handle_dns_query(dns_query, client_address)


    def handle_dns_query(self, dns_query, client_address) -> None:
        try:
            request = dns.message.from_wire(dns_query)
            # log all data in the request
            dns_logging.debug(f"DNS query: {request.to_text()}")
            response = dns.query.udp(request, self.dns_ip)
            dns_logging.debug(f"DNS response: {response.to_text()}")

            modified_response = self.modify_dns_response(response)
            self.proxy_socket.sendto(modified_response.to_wire(), client_address)
        except Exception as e:
            dns_logging.error(f"Error handling DNS query: {e}")


    def modify_dns_response(self, response) -> dns.message.Message:
        for answer in response.answer:
            if answer.rdtype == dns.rdatatype.A:
                new_rdatas = dns.rdataset.Rdataset(answer.rdclass, answer.rdtype)
                for rd in answer:
                    dns_logging.debug(f"DNS returns IP {rd.address} for {answer.name}")
                    for domain in ["gamestats2.gs.nintendowifi.net", "dls1.ilostmymind.xyz"]:
                        if answer.name == dns.name.from_text(domain):
                            dns_logging.debug(f"Changing IP for {answer.name} from {rd.address} to {self.proxy_ip}")
                            new_rdatas.add(rd.replace(address=self.proxy_ip), answer.ttl)
                if len(new_rdatas) == 1:
                    answer.clear()
                    answer.update(new_rdatas)
        return response

if __name__ == "__main__":
    proxy_server = DNSServer()
    proxy_server.start()
