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
                pass
            case "-sS":
                self.syn_scan()
            case "-sU":
                self.udp_scan()
            case "-sN":
                pass
            case "-sF":
                pass
            case "-sX":
                pass

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
                      f"filtered on IP: {self._target}")
            elif response.haslayer(UDP):
                print(f"UDP Port {self._port} is open on IP: {response.src}")
            elif response.haslayer(ICMP) and int(
                    response.getlayer(ICMP).type) == 3:
                if int(response.getlayer(ICMP).code) == 3:
                    print(f"UDP port {self._port} is closed "
                          f"on IP: {response.src}")
                elif int(response.getlayer(ICMP).code) in [1, 2, 9, 10, 13]:
                    print(f"UDP port {self._port} is filtered on "
                          f"IP: {response.src}")

    def tcp_scan(self):
        raise NotImplementedError("Not yet implemented")

    def syn_scan(self):
            try:
                tcp_packet = IP(dst=self._target) / TCP(dport=self._port,
                                                        flags=self.SYN)
            except socket.gaierror:
                raise InvalidHostName()
            response = sr1(tcp_packet, timeout=2)
            if response is None:
                print(f"TCP Port {self._port} is open or "
                      f"filtered on IP: {self._target}")
            elif response.haslayer(TCP):
                if response.getlayer(TCP).flags == self.SYN + self.ACK:
                    sr(IP(dst=self._target) / TCP(dport=self._port,
                                                  flags=self.RST), timeout=10)
                    print(f"TCP Port {self._port} is open "
                          f"on IP: {response.src} and should be "
                          f"running {socket.getservbyport(self._port)}")
                elif response.getlayer(TCP).flags == self.RST + self.ACK:
                    print(f"TCP Port {self._port} is closed on IP:"
                          f" {response.src}")

    def null_scan(self):
        raise NotImplementedError("Not yet implemented")

    def fin_scan(self):
        raise NotImplementedError("Not yet implemented")

    def xmas_scan(self):
        raise NotImplementedError("Not yet implemented")
