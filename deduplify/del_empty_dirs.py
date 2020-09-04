"""
Delete Empty Directories
------------------------

Script to search for and delete empty directories.

Author: Sarah Gibson
Python version: >= 3.7 (developed with 3.8)
"""

import os
import logging

logger = logging.getLogger()


def empty_dir_search(dir_to_walk):
    """Walk over the directory structure under a given parent directory. If a
    directory is empty, delete it.

    Args:
        dir_to_walk ()str): Directory to begin walk from
    """
    for dirname, _, _ in os.walk(dir_to_walk, topdown=False):
        if len(os.listdir(dirname)) == 0:
            logger.info("EMPTY: %s" % dirname)
            os.rmdir(dirname)
