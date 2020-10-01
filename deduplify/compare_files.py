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

import os
import sys
import json
import logging
from tqdm import tqdm
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger()


def filter_by_length(dict_to_filter: dict) -> dict:
    """Filter a dictionary to return key-value pairs where the value's length is
    greater than 1.

    Args:
        dict_to_filter (dict): The dictionary to be filtered

    Returns:
        filtered_dict (dict): The filtered dictionary
    """
    filtered_dict = {
        key: value for (key, value) in dict_to_filter.items() if len(value) > 1
    }

    if len(filtered_dict) == 0:
        logger.info("There are no filenames to compare!")
        sys.exit()

    return filtered_dict


def compare_filenames(file_list: list) -> str:
    """Compare filenames for equivalence.

    Args:
        file_list (list): A list of filepaths to be checked

    Returns:
        file_list (list): In the case when filenames are identical, the
                          shortest filepath is removed from the list and the
                          rest are returned to be deleted.
    """
    file_list.sort()  # Sort the list of filepaths alphabetically
    filenames = [
        os.path.basename(filename) for filename in file_list
    ]  # Get the filenames
    name_freq = Counter(filenames)  # Count the frequency of the filenames

    if len(name_freq) == 1:
        file_list.remove(min(file_list, key=len))
        return file_list
    else:
        raise ValueError(
            f"The following filenames need investigation.\n{name_freq}\n{file_list}"
        )


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
        count (int): Number of threadsto parallelise over
    """
    # Load the file into a dictionary
    logger.info("Loading in file: %s" % infile)
    with open(infile, "r") as stream:
        files = json.load(stream)
    logger.info("Done!")

    # Filter the dictionary
    files = filter_by_length(files)
    logger.info("Number of files to compare: %s" % (len(files)))

    # Determine which filenames are duplicated
    files_to_delete = []
    logger.info("Comparing filenames...")
    for value in tqdm(files.values(), total=len(files)):
        files_to_delete.extend(compare_filenames(value))
    logger.info("Done!")

    logger.info("Number of files that can be safely deleted: %s" % len(files_to_delete))

    if purge:
        delete_files(files_to_delete, count)
