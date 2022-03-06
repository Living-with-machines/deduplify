import os

from tinydb import TinyDB

from deduplify.hash_files import hashfile, restart_run


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
