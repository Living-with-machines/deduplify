# deduplify

[![CI](https://github.com/Living-with-machines/deduplify/workflows/CI/badge.svg)](https://github.com/Living-with-machines/deduplify/actions?query=workflow%3ACI)

A Python tool to search for and remove duplicated files in messy datasets.

**Table of Contents:**

- [Overview](#overview)
- [Installation](#installation)
  - [Manual Installation](#manual-installation)
- [Usage](#usage)
  - [Hashing files](#hashing-files)
  - [Comparing files](#comparing-files)
  - [Cleaning up](#cleaning-up)
  - [Global arguments](#global-arguments)
- [Contributing](#contributing)

---

## Overview

`deduplify` is a Python command line tool that will search a directory tree for duplicated files and optionally remove them.
It generates an MD5 hash for each file recursively under a target directory, groups together the filepaths that generate unique and duplicated hashes. When deleting duplicated files, it deletes those deepest in the directory tree first leaving the last present.

## Installation

`deduplify` has a minimum Python requirement of v3.7 but has been developed in v3.8.

### Manual Installation

Begin by cloning this repository and change into it.

```bash
git clone https://github.com/Living-with-machines/deduplify.git
cd deduplify
```

Now run the setup script.
This will install any requirements and the CLI tool into your Python `$PATH`.

```bash
python setup.py install
```

## Usage

`deduplify` has 3 commands: `hash`, `compare` and `clean`.

### Hashing files

The `hash` command takes a path to a target directory as an argument.
It walks the structure of this directory tree and generates MD5 hashes for all files and outputs two JSON files, the names of which can be overwritten using the `--dupfile [-d]` and `--unfile [-u]` flags.

One JSON file contains hashes that are considered "unique" since only one filepath generated this hash.
This file is organised such that the keys are the hashes and the values are the filepaths that generated the hashes.

The second JSON file contains hashes that are considered "duplicated" since more than one filepath generated the same hash.
This file is organised such that the keys are the hashes and the values are a **list** of the filepaths that generated the duplicated hashes.

**Command line usage:**

```bash
usage: deduplify hash [-h] [-c COUNT] [-v] [-d DUPFILE] [-u UNFILE] dir

positional arguments:
  dir                   Path to directory to begin search from

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Number of threads to parallelise over. Default: 1
  -v, --verbose         Print logging messages to the console
  -d DUPFILE, --dupfile DUPFILE
                        Destination file for duplicated hashes. Must be a JSON file. Default: duplicates.json
  -u UNFILE, --unfile UNFILE
                        Destination file for unique hashes. Must be a JSON file. Default: uniques.json
```

### Comparing files

The `compare` command reads in the JSON file of duplicates generated by running `hash`, the name of which can be overwritten using the `--infile [-i]` flag if the data were saved under a different name.
The command runs a check to test if the stem of the filepath are equivalent for all paths that generated a given hash.
This indicates that the file is a true duplication as since both its name and content match.
If they do not match, this implies that the same content is saved under two different filenames.
In this scenario, a `ValueError` is raised and the user is asked to manually investigate these files.

If all the filenames for a given hash match, then the shortest filepath is removed from the list and the rest are returned to be deleted.
To delete files, the user needs to run `compare` with the `--purge` flag set.

A recommended workflow to ensure that all duplicated files have been removed would be as follows:

```bash
deduplify hash target_dir  # First pass at hashing files
deduplify compare --purge  # Delete duplicated files
deduplify hash target_dir  # Second pass at hashing files
deduplify compare          # Compare the filenames again. The code should return nothing to compare
```

**Command line usage:**

```bash
usage: deduplify compare [-h] [-c COUNT] [-v] [-i INFILE] [--purge]

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Number of threads to parallelise over. Default: 1
  -v, --verbose         Print logging messages to the console
  -i INFILE, --infile INFILE
                        Filename to analyse. Must be a JSON file. Default: duplicates.json
  --purge               Deletes duplicated files. Default: False
  ```

### Cleaning up

After purging duplicated files, the target directory may be left with empty sub-directories.
Running the `clean` command will locate and delete these empty subdirs and remove them.

**Command line usage:**

```bash
usage: deduplify clean [-h] [-c COUNT] [-v] dir

positional arguments:
  dir                   Path to directory to begin search from

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Number of threads to parallelise over. Default: 1
  -v, --verbose         Print logging messages to the console
  ```

### Global arguments

The following flags can be passed to any of the commands of `deduplify`.

- `--verbose [-v]`: The flag will print verbose output to the console, as opposed to saving it to the `deduplify.log` file.
- `--count [-c]`: Some processes within `deduplify` can be parallelised over multiple threads when working with larger datasets.
  To do this, include the `--count` flag with the (integer) number of threads you'd like to parallelise over.
  This flag will raise an error if requesting more threads than CPUs available on the host machine.

## Contributing

Thank you for wanting to contribute to `deduplify`! :tada: :sparkling_heart:
To get you started, please read our [Code of Conduct](./CODE_OF_CONDUCT.md) and [Contributing Guidelines](./CONTRIBUTING.md).
