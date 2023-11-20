from typing import List
from data import Options
import sys

def process_args(args: List[str]) -> Options:
    validScan: List[str] = ["-sT", "-sI", "-sS", "-sN", "-sF", "sX"]
    if args[1] == "--help":
        print_help()
        exit()
    if len(args) == 2:
        options = Options("-sT", args[1], 0)
    elif len(args) == 3 and args[1] in validScan:
        options = Options(args[1], args[2], 0)
    elif len(args) == 4 and args[1] == "-p":
        try:
            port: int = int(args[2])
        except ValueError:
            raise Exception("Incorrect argument usage, use --help for more information.")
        if (port > 0 and port < 65536):
            options = Options("-sT", args[2], args[3])
        else:
            raise Exception("Invalid port number, needs to be in the range of 1 - 65545 (inclusive)")
    elif len(args) == 5 and args[1] in validScan and args[2] == "-p" and (int(args[3]) > 0 and int(args[3]) < 65536):
        options = Options(args[1], args[4], args[3])
    else:
        raise Exception("Incorrect argument usage, use --help for more information.")
    return options
    

def print_help() -> None:
    print("""------------------------------------------------
Usage: python GUIPortScanner.py [scan_type] [port] target
------------------------------------------------
SCAN TYPE:
-sT: TCP scan
-sI: IP scan
-sS: SYN scan
-sN: NULL scan
-sF: FIN scan
-sX: XMAS scan
------------------------------------------------
TARGETS
------------------------------------------------
IP adresses
hostname""")