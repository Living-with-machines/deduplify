"""
Hash Files
----------

Walk over a directory structure and hash the files within it. Then group
together files that have generated the same hash.

Author: Sarah Gibson
Python version: >=3.7 (developed with 3.8, tested with 3.6 -> 3.10)
"""
import fnmatch
import hashlib
import logging
import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple

from tinydb import TinyDB, where
from tqdm import tqdm

logger = logging.getLogger()
EXPANDED_USER = os.path.expanduser("~")


def get_total_number_of_files(target_dir: str, file_ext: str = "*") -> int:
    """Count the total number of files of a given extension in a directory.

    Args:
        target_dir (str): The target directory to search.
        file_ext (str): The file extension to search for. Default: all extensions.

    Returns:
        int: The number of files with the matching extension within the tree
            of the target directory
    """
    logger.info("Calculating number of files that will be hashed in %s" % target_dir)

    output = len(fnmatch.filter(os.listdir(target_dir), f"*.{file_ext}"))

    logger.info(f"{output} files to be hashed in {target_dir}")

    return output


def hashfile(path: str, blocksize: int = 65536) -> Tuple[str, str]:
    """Calculate the MD5 hash of a given file

    Args:
        path (str, os.path): Path to the file to generate a hash for
        blocksize (int, optional): Memory size to read in the file. Default: 65536.

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

    return hasher.hexdigest(), path.replace(EXPANDED_USER, "~")


def identify_duplicates(db):
    """Identify duplicated documents in a given TinyDB database based on the whether
    the hash key in each document is unique in the whole database.

    Args:
        db (TinyDB database): The TinyDB database object to be filtered

    Returns:
        db (TinyDB database): The database updated with the "duplicate" key
            containing a Boolean value indicating if the file has a duplicate or not.
    """
    logger.info("Filtering the results...")

    all_rows = db.all()
    all_hashes = [row["hash"] for row in all_rows]
    counted_hashes = Counter(all_hashes)

    # Add duplicate key to each document in the database indicating
    # whether it is a duplicate or not
    for k, v in counted_hashes.items():
        if v == 1:
            db.update({"duplicate": False}, where("hash") == k)
        elif v > 1:
            db.update({"duplicate": True}, where("hash") == k)

    # Calculate number of unique and duplicated files
    unique = db.search(where("duplicate") == False)
    logger.info("Number of unique files: %s" % len(unique))

    duplicates = db.search(where("duplicate") == True)
    logger.info("Number of duplicated files: %s" % len(duplicates))

    return db


def restart_run(db) -> list:
    """When restarting a hash run, identify which files need to be skipped from the
    database

    Args:
        db (TinyDB database): A TinyDB database objects containing filepaths and hashes
            of the search so far
    """
    logger.info("Restarting hashing process")
    return [os.path.basename(row["filepath"]) for row in db.all()]


def run_hash(dir: str, count: int, dbfile: str, restart: bool = False, **kwargs):
    """Hash files within a directory structure

    Args:
        dir (str): Root directory to search under
        count (int): Number of threads to parallelise over
        dbfile (str): JSON file location for the file hashes database
        restart (bool): If true, will restart a hash run. dupfile and unfile
            must exist since the filenames already hashed will be skipped.
            Default: False.
    """
    # Check the directory path exists
    if not os.path.exists(dir):
        raise ValueError("Please provide a known filepath!")

    hashes_db = TinyDB(dbfile)

    total_file_num = get_total_number_of_files(dir)

    if restart:
        files_to_skip = restart_run(hashes_db)
    else:
        files_to_skip = []

    logger.info("Walking structure of: %s" % dir)
    logger.info("Generating MD5 hashes for files...")

    total = total_file_num - len(files_to_skip)
    pbar = tqdm(total=total)

    for dirName, _, fileList in os.walk(dir):
        with ThreadPoolExecutor(max_workers=count) as executor:
            futures = [
                executor.submit(hashfile, os.path.join(dirName, filename))
                for filename in fileList
                if filename not in files_to_skip
            ]
            for future in as_completed(futures):
                hash, filepath = future.result()
                hashes_db.insert({"hash": hash, "filepath": filepath})

                pbar.update(1)

    pbar.close()

    hashes_db = identify_duplicates(hashes_db)
