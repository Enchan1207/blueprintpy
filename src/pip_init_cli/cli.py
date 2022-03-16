#
# pip_init CLI
#
import pip_init
from argparse import ArgumentParser


def main() -> int:
    parser = ArgumentParser(description="Python package template extractor")
    args = parser.parse_args()
    print("Hello, World!")
    return 0


if __name__ == "__main__":
    result = 0
    try:
        result = main() or 0
    except KeyboardInterrupt:
        print("Ctrl+C")
        exit(result)
