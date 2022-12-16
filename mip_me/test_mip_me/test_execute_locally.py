import unittest
from pathlib import Path

import utils

import mip_me


class TestLocalExecution(unittest.TestCase):

    def test_action_data_prep(self):
        path_data = Path.cwd() / 'mip_me' / 'test_mip_me' / 'data' / 'raw_input'
        conv_path = path_data / 'conversion_table.csv'
        reqs_path = path_data / 'requirements.csv'
        dat = mip_me.data_preprocessing(conv_path=conv_path, reqs_path=reqs_path)
        utils.check_data(dat, mip_me.input_schema)


if __name__ == '__main__':
    unittest.main()