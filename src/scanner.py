import logging
import socket

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import IP, ICMP, UDP, TCP, sr1, sr, conf
from exceptions import InvalidHostName


class Scanner:
    FIN = "F"
    SYN = "S"
    RST = "R"
    PSH = "P"
    ACK = "A"
    URG = "U"
    ECE = "E"
    CWR = "C"

    def __init__(self, scan_type: str, target: str, port: int):
        self._target: str = target
        self._port: int = port
        self._scan_type = scan_type
        self._packet = None
        conf.verb = 0

    def initiate_scan(self) -> None:
        match self._scan_type:
            case "-sI":
                self.ip_scan()
            case "-sT":
                self.tcp_scan()
            case "-sS":
                self.syn_scan()
            case "-sU":
                self.udp_scan()
            case "-sN":
                self.null_scan()
            case "-sF":
                self.fin_scan()
            case "-sX":
                self.xmas_scan()

    def ip_scan(self) -> None:
        try:
            ip_packet = IP(dst=self._target) / ICMP()
        except socket.gaierror:
            raise InvalidHostName()
        response = sr1(ip_packet, timeout=2)
        if response:
            print(f"IP is responsive. ICMP Response "
                  f"received from {response.src}")
        else:
            print(f"No response received {self._target} is unresponsive")

    def udp_scan(self) -> None:
        if self._port != 0:
            try:
                udp_packet = IP(dst=self._target) / UDP(dport=self._port)
            except socket.gaierror:
                raise InvalidHostName()
            response = sr1(udp_packet, timeout=2)
            if response is None:
                print(f"UDP Port {self._port} is open or "
                      f"filtered on IP: {self._target} running"
                      f" {socket.getservbyport(self._port, 'udp')}")
            elif response.haslayer(UDP):
                print(f"UDP Port {self._port} is open on IP: {response.src}, "
                      f"running {socket.getservbyport(self._port, 'udp')}")
            elif response.haslayer(ICMP) and int(
                    response.getlayer(ICMP).type) == 3:
                if int(response.getlayer(ICMP).code) == 3:
                    print(f"UDP port {self._port} is closed "
                          f"on IP: {response.src} running "
                          f"{socket.getservbyport(self._port)}")
                elif int(response.getlayer(ICMP).code) in [1, 2, 9, 10, 13]:
                    print(f"UDP port {self._port} is filtered on "
                          f"IP: {response.src} running "
                          f"{socket.getservbyport(self._port)}")

    def tcp_scan(self):
        try:
            tcp_packet = IP(dst=self._target) / TCP(dport=self._port,
                                                    flags=self.SYN)
        except socket.gaierror:
            raise InvalidHostName()
        response = sr1(tcp_packet, timeout=2)
        if response is None:
            print(f"TCP Port {self._port} is open or "
                  f"filtered on IP: {self._target} running "
                  f"{socket.getservbyport(self._port)}")
        elif response.haslayer(TCP):
            if response.getlayer(TCP).flags == self.SYN + self.ACK:
                sr(IP(dst=self._target) / TCP(dport=self._port,
                                              flags=self.ACK), timeout=10)
                print(f"TCP Port {self._port} is open "
                      f"on IP: {response.src} and should be "
                      f"running {socket.getservbyport(self._port)}")
            elif response.getlayer(TCP).flags == self.RST + self.ACK:
                print(f"TCP Port {self._port} is closed on IP:"
                      f" {response.src} running "
                      f"{socket.getservbyport(self._port)}")

    def syn_scan(self):
        try:
            tcp_packet = IP(dst=self._target) / TCP(dport=self._port,
                                                    flags=self.SYN)
        except socket.gaierror:
            raise InvalidHostName()
        response = sr1(tcp_packet, timeout=2)
        if response is None:
            print(f"TCP Port {self._port} is open or "
                  f"filtered on IP: {self._target} running "
                  f"{socket.getservbyport(self._port)}")
        elif response.haslayer(TCP):
            if response.getlayer(TCP).flags == self.SYN + self.ACK:
                sr(IP(dst=self._target) / TCP(dport=self._port,
                                              flags=self.RST), timeout=10)
                print(f"TCP Port {self._port} is open "
                      f"on IP: {response.src} and should be "
                      f"running {socket.getservbyport(self._port)}")
            elif response.getlayer(TCP).flags == self.RST + self.ACK:
                print(f"TCP Port {self._port} is closed on IP:"
                      f" {response.src} running "
                      f"{socket.getservbyport(self._port)}")

    def null_scan(self):
        try:
            tcp_packet = IP(dst=self._target) / TCP(dport=self._port, flags="")
        except socket.gaierror:
            raise InvalidHostName()
        response = sr1(tcp_packet, timeout=2)
        if response is None:
            print(f"TCP Port {self._port} is open or "
                  f"filtered on IP: {self._target}, "
                  f"running {socket.getservbyport(self._port)}")
        elif response.haslayer(TCP):
            if (response.getlayer(TCP).flags == self.RST or
                    response.getlayer(TCP).flags == self.RST + self.ACK):
                print(f"TCP Port {self._port} is closed on IP:"
                      f" {response.src} running "
                      f"{socket.getservbyport(self._port)}")
        elif (response.haslayer(ICMP) and int(response.getlayer(ICMP).code)
              in [1, 2, 3, 9, 10, 13]):
            print(f"TCP port {self._port} is filtered on "
                  f"IP: {response.src} running "
                  f"{socket.getservbyport(self._port)}")

    def fin_scan(self):
        try:
            tcp_packet = IP(dst=self._target) / TCP(dport=self._port,
                                                    flags=self.FIN)
        except socket.gaierror:
            raise InvalidHostName()
        response = sr1(tcp_packet, timeout=2)
        if response is None:
            print(f"TCP Port {self._port} is open or "
                  f"filtered on IP: {self._target}, "
                  f"running {socket.getservbyport(self._port)}")
        elif response.haslayer(TCP):
            if (response.getlayer(TCP).flags == self.RST or
                    response.getlayer(TCP).flags == self.RST + self.ACK):
                print(f"TCP Port {self._port} is closed on IP:"
                      f" {response.src} running "
                      f"{socket.getservbyport(self._port)}")
        elif (response.haslayer(ICMP) and int(response.getlayer(ICMP).code)
              in [1, 2, 3, 9, 10, 13]):
            print(f"TCP port {self._port} is filtered on "
                  f"IP: {response.src} running "
                  f"{socket.getservbyport(self._port)}")

    def xmas_scan(self):
        try:
            tcp_packet = (IP(dst=self._target) /
                          TCP(dport=self._port, flags=self.FIN + self.PSH +
                          self.URG))
        except socket.gaierror:
            raise InvalidHostName()
        response = sr1(tcp_packet, timeout=2)
        if response is None:
            print(f"TCP Port {self._port} is open or "
                  f"filtered on IP: {self._target}, "
                  f"running {socket.getservbyport(self._port)}")
        elif response.haslayer(TCP):
            if (response.getlayer(TCP).flags == self.RST or
                    response.getlayer(TCP).flags == self.RST + self.ACK):
                print(f"TCP Port {self._port} is closed on IP:"
                      f" {response.src} running "
                      f"{socket.getservbyport(self._port)}")
        elif (response.haslayer(ICMP) and int(response.getlayer(ICMP).code)
              in [1, 2, 3, 9, 10, 13]):
            print(f"TCP port {self._port} is filtered on "
                  f"IP: {response.src} running "
                  f"{socket.getservbyport(self._port)}")
