import logging
import socket
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import IP, ICMP, UDP, sr1, conf
import logging
import socket
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import IP, ICMP, sr1, conf

class Scanner():
    def __init__(self, scanType: str, target: str, port: int):
        self._target: str = target
        self._port: int = port
        self._scanType = scanType
        self._packet = None
        conf.verb = 0
    
    def InitiateScan(self) -> None:
        match self._scanType:
            case "-sI":
                self.IPScan()
            case "-sT":
                pass 
            case "-sS":
                pass 
            case "-sU":
                self.UDPscan() 
            case "-sN":
                pass 
            case "-sF":
                pass 
            case "-sX":
                pass 
    
    def IPScan(self) -> None:
        try:
            IPPacket = IP(dst = self._target)/ICMP()
        except socket.gaierror:
            raise Exception("Cannot resolve domains IP address")
        response = sr1(IPPacket, timeout = 2)
        if response:
            print(f"IP is responsive. ICMP Response received from {response.src}")
        else:
            print(f"No response received {self._target} is unresponsive")
    
    def UDPscan(self) -> None:
        if self._port != 0:
            try:
                UDPPacket = IP(dst = self._target)/UDP(dport = self._port)
            except socket.gaierror:
                raise Exception("Cannot resolve domains IP address")
            response = sr1(UDPPacket, timeout = 2)
            if type(response) is type(None):
                print(f"UDP Port {self._port} is open or filtered on IP: {self._target}")
            elif response.haslayer(UDP):
                print(f"UDP Port {self._port} is open on IP: {response.src}")
            elif response.haslayer(ICMP) and int(response.getlayer(ICMP).type) == 3:
                if int(response.getlayer(ICMP).code) == 3:
                    print(f"UDP port {self._port} is closed on IP: {response.src}")
                elif int(response.getlayer(ICMP).code) in [1, 2, 9, 10, 13]:
                    print(f"UDP port {self._port} is filtered on IP: {response.src}")



    def TCPScan(self):
        raise NotImplementedError("Not yet implemented")
    
    def SYNScan(self):
        raise NotImplementedError("Not yet implemented")
    
    def NULLScan(self):
        raise NotImplementedError("Not yet implemented")
    
    def FINScan(self):
        raise NotImplementedError("Not yet implemented")
    
    def XMASScan(self):
        raise NotImplementedError("Not yet implemented")