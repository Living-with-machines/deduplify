"""
Hash Files
----------

Walk over a directory structure and hash the files within it. Then group
together files that have generated the same hash.

Author: Sarah Gibson
Python version: >=3.7 (developed with 3.8)
"""

import os
import sys
import json
import hashlib
import logging
from typing import Tuple
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger()


def hashfile(path: str, blocksize: int = 65536) -> Tuple[str, str]:
    """Calculate the MD5 hash of a given file

    Args:
        path ()str, os.path): Path to the file to generate a hash for
        blocksize (int, optional): Memory size to read in the file
                                   Default: 65536

    Returns:
        hash (str): The HEX digest hash of the given file
        path (str): The filepath that generated the hash
    """
    # Instatiate the hashlib module with md5
    hasher = hashlib.md5()

    # Open the file and instatiate the buffer
    f = open(path, "rb")
    buf = f.read(blocksize)

    # Continue to read in the file in blocks
    while len(buf) > 0:
        hasher.update(buf)  # Update the hash
        buf = f.read(blocksize)  # Update the buffer

    f.close()

    return hasher.hexdigest(), path


def filter_dict(results: dict) -> Tuple[dict, dict]:
    """Filter a given dictionary into two separate dictionaries based on the
    conditional that the length of the values is either greater than or equal
    to unity.

    Args:
        results (dict): Dictionary to be filtered

    Results:
        duplicated (dict): Dictionary where len(values) > 1. Considered to be
                           duplicated hashes.
        unique (dict): Dictionary where len(values) == 1. Considered to be
                       unique hashes.
    """
    logger.info("Filtering the results...")
    duplicated = {key: value for (key, value) in results.items() if len(value) > 1}
    unique = {key: value[0] for (key, value) in results.items() if len(value) == 1}

    # Calculate number of unique and duplicated files
    logger.info("Number of unique files: %s" % len(unique))

    total = 0
    for value in duplicated.values():
        total += len(value)

    logger.info("Number of identical files: %s" % total)

    return duplicated, unique


def run_hash(dir: str, count: int, dupfile: str, unfile: str, **kwargs):
    """Hash files within a directory structure

    Args:
        dir (str): Root directory to search under
        count (int): Number of threads to parallelise over
        dupfile (str): JSON file location for duplicated hashes
        unfile (str): JSON file location for unique hashes
    """
    # Check the directory path exists
    if not os.path.exists(dir):
        raise ValueError("Please provide a known filepath!")

    logger.info("Walking structure of: %s" % dir)
    logger.info("Generating MD5 hashes for files...")
    hashes = defaultdict(list)  # Empty dict to store hashes in
    counter = 0

    for dirName, subdirs, fileList in os.walk(dir):
        with ThreadPoolExecutor(max_workers=count) as executor:
            futures = [
                executor.submit(hashfile, os.path.join(dirName, filename))
                for filename in fileList
            ]
            for future in as_completed(futures):
                hash, filepath = future.result()
                hashes[hash].append(filepath)

                counter += 1
                print(f"Total files hashed: {counter}", end="\r")
                sys.stdout.flush()

    dup_dict, unique_dict = filter_dict(hashes)  # Filter the results

    for filename, content in zip([dupfile, unfile], [dup_dict, unique_dict]):
        logger.info("Writing outputs to: %s" % filename)
        with open(filename, "w") as f:
            json.dump(content, f, indent=2, sort_keys=True)
