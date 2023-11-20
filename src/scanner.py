import scapy.all

class Scanner():
    def __init__(self, target: str, port: int):
        self._target = target
        self._port = port
    
    def IPscan(self):
        raise NotImplementedError("Not yet implemented")

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