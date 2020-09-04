"""
Delete Empty Directories
------------------------

Script to search for and delete empty directories.

Author: Sarah Gibson
Python version: >= 3.7 (developed with 3.8)
"""

import os
import logging
import argparse

logging.basicConfig(
    level=logging.DEBUG,
    filename="del_empty_dirs.log",
    filemode="a",
    format="[%(asctime)s %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def parse_args():
    """Parse arguments from the command line

    Returns:
        args {Namespace obj} -- The arguments parsed from the command line
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("dir", help="Directory to begin walk from")

    return parser.parse_args()


def empty_dir_search(dir_to_walk):
    """Walk over the directory structure under a given parent directory. If a
    directory is empty, delete it.

    Arguments:
        dir_to_walk {str} -- Directory to begin walk from
    """
    for dirname, _, _ in os.walk(dir_to_walk, topdown=False):
        if len(os.listdir(dirname)) == 0:
            logging.info("EMPTY: %s" % dirname)
            os.rmdir(dirname)


def main():
    """Main function"""
    args = parse_args()
    empty_dir_search(args.dir)


if __name__ == "__main__":
    main()
