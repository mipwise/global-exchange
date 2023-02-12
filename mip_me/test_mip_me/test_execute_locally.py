import unittest
from pathlib import Path

import utils

import mip_me


class TestLocalExecution(unittest.TestCase):

    # def test_action_data_prep(self):
    #     path_data = Path(__file__).parent / 'data' / 'raw_data'
    #     conv_path = path_data / 'conversion_table.csv'
    #     reqs_path = path_data / 'requirements.csv'
    #     dat = mip_me.preprocess_data(conv_path=conv_path, reqs_path=reqs_path)
    #     utils.check_data(dat, mip_me.input_schema)
    #     utils.write_data(dat, 'inputs', mip_me.input_schema)

    def test_3_main_solve(self):
        dat = utils.read_data('inputs', mip_me.input_schema)
        utils.check_data(dat, mip_me.input_schema)
        sln = mip_me.solve(dat)
        utils.write_data(sln, 'outputs', mip_me.output_schema)


if __name__ == '__main__':
    unittest.main()