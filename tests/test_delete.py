import os
from unittest.mock import patch, call
from deduplify.del_empty_dirs import empty_dir_search


@patch("deduplify.del_empty_dirs.os.rmdir")
def test_del_empty_dirs(mock):
    test_dir = os.path.join("tests", "testdir_empty")
    test_call = [call(os.path.abspath(test_dir))]

    if not os.path.exists(test_dir):
        os.mkdir(test_dir)

    here = os.path.dirname(__file__)
    empty_dir_search(here)

    assert mock.call_count == 1
    mock.assert_has_calls(test_call)
