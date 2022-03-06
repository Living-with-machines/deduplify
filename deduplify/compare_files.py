"""
Compare Filenames
-----------------

Ascertain whether files that share the same hash also share the same filename,
thereby being identical beyond reasonable doubt. Requires hash_files.py to
already have been executed. Using the --purge option will delete the duplicated
files.

Python version: >= 3.7 (developed with 3.8)
Packages: tqdm

>>> pip install tqdm
"""

import logging
import os
import warnings
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import jmespath
from tinydb import TinyDB, where
from tqdm import tqdm

logger = logging.getLogger()


def identify_unique_hashes(db) -> list:
    """Generate a list of unique hashes from a TinyDB database object

    Args:
        db (TinyDB database): The TinyDB database object to parse for hashes

    Returns:
        list: A list of the unique hashes contained within the database.
    """
    all_hashes = [row["hash"] for row in db.all() if row["duplicate"]]
    return list(set(all_hashes))


def compare_filenames(hash: str, db) -> list:
    """Compare filenames for equivalence for a given hash.

    Args:
        hash (str): The hash for which to compare the filepaths for.
        db (TinyDB database): A TinyDB database object that contains the hash and
            filepath information to analyse.

    Returns:
        file_list (list): In the case when filenames are identical, the
            shortest filepath is removed from the list and the rest are returned to be
            deleted. In the case where the filenames are not identical but,
            coincidentally, the same length, then the first filepath in the list is
            removed and the rest are returned to be deleted.
    """
    expression = jmespath.compile("[*].filepath")
    files_with_matching_hash = db.search(where("hash").matches(hash))

    file_list = expression.search(files_with_matching_hash)
    file_list.sort()  # Sort the list of filepaths alphabetically

    filenames = [
        os.path.basename(filename) for filename in file_list
    ]  # Get the filenames
    name_freq = Counter(filenames)  # Count the frequency of the filenames

    if len(name_freq) == 1:
        file_list.remove(min(file_list, key=len))
    elif (len(name_freq) > 1) and (list(set(file_list)) == 1):
        # there are multiple filepaths that are different,
        # but, by coincidence, have the same length
        file_list.remove(file_list[0])
    else:
        # Hashes are same but filenames are different
        warnings.warn(
            "The following filenames need investigation.\n- " + "\n- ".join(file_list)
        )

    return file_list


def delete_files(files: list, workers: int):
    """Delete filepaths

    Args:
        files (list): List of files to delete
        workers (int): Number of threads to parallelise over
    """
    logger.info("Deleting files...")
    pbar = tqdm(total=len(files))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(os.remove, filename) for filename in files]
        for _ in as_completed(futures):
            pbar.update(1)

    pbar.close()
    logger.info("Deletion complete!")


def run_compare(infile: str, purge: bool, count: int, **kwargs):
    """Compare files for duplicated hashes

    Args:
        infile (str): JSON location of filepaths and hashes
        purge (bool): Delete duplicated files
        count (int): Number of threads to parallelise over
    """
    logger.info("Loading in file: %s" % infile)
    db = TinyDB(infile)

    # Find the unique hashes
    hashes = identify_unique_hashes(db)

    # Determine which filenames should be deleted
    files_to_delete = []
    logger.info("Comparing filenames...")
    for hash in hashes:
        files_to_delete.extend(compare_filenames(hash, db))
    logger.info("Done!")

    logger.info("Number of files that can be safely deleted: %s" % len(files_to_delete))

    if purge:
        delete_files(files_to_delete, count)
