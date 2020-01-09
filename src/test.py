import unittest
from decode import Application

class TestDecodeMethods(unittest.TestCase):
    def test_decode_pair_case_1(self):
        pair = ['00', '61']
        current_data = []
        app = Application(pair, current_data)
        data = app.decode()
        self.assertEqual(data, ['61'])

    def test_decode_pair_case_1_existed_data(self):
        pair = ['00', '62']
        current_data = ['61']
        app = Application(pair, current_data)
        data = app.decode()
        self.assertEqual(data, ['62'])

    def test_decode_pair_case_2_existed_data(self):
        pair = ['1', '1']
        current_data = ['61']
        app = Application(pair, current_data)
        data = app.decode()
        self.assertEqual(data, ['61'])

    def test_decode_pair_case_2_nonexisted_data(self):
        pair = ['1', '1']
        current_data = []
        app = Application(pair, current_data)
        data = app.decode()
        self.assertEqual(data, ['3F'])

    def test_decode_pair_case_2_valid_range(self):
        pair = ['5', '3']
        current_data = ['61', '62', '63', '64', '65']
        app = Application(pair, current_data)
        data = app.decode()
        self.assertEqual(data, ['61', '62', '63'])

    def test_decode_pair_case_2_invalid_pair_index(self):
        pair = ['1', '2']
        current_data = ['61']
        app = Application(pair, current_data)
        data = app.decode()
        self.assertEqual(data, ['3F'])

    def test_decode_pair_case_2_invalid_data_range(self):
        pair = ['2', '1']
        current_data = ['61']
        app = Application(pair, current_data)
        data = app.decode()
        self.assertEqual(data, ['3F'])

if __name__ == '__main__':
    unittest.main()
