import unittest
import requests


def post(url, data):
	headers = {
		'Content-type': 'application/json',
	}
	# data = '{"text":"Hello, World!"}'
	response = requests.post(url, headers=headers, data=data)
	# TODO :


class TestUtils(unittest.TestCase):

	def test_api(self):
		self.assertEqual(False, "")


if __name__ == '__main__':
	unittest.main()
