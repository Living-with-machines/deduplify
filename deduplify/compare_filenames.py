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
import argparse
from tqdm import tqdm
from collections import Counter
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup log config
logging.basicConfig(
    level=logging.DEBUG,
    filename="compare_filenames.log",
    filemode="a",
    format="[%(asctime)s %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def parse_args():
    """Parse arguments from the command line

    Returns
    -------
        args {Namespace obj}: The arguments parsed from the command line
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--infile",
        "-i",
        default="duplicates.json",
        help="Filename to analyse. Must be a .json file",
    )
    parser.add_argument(
        "--length",
        "-l",
        type=int,
        default=2,
        help="Length of values to filter by",
    )
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=4,
        help="Number of threads to parallelise over",
    )
    parser.add_argument(
        "--purge",
        action="store_true",
        help="If used, files WILL be deleted",
    )

    return parser.parse_args()


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
    logging.info("Filtering based on length: %s" % filter_length)

    filtered_dict = {
        key: value
        for (key, value) in dict_to_filter.items()
        if len(value) == filter_length
    }

    if len(filtered_dict) == 0:
        logging.info(
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
    file_lengths = [len(filename) for filename in file_list]  # Get the string lengths
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
    logging.info("Deleting files...")
    pbar = tqdm(total=len(files))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(os.remove, filename) for filename in files]
        for future in as_completed(futures):
            pbar.update(1)

    pbar.close()
    logging.info("Deletion complete!")


def main():
    """Main function"""
    args = parse_args()

    if not args.infile.endswith(".json"):
        raise ValueError("Please provide a JSON input file!")

    cpus = cpu_count()
    if args.count > cpus:
        raise ValueError(
            "You have requested more threads than are available to this machine. "
            f"This machine has {cpus} CPUs. "
            "Please reduce your value of --count accordingly."
        )

    # Load the file into a dictionary
    logging.info("Loading in file: %s" % args.infile)
    with open(args.infile, "r") as stream:
        files = json.load(stream)
    logging.info("Done!")

    # Filter the dictionary
    files = filter_by_length(files, filter_length=args.length)
    logging.info("Number of files to compare: %s" % (args.length * len(files)))

    # Determine which filenames are duplicated
    files_to_delete = []
    logging.info("Comparing filenames...")
    for key, value in tqdm(files.items(), total=len(files)):
        files_to_delete.extend(compare_filenames(value))
    logging.info("Done!")

    logging.info(
        "Number of files that can be safely deleted: %s" % len(files_to_delete)
    )

    if args.purge:
        delete_files(files_to_delete, args.count)


if __name__ == "__main__":
    main()
