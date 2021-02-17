import re


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
        return pattern.match(email)

    @staticmethod
    def is_valid_tel(tel):
        """
        :param: str tel, the phone number we want to check
        :return: boolean, true if valid
        """
        pattern = re.compile("^[0-9]{10}$")
        return pattern.match(tel)

    @staticmethod
    def is_valid_postalcode(pc):
        """
        :param: str password, the postal code we want to check
        :return: boolean, true if valid
        """
        pattern = re.compile("^[0-9]{5}$")
        return pattern.match(pc)

    @staticmethod
    def str_collon_to_list(str):
        """
        :param: str subscription, the subscriptions features to transform in list from ;
        :return: list,
        """
        return str.split(";")[:-1]
