import unittest
from utils import *


class TestUtils(unittest.TestCase):

    def test_url_valid(self):
        self.assertEqual(True, Utils.is_url_valid("https://www.google.com/"))
        self.assertEqual(True, Utils.is_url_valid("https://gitlab.com/IronJulo/project-bikeeper"))
        self.assertEqual(False, Utils.is_url_valid("127.0.0.1"))
        self.assertEqual(False, Utils.is_url_valid("testing http://"))

    def test_get_data(self):
        self.assertEqual(201, Utils.send_data_to_api(
            url="http://127.0.0.1:5000/test/api/users/send/test",
            payload={"Hey": "dfdsfdsf", "df": 5}
        ))
        #self.assertEqual(201, Utils.send_data_to_api("",))


if __name__ == '__main__':
    unittest.main()
