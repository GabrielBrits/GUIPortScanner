import program_options as po
import sys
from scanner import Scanner
from data import Options


def main() -> None:
    if len(sys.argv) > 1:
        options: Options = po.process_args(sys.argv)
        scanner: Scanner = Scanner(options.scan_type, options.ip, options.port)
        scanner.initiate_scan()
    else:
        # Handle GUI
        pass


if __name__ == "__main__":
    main()
