from deduplify.hash_files import filter_dict


def test_filter_dict():
    test_dict = {"hash1": ["filepath1"], "hash2": ["filepath2", "filepath3"]}

    dupdict, undict = filter_dict(test_dict)

    assert dupdict == {"hash2": ["filepath2", "filepath3"]}
    assert undict == {"hash1": "filepath1"}
