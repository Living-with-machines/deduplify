import os
from deduplify.cli import resolvepath
from deduplify.hash_files import filter_dict, get_total_number_of_files, hashfile


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


def test_hashfile():
    path = os.path.join("tests", "assets", "test_infile.json")

    md5_hash, outpath = hashfile(path)

    assert md5_hash == 'f3fb257d843b252bdc0442402552d840'
    assert outpath == path
