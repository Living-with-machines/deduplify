"""
Hash Files
----------

Walk over a directory structure and hash the files within it. Then group
together files that have generated the same hash.

Author: Sarah Gibson
Python version: >=3.7 (developed with 3.8)
Requirements: tqdm

>>> pip install tqdm
"""

import os
import json
import hashlib
import logging
import argparse
from tqdm import tqdm
from collections import defaultdict
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup log config
logging.basicConfig(
    level=logging.DEBUG,
    filename="hash_files.log",
    filemode="a",
    format="[%(asctime)s %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def parse_args():
    """Parse arguments from the command line

    Returns
    -------
        args {Namespace object}: The arguments parsed from the command line
    """
    parser = argparse.ArgumentParser(
        description="Walk a directory structure and hash the files"
    )

    parser.add_argument(
        "dir",
        help="Directory to begin walk from",
    )
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=4,
        help="Number of threads to parallelise over",
    )
    parser.add_argument(
        "--dupfile",
        "-d",
        default="duplicates.json",
        help="Destination file for duplicated hashes. Must be a .json file.",
    )
    parser.add_argument(
        "--unfile",
        "-u",
        default="uniques.json",
        help="Destination file for unique hashes. Must be a .json file.",
    )

    return parser.parse_args()


def walk_dir(dir_to_walk):
    """Walk a directory structure from a given directory

    Arguments
    ---------
        dir_to_walk {str}: The path of the directory to begin walking from

    Returns
    -------
        files {list}: A list of the filepaths contained within dir_to_walk
    """
    logging.info("Walking structure of: %s..." % dir_to_walk)
    files = []  # Empty list to save filepaths to

    # Walk through ROOT_DIR directory structure
    for dirName, subdirs, fileList in tqdm(os.walk(dir_to_walk)):
        for filename in fileList:
            # Create filepath
            filepath = os.path.join(dirName, filename)
            # Append filepath to dict
            files.append(filepath)

    logging.info("Completed!")
    logging.info("Total number of files: %s" % len(files))

    return files


def hashfile(path, blocksize=65536):
    """Calculate the MD5 hash of a given file

    Arguments
    ---------
        path {str, os.path}: Path to the file to generate a hash for
        blocksize {int}: Memory size to read in the file (default: 65536)

    Returns
    -------
        hash {str}: The HEX digest hash of the given file
        path {str}: The filepath that generated the hash
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

    return (hasher.hexdigest(), path)


def generate_hashes(files, workers):
    """Generate MD5 hashes for a list of files (in parallel)

    Arguments
    ---------
        files {list}: Files to generate an MD5 hash for
        workers {int}: Number of threads to parallelise over

    Results
    -------
        hashes {dict}: A dict of the hashes [keys] and files that generated them
                       [values]. Hashes with more than one file in their value
                       list are considered duplicated.
    """
    logging.info("Generating MD5 hashes for files...")
    hashes = defaultdict(list)  # Empty dict to store hashes in

    pbar = tqdm(total=len(files))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(hashfile, filename) for filename in files]
        for future in as_completed(futures):
            hash, filepath = future.result()
            hashes[hash].append(filepath)
            pbar.update(1)

    pbar.close()

    return hashes


def filter_dict(results):
    """Filter a given dictionary into two separate dictionaries based on the
    conditional that the length of the values is either greater than or equal to
    unity.

    Arguments
    ---------
        results {dict}: Dictionary to be filtered

    Results
    -------
        duplicated {dict}: Dictionary where len(values) > 1. Considered to be
                           duplicated hashes.
        unique {dict}: Dictionary where len(values) == 1. Considered to be
                       unique hashes.
    """
    logging.info("Filtering the results...")
    duplicated = {key: value for (key, value) in results.items() if len(value) > 1}
    unique = {key: value[0] for (key, value) in results.items() if len(value) == 1}

    # Calculate number of unique and duplicated files
    logging.info("Number of unique files: %s" % len(unique))

    total = 0
    for key, value in duplicated.items():
        total += len(value)

    logging.info("Number of identical files: %s" % total)

    return duplicated, unique


def dict_to_json_file(filename, dict_content):
    """Write a dictionary to a JSON file

    Arguments
    ---------
        filename {str}: Filename to write to. Must be `.json`.
        dict_content {dict}: Dictionary containing the content to write
    """
    with open(filename, "w") as f:
        f.write(json.dumps(dict_content, indent=2, sort_keys=True))


def main():
    """Main function"""
    args = parse_args()

    # Check the directory path exists
    if not os.path.exists(args.dir):
        raise ValueError("Please provide a known filepath!")

    # Check the output files are JSON type
    for obj in [args.dupfile, args.unfile]:
        if not obj.endswith(".json"):
            raise ValueError("Please provide a JSON filetype for output!")

    # Check that more threads the CPUs have not been requested
    cpus = cpu_count()
    if args.count > cpus:
        raise ValueError(
            "You have requested more threads than are available to this machine. "
            f"This machine has {cpus} CPUs. "
            "Please reduce your value of --count accordingly."
        )

    filepaths = walk_dir(args.dir)  # Collect filepaths
    hashes = generate_hashes(filepaths, args.count)  # Hash the files
    dup_dict, unique_dict = filter_dict(hashes)  # Filter the results

    for filename, content in zip([args.dupfile, args.unfile], [dup_dict, unique_dict]):
        logging.info("Writing outputs to: %s" % filename)
        dict_to_json_file(filename, content)


if __name__ == "__main__":
    main()
