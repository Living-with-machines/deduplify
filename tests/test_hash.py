import os
from tempfile import NamedTemporaryFile

from tinydb import TinyDB

from deduplify.hash_files import (
    get_total_number_of_files,
    hashfile,
    identify_duplicates,
    restart_run,
)


def test_get_total_number_of_files():
    dirpath = os.path.join("tests", "testdir")

    output1 = get_total_number_of_files(dirpath)
    output2 = get_total_number_of_files(dirpath, file_ext="txt")

    assert output1 == 3
    assert output2 == 1


def test_hashfile():
    path = os.path.join("tests", "assets", "test_infile.json")

    md5_hash, outpath = hashfile(path)

    assert md5_hash == "f3fb257d843b252bdc0442402552d840"
    assert outpath == path


def test_restart_run():
    test_db = TinyDB(os.path.join("tests", "assets", "test_db.json"))

    expected_list = ["file.txt", "file.txt", "file.txt"]

    files_to_be_skipped = restart_run(test_db)

    assert files_to_be_skipped == expected_list


def test_identify_duplicates():
    with NamedTemporaryFile("w") as test_f, NamedTemporaryFile("w") as expected_f:
        test_db = TinyDB(test_f.name)
        expected_db = TinyDB(expected_f.name)

    test_db.insert_multiple(
        [
            {"hash": "hash1", "filepath": "file1.txt"},
            {"hash": "hash1", "filepath": "file2.txt"},
        ]
    )
    expected_db.insert_multiple(
        [
            {"hash": "hash1", "filepath": "file1.txt", "duplicate": True},
            {"hash": "hash1", "filepath": "file2.txt", "duplicate": True},
        ]
    )
    updated_db = identify_duplicates(test_db)

    assert expected_db.all() == updated_db.all()
