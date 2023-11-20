import program_options as po
import sys
from data import Options
from typing import List

def main() -> None:
    if len(sys.argv) > 1:
        options: Options = po.process_args(sys.argv)
    else:
        pass

if __name__ == "__main__":
    main()