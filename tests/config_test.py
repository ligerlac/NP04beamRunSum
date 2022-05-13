from os.path import exists
from src import config
from src.utils.misc import non_private_dict


def test_input_files_exist():
    file_names = config.InputFileNames()
    for file_list in non_private_dict(file_names).values():
        _test_input_files_exist(file_list)


def _test_input_files_exist(file_list):
    for file_name in file_list:
        assert exists(file_name)
