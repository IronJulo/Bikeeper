import re, os
from flask_login import current_user
from hashlib import sha256
import random


class Utils:

	@staticmethod
	def is_valid_password(password):
		"""
        :param: str password, the password we want to check
        :return: boolean, true if valid
        """
		return any(x.isupper() for x in password) and any(x.islower() for x in password) and any(
			x.isdigit() for x in password) and len(password) >= 5

	@staticmethod
	def is_valid_email(email):
		"""
        :param: str email, the email adress we want to check
        :return: boolean, true if valid
        """
		pattern = re.compile('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
		return True if pattern.match(email) is not None else False

	@staticmethod
	def is_valid_tel(tel):
		"""
        :param: str tel, the phone number we want to check
        :return: boolean, true if valid
        """
		pattern = re.compile("^[0-9]{10}$")
		return True if pattern.match(tel) is not None else False

	@staticmethod
	def is_valid_postalcode(pc):
		"""
        :param: str password, the postal code we want to check
        :return: boolean, true if valid
        """
		pattern = re.compile("^[0-9]{5}$")
		return True if pattern.match(pc) is not None else False

	@staticmethod
	def str_collon_to_list(str):
		"""
		:param: str subscription, the subscriptions features to transform in list from ;
		:return: list,
		"""
		return str.split(";")[:-1]  # TODO return True or False

	@staticmethod
	def get_encrypt_password(password):
		encrypt = sha256()
		encrypt.update(password.encode())
		return encrypt.hexdigest()

	@staticmethod
	def is_valid_change_account(password, phonenumber, email, city, street, postalcode):
		if not Utils.is_valid_password(password):
			erreur = "Incorrect password. Password must :\n \
                • contains at least one upper case letter,\n \
                • contains at least one lower case letter,\n \
                • contains at least one number,\n \
                • has a minimal length of 5 characters."
			return (False, erreur)
		elif not Utils.is_valid_tel(phonenumber):
			erreur = "Incorrect phone number format. Please try again."
			return (False, erreur)
		elif not Utils.is_valid_email(email):
			erreur = "Incorrect email format. Please try again."
			return (False, erreur)
		elif city == "" and street == "":
			erreur = "Incomplete address. Please try again."
			return (False, erreur)
		elif not Utils.is_valid_postalcode(postalcode):
			erreur = "Incorrect postal code format. Please try again."
			return (False, erreur)
		else:
			return (True, "Account has been updated!")

	@staticmethod
	def read_prefixes():
		lines = open("./website/prefixes.txt").read().splitlines()
		return "Bikeeper - " + str(random.choice(lines))

	@staticmethod
	def clean_old_image(path):
		"""
		Try to remove old user image when it necessary
		:param: str path: path to remove
		"""

		if "http" in path:
			print("It's an url no need to remove")
		else:
			if os.path.exists(path):
				print("Removing.....")
				os.remove(path)
