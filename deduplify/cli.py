import sys
import logging
import argparse
from multiprocessing import cpu_count

from .hash_files import run_hash
from .compare_files import run_compare
from .del_empty_dirs import empty_dir_search

CPUS = cpu_count()


def setup_logging(verbose=False):
    """Setup logging config"""
    if verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(asctime)s %(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            filename="deduplify.log",
            filemode="a",
            format="[%(asctime)s %(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Find and delete duplicated files in messy datasets"
    )
    subparsers = parser.add_subparsers(
        required=True, dest="command", help="Available subcommands"
    )

    # Base parser
    parser_base = argparse.ArgumentParser(add_help=False)
    parser_base.add_argument(
        "-c",
        "--count",
        type=int,
        default=1,
        dest="count",
        help="Number of threads to parallelise over. Default: 1",
    )
    parser_base.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print logging messages to the console",
    )

    # Positional parser
    parser_pos = argparse.ArgumentParser(add_help=False)
    parser_pos.add_argument(
        "dir", type=str, help="Path to directory to begin search from"
    )

    # Hash subcommand
    parser_hash = subparsers.add_parser(
        "hash",
        parents=[parser_base, parser_pos],
        help="Generate hashes of all files in a directory tree",
    )
    parser_hash.set_defaults(func=run_hash)

    parser_hash.add_argument(
        "-d",
        "--dupfile",
        type=str,
        dest="dupfile",
        default="duplicates.json",
        help="Destination file for duplicated hashes. Must be a JSON file. Default: duplicates.json",
    )
    parser_hash.add_argument(
        "-u",
        "--unfile",
        type=str,
        dest="unfile",
        default="uniques.json",
        help="Destination file for unique hashes. Must be a JSON file. Default: uniques.json",
    )

    # Compare subcommand
    parser_compare = subparsers.add_parser(
        "compare",
        parents=[parser_base],
        help="Compare hashes for duplicated files",
    )
    parser_compare.set_defaults(func=run_compare)

    parser_compare.add_argument(
        "-i",
        "--infile",
        type=str,
        default="duplicates.json",
        help="Filename to analyse. Must be a JSON file. Default: duplicates.json",
    )
    parser_compare.add_argument(
        "--purge", action="store_true", help="Deletes duplicated files. Default: False"
    )

    # Clean subcommand
    parser_clean = subparsers.add_parser(
        "clean",
        parents=[parser_base, parser_pos],
        help="Clean up empty subdirectories",
    )
    parser_clean.set_defaults(func=empty_dir_search)

    return parser.parse_args()


def main():
    args = parse_args(sys.argv[1:])

    for file_arg in ["infile", "dupfile", "unfile"]:
        if (file_arg in vars(args).keys()) and not (
            vars(args)[file_arg].endswith(".json")
        ):
            raise ValueError("Please provide a JSON input file!")

    if args.count > CPUS:
        raise ValueError(
            "You have requested more threads than are available to this machine. "
            f"This machine has {CPUS} CPUs. "
            "Please reduce your value of --count accordingly."
        )

    setup_logging(verbose=args.verbose)
    args.func(**vars(args))


if __name__ == "__main__":
    main()
