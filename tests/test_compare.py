import os

from unittest.mock import call, patch

from tinydb import TinyDB

from deduplify.compare_files import (
    compare_filenames,
    delete_files,
    run_compare,
)


def test_compare_filenames():
    test_db = TinyDB(os.path.join("tests", "assets", "test_db.json"))

    out_file_list = compare_filenames("test_hash", test_db)

    assert len(out_file_list) == 2
    assert out_file_list == ["different/path/to/test/file.txt", 'path/to/test/file.txt']


def test_compare_filenames_same_length():
    test_db = TinyDB(os.path.join("tests", "assets", "test_db.json"))

    out_file_list = compare_filenames("test_hash", test_db)

    assert len(out_file_list) == 2
    assert out_file_list == ['different/path/to/test/file.txt', "path/to/test/file.txt"]


@patch("deduplify.compare_files.os.remove")
def test_delete_files(mock):
    test_files = ["path/to/file_1.txt", "path/to/file_2.txt"]
    test_calls = [call(filename) for filename in test_files]

    delete_files(test_files, 1)

    assert mock.call_count == len(test_files)
    mock.assert_has_calls(test_calls)


@patch("deduplify.compare_files.os.remove")
def test_run_compare_and_purge(mock):
    infile = "tests/assets/test_db.json"
    test_calls = [
        call('different/path/to/test/file.txt'),
        call("path/to/test/file.txt"),
    ]

    run_compare(infile, True, 1)

    assert mock.call_count == 2
    mock.assert_has_calls(test_calls)
