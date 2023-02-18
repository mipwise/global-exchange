import unittest
from pathlib import Path

import utils

import global_exchange


class TestLocalExecution(unittest.TestCase):

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