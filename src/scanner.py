import logging
import socket
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import IP, ICMP, sr1, conf

class Scanner():
    def __init__(self, target: str, port: int):
        self._target: str = target
        self._port: int = port
        self._packet = None
    
    def IPscan(self):
        conf.verb = 0
        try:
            packet = IP(dst=self._target)/ICMP()
        except socket.gaierror:
            raise Exception("Cannot resolve domains IP address")
        response = sr1(packet, timeout = 2)
        if response:
            print(f"IP is responsive. ICMP Response received from {response.src}")
        else:
            print(f"No response received {self._target} is unresponsive")

    def TCPscan(self):
        raise NotImplementedError("Not yet implemented")
    
    def SYNscan(self):
        raise NotImplementedError("Not yet implemented")
    
    def NULLscan(self):
        raise NotImplementedError("Not yet implemented")
    
    def FINscan(self):
        raise NotImplementedError("Not yet implemented")
    
    def XMASscan(self):
        raise NotImplementedError("Not yet implemented")