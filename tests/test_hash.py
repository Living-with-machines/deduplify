import os
from deduplify.cli import resolvepath
from deduplify.hash_files import filter_dict, get_total_number_of_files


def test_filter_dict():
    test_dict = {"hash1": ["filepath1"], "hash2": ["filepath2", "filepath3"]}

    dupdict, undict = filter_dict(test_dict)

    assert dupdict == {"hash2": ["filepath2", "filepath3"]}
    assert undict == {"hash1": "filepath1"}


def test_get_total_number_of_files():
    dirpath = resolvepath(os.path.join("tests", "testdir"))
    print(dirpath)

    output1 = get_total_number_of_files(dirpath)
    output2 = get_total_number_of_files(dirpath, file_ext=".txt")

    assert output1 == 2
    assert output2 == 1
