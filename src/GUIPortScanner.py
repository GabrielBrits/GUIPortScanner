import program_options as po
import sys
from scanner import Scanner
from data import Options

def handle_scan(scanType: str, ip: str, port: int) -> None:
    match scanType:
        case "-sI":
            scanner = Scanner(ip, port)
            scanner.IPscan()
        case "-sT":
            pass 
        case "-sS":
            pass 
        case "-sU":
            pass 
        case "-sN":
            pass 
        case "-sF":
            pass 
        case "-sX":
            pass 

def main() -> None:
    if len(sys.argv) > 1:
        options: Options = po.process_args(sys.argv)
        handle_scan(options.scanType, options.ip, options.port)
    else:
        pass

if __name__ == "__main__":
    main()