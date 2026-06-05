"""python -m unit_converter 진입점 (SPEC §5)."""

import sys

from unit_converter.app.cli import run_cli


def main(argv=None):
    for line in run_cli(sys.argv[1:] if argv is None else argv):
        print(line)


if __name__ == "__main__":
    main()
