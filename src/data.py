from dataclasses import dataclass


@dataclass
class Options:
    scan_type: str
    ip: str
    port: int
