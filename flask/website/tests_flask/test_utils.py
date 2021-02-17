import unittest

from utils import Utils


class TestUtils(unittest.TestCase):

	def test_valid_password(self):
		self.assertEqual(False, Utils.is_valid_password(""))
		self.assertEqual(False, Utils.is_valid_password("motdepasse1"))
		self.assertEqual(False, Utils.is_valid_password("Motdepasse"))
		self.assertEqual(False, Utils.is_valid_password("MOTDEPASSE1"))
		self.assertEqual(False, Utils.is_valid_password("motdepasse"))
		self.assertEqual(False, Utils.is_valid_password("54275242343"))
		self.assertEqual(False, Utils.is_valid_password("MOTDEPASSE"))
		self.assertEqual(True, Utils.is_valid_password("Motdepasse1"))

	def test_valid_email(self):
		print("=" * 70)
		print(Utils.is_valid_email(""))
		print("=" * 70)
		print(Utils.is_valid_email("unemailrandom"))
		print("=" * 70)
		print(Utils.is_valid_email("un.email@random.com"))
		self.assertEqual(False, Utils.is_valid_email(""))
		self.assertEqual(False, Utils.is_valid_email("unemailrandom"))
		self.assertEqual(False, Utils.is_valid_email("1emailrandom"))
		self.assertEqual(False, Utils.is_valid_email("@unemailrandom"))
		self.assertEqual(False, Utils.is_valid_email("unemailrandom@"))
		self.assertEqual(False, Utils.is_valid_email("un.emailrandom.com"))
		self.assertEqual(True, Utils.is_valid_email("un.email@random.com"))

	def test_valid_tel(self):
		self.assertEqual(False, Utils.is_valid_tel(""))
		self.assertEqual(False, Utils.is_valid_tel("zeordeuxzerohuitquarantedeuxvingtcinqdix"))
		self.assertEqual(False, Utils.is_valid_tel("1"))
		self.assertEqual(False, Utils.is_valid_tel("111111111"))
		self.assertEqual(False, Utils.is_valid_tel("11111111111"))
		self.assertEqual(False, Utils.is_valid_tel("111111111u"))
		self.assertEqual(True, Utils.is_valid_tel("0201020304"))

	def test_valid_postal_code(self):
		self.assertEqual(False, Utils.is_valid_postalcode(""))
		self.assertEqual(False, Utils.is_valid_postalcode("quarantecinquemille"))
		self.assertEqual(False, Utils.is_valid_postalcode("45"))
		self.assertEqual(False, Utils.is_valid_postalcode("450000"))
		self.assertEqual(True, Utils.is_valid_postalcode("45000"))


if __name__ == '__main__':
	unittest.main()
