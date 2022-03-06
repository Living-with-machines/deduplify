"""
Hash Files
----------

Walk over a directory structure and hash the files within it. Then group
together files that have generated the same hash.

Author: Sarah Gibson
Python version: >=3.7 (developed with 3.8)
"""
import hashlib
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple

from tinydb import Query, TinyDB

logger = logging.getLogger()
EXPANDED_USER = os.path.expanduser("~")


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


def restart_run(db) -> list:
    """When restarting a hash run, identify which files need to be skipped from the
    database

    Args:
        db (TinyDB database): A TinyDB database objects containing filepaths and hashes
            of the search so far
    """
    logger.info("Restarting hashing process")
    return [os.path.basename(row["filepath"]) for row in db.all()]


def run_hash(
    dir: str,
    count: int,
    dbfile: str,
    restart: bool = False,
    file_ext: list = ["*"],
    **kwargs,
):
    """Hash files within a directory structure

    Args:
        dir (str): Root directory to search under
        count (int): Number of threads to parallelise over
        dbfile (str): JSON file location for the file hashes database
        restart (bool): If true, will restart a hash run. dupfile and unfile
            must exist since the filenames already hashed will be skipped.
            Default: False.
        file_ext (list[str]): A list of file extensions to search for. Default: all
            extensions (['*']).
    """
    # Check the directory path exists
    if not os.path.exists(dir):
        raise ValueError("Please provide a known filepath!")

    hashes_db = TinyDB(dbfile)
    DBQuery = Query()

    if restart:
        files_to_skip = restart_run(hashes_db)
    else:
        files_to_skip = []

    logger.info("Walking structure of: %s" % dir)
    logger.info("Generating MD5 hashes for files...")

    count_files_hashed = 0
    for dirName, _, fileList in os.walk(dir):
        with ThreadPoolExecutor(max_workers=count) as executor:
            futures = [
                executor.submit(hashfile, os.path.join(dirName, filename))
                for filename in fileList
                if filename not in files_to_skip
                if os.path.splitext(filename)[1].replace(".", "") in file_ext
                or file_ext == ["*"]
            ]
            for future in as_completed(futures):
                hash, filepath = future.result()

                if hashes_db.contains(DBQuery.hash == hash):
                    hashes_db.insert(
                        {"hash": hash, "filepath": filepath, "duplicate": True}
                    )
                    hashes_db.update({"duplicate": True}, DBQuery.hash == hash)
                else:
                    hashes_db.insert(
                        {"hash": hash, "filepath": filepath, "duplicate": False}
                    )

                count_files_hashed += 1
                print(f"Total files hashed: {count_files_hashed}", end="\r", flush=True)

    # Calculate number of unique and duplicated files
    logger.info("Number of files hashed: %s" % len(hashes_db))
    logger.info(
        "Number of unique files: %s" % hashes_db.count(DBQuery.duplicate == False)
    )
    logger.info(
        "Number of duplicated files: %s" % hashes_db.count(DBQuery.duplicate == True)
    )
