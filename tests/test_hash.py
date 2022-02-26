import os
from collections import defaultdict

from deduplify.hash_files import (
    filter_dict,
    get_total_number_of_files,
    hashfile,
    restart_run,
    transform_dict,
)


def test_filter_dict():
    test_dict = {"hash1": ["filepath1"], "hash2": ["filepath2", "filepath3"]}

    dupdict, undict = filter_dict(test_dict)

    assert dupdict == {"hash2": ["filepath2", "filepath3"]}
    assert undict == {"hash1": "filepath1"}


def test_get_total_number_of_files():
    dirpath = os.path.join("tests", "testdir")

    output1 = get_total_number_of_files(dirpath)
    output2 = get_total_number_of_files(dirpath, file_ext=".txt")

    assert output1 == 2
    assert output2 == 1


def test_hashfile():
    path = os.path.join("tests", "assets", "test_infile.json")

    md5_hash, outpath = hashfile(path)

    assert md5_hash == "f3fb257d843b252bdc0442402552d840"
    assert outpath == path


def test_transform_dict():
    test_dict = {"key1": "value1", "key2": "value2"}
    expected = {"key1": ["value1"], "key2": ["value2"]}

    output = transform_dict(test_dict)

    assert output == expected


def test_restart_run():
    dup_file = os.path.join(os.getcwd(), "tests", "assets", "test_duplicates.json")
    un_file = os.path.join(os.getcwd(), "tests", "assets", "test_uniques.json")

    expected_dict = defaultdict(
        list,
        {
            "key1": ["valueA", "valueB"],
            "key2": ["valueC", "valueD"],
            "key3": ["valueE"],
            "key4": ["valueF"],
        },
    )
    expected_list = ["valueA", "valueB", "valueC", "valueD", "valueE", "valueF"]

    hashes, files_to_be_skipped = restart_run(dup_file, un_file)

    assert hashes == expected_dict
    assert files_to_be_skipped == expected_list
