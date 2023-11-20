from dataclasses import dataclass

@dataclass
class Options:
    scanType: str
    ip: str
    port: int