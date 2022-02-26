from unittest.mock import call, patch

from deduplify.compare_files import (
    compare_filenames,
    delete_files,
    filter_by_length,
    run_compare,
)


def test_filter_by_length():
    test_dict = {"key1": ["value1"], "key2": ["value2", "value3"]}

    out_dict = filter_by_length(test_dict)

    assert out_dict == {"key2": ["value2", "value3"]}


def test_compare_filenames():
    test_file_list = [
        "path/to/test/file.txt",
        "different/path/to/test/file.txt",
    ]

    out_file_list = compare_filenames(test_file_list)

    assert len(out_file_list) == 1
    assert out_file_list == ["different/path/to/test/file.txt"]


def test_compare_filenames_same_length():
    test_file_list = [
        "path/to/test/file.txt",
        "diff/xy/path/file.txt",
    ]

    out_file_list = compare_filenames(test_file_list)

    assert len(out_file_list) == 1
    assert out_file_list == ["path/to/test/file.txt"]


@patch("deduplify.compare_files.os.remove")
def test_delete_files(mock):
    test_files = ["path/to/file_1.txt", "path/to/file_2.txt"]
    test_calls = [call(filename) for filename in test_files]

    delete_files(test_files, 1)

    assert mock.call_count == len(test_files)
    mock.assert_has_calls(test_calls)


@patch("deduplify.compare_files.os.remove")
def test_run_compare_and_purge(mock):
    infile = "tests/assets/test_infile.json"
    test_calls = [
        call("different/path/to/test/file_1.txt"),
        call("different/path/to/test/file_2.txt"),
    ]

    run_compare(infile, True, 1)

    assert mock.call_count == 2
    mock.assert_has_calls(test_calls)
