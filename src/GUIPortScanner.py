import program_options as po
import sys
from data import Options

def main() -> None:
    if len(sys.argv) > 1:
        options: Options = po.process_args(sys.argv)
        print(options.scanType)
        print(options.ip)
        print(options.port)
    else:
        pass

if __name__ == "__main__":
    main()