from YAMLDataReader import YAMLDataReader
from CheckAll90Ratings import CheckAll90Ratings
import argparse
import sys


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def main():
    path = get_path_from_arguments(sys.argv[1:])
    reader = YAMLDataReader()
    students = reader.read(path)
    print("Students: ", students)
    rating = CheckAll90Ratings(students).calc()
    print("Ratings All 90: ", rating)


if __name__ == "__main__":
    main()
