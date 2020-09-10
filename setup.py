import io
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Package meta-data.
AUTHOR = "Sarah Gibson"
DESCRIPTION = (
    "A Python package to search for and remove duplicated files in messy datasets"
)
EMAIL = "sgibson@turing.ac.uk"
LICENSE = "MIT"
LICENSE_TROVE = "License :: OSI Approved :: MIT License"
NAME = "deduplify"
REQUIRES_PYTHON = ">=3.7.0"
URL = "https://github.com/Living-with-Machines/deduplify"
VERSION = None

# What packages are required for this module to be executed?
with open(os.path.join(here, "requirements.txt"), "r") as f:
    required = [line.strip("\n") for line in f.readlines()]

REQUIRED = required + ["incremental"]
full_require = []
docs_require = []
test_require = full_require + ["pytest", "coverage"]
dev_require = ["incremental"]

# What packages are optional?
EXTRAS = {
    "full": full_require,
    "docs": docs_require,
    "tests": test_require,
    "dev": docs_require + test_require + dev_require,
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!
#
# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Where the magic happens:
setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license=LICENSE,
    ext_modules=[],
    entry_points={"console_scripts": ["deduplify = deduplify.cli:main"]},
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        LICENSE_TROVE,
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    use_incremental=True,
    setup_requires=["incremental"],
)
