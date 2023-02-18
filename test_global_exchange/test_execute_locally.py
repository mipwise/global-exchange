import unittest
from pathlib import Path

import utils

import global_exchange


class TestLocalExecution(unittest.TestCase):

    # def test_action_data_prep(self):
    #     path_data = Path(__file__).parent / 'data' / 'raw_data'
    #     conv_path = path_data / 'conversion_table.csv'
    #     reqs_path = path_data / 'requirements.csv'
    #     dat = global_exchange.preprocess_data(conv_path=conv_path, reqs_path=reqs_path)
    #     utils.check_data(dat, global_exchange.input_schema)
    #     utils.write_data(dat, 'inputs', global_exchange.input_schema)

    def test_2_main_solve(self):
        dat = utils.read_data('inputs', global_exchange.input_schema)
        utils.check_data(dat, global_exchange.input_schema)
        sln = global_exchange.solve(dat)
        utils.write_data(sln, 'outputs', global_exchange.output_schema)

    def test_3_generate_data(self):
        dat = utils.read_data('inputs', global_exchange.input_schema)
        utils.check_data(dat, global_exchange.input_schema)
        utils.write_data(dat, 'testing_data/testing_data.json', global_exchange.input_schema)

if __name__ == '__main__':
    unittest.main()