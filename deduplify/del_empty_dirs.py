"""
Delete Empty Directories
------------------------

Script to search for and delete empty directories.

Author: Sarah Gibson
Python version: >= 3.7 (developed with 3.8)
"""

import logging
import os
import sys

logger = logging.getLogger()


def empty_dir_search(dir: str, **kwargs):
    """Walk over the directory structure under a given parent directory. If a
    directory is empty, delete it.

    Args:
        dir (str): Directory to begin walk from
    """
    counter = 0
    deleted = 0

    for dirname, subdirs, files in os.walk(dir, topdown=False):
        counter += 1

        if not subdirs and not files:
            logger.info("EMPTY: %s" % dirname)
            os.rmdir(dirname)
            deleted += 1

        print(
            f"Total directories: {counter} / Directories deleted: {deleted}", end="\r"
        )
        sys.stdout.flush()
