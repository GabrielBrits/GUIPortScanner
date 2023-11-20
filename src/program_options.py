from typing import List
from data import Options
import sys

def process_args(args: List[str]) -> Options:
    options: Options = Options("-sT", "0.0.0.0")
    validScan: List[str] = ["-sT", "-sI", "-sS", "-sN", "-sF", "sX"]
    if args[1] == "--help":
        print_help()
    if len(args) == 2:
        options = Options("-sT", args[1])
    elif len(args) == 3 and args[1] in validScan:
        options = Options(args[1], args[2])
    else:
        raise Exception("Incorrect argument usage, use --help for more information.")
    return options
    

def print_help() -> None:
    print("""------------------------------------------------
Usage: python GUIPortScanner.py Scan_Type target
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