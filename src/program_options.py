from typing import List
from data import Options
from exceptions import IncorrectArgumentUsage, InvalidPortNumber
import sys


def process_args(args: List[str]) -> Options:
    valid_scan: List[str] = ["-sT", "-sI", "-sS", "-sN", "-sF", "-sX", "-sU"]
    if args[1] == "--help":
        print_help()
    if len(args) == 2:
        options = Options("-sT", args[1], 0)
    elif len(args) == 3 and args[1] in valid_scan:
        options = Options(args[1], args[2], 0)
    elif len(args) == 4 and args[1] == "-p":
        try:
            port: int = int(args[2])
        except ValueError:
            raise IncorrectArgumentUsage()
        if 0 < port < 65536:
            options = Options("-sT", args[2], port)
        else:
            raise InvalidPortNumber()
    elif len(args) == 5 and args[1] in valid_scan and args[2] == "-p":
        try:
            port = int(args[3])
        except ValueError:
            raise IncorrectArgumentUsage()
        if 0 < port < 65536:
            options = Options(args[1], args[4], port)
        else:
            raise InvalidPortNumber()
    else:
        raise IncorrectArgumentUsage()
    return options


def print_help() -> None:
    print("""------------------------------------------------
Usage: python GUIPortScanner.py [scan_type] [-p port] target
------------------------------------------------
SCAN TYPE:
-sT: TCP scan
-sI: IP scan
-sU: UDP scan
-sS: SYN scan
-sN: NULL scan
-sF: FIN scan
-sX: XMAS scan
------------------------------------------------
PORT:
Integer in the range of 1 - 65535 (inclusive)
------------------------------------------------
TARGETS:
IP adresses
hostname""")
    sys.exit()
