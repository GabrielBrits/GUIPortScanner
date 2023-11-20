import program_options as po
import sys
from typing import List

def main() -> None:
    if len(sys.argv) > 1:
        po.process_args(sys.argv)
    else:
        pass

if __name__ == "__main__":
    main()