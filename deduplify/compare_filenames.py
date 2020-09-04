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


def filter_by_length(dict_to_filter, filter_length=2):
    """Filter a dictionary to return key-value pairs where the value is equal to
    a given length.

    Arguments
    ---------
        dict_to_filter {dict}: The dictionary to be filtered
        filter_length {int}: The length of the values to filter for (default: 2)

    Returns
    -------
        filtered_dict {dict}: The filtered dictionary
    """
    logger.info("Filtering based on length: %s" % filter_length)

    filtered_dict = {
        key: value
        for (key, value) in dict_to_filter.items()
        if len(value) == filter_length
    }

    if len(filtered_dict) == 0:
        logger.info(
            "There are no filenames to compare! Please choose a different filter_length."
        )
        sys.exit()

    return filtered_dict


def compare_filenames(file_list):
    """Compare filenames for equivalence.

    Arguments
    ---------
        file_list {list}: A list of filepaths to be checked

    Returns
    -------
        filepath {str}: In the case when filenames are identical, one filepath
                        is returned to be deleted.
    """
    file_list.sort()  # Sort the list of filepaths alphabetically
    filenames = [filename.split("/")[-1] for filename in file_list]  # Get the filenames
    name_freq = Counter(filenames)  # Count the frequency of the filenames

    if len(name_freq) == 1:
        file_list.remove(max(file_list, key=len))
        return file_list
    else:
        raise ValueError(
            f"The following filenames need investigation.\n{name_freq}\n{file_list}"
        )


def delete_files(files, workers):
    """Delete filepaths

    Arguments
    ---------
        files {list}: List of files to delete
        workers {int}: Number of threads to parallelise over
    """
    logger.info("Deleting files...")
    pbar = tqdm(total=len(files))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(os.remove, filename) for filename in files]
        for future in as_completed(futures):
            pbar.update(1)

    pbar.close()
    logger.info("Deletion complete!")


def run_compare(infile, purge, count):
    """Main function"""

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
    for key, value in tqdm(files.items(), total=len(files)):
        files_to_delete.extend(compare_filenames(value))
    logger.info("Done!")

    logger.info("Number of files that can be safely deleted: %s" % len(files_to_delete))

    if purge:
        delete_files(files_to_delete, count)
