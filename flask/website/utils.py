import re


class Utils:

    @staticmethod
    def is_valid_password(password):
        return any(x.isupper() for x in password) and any(x.islower() for x in password) and any(
            x.isdigit() for x in password) and len(password) >= 5

    @staticmethod
    def is_valid_email(email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        return re.search(regex, email)

    @staticmethod
    def is_valid_tel(tel):
        pattern = re.compile("(0/91)?[7-9][0-9]{9}")
        return pattern.match(tel)

    @staticmethod
    def is_valid_postalcode(pc):
        pattern = re.compile(r"\s*(\w\d\s*){3}\s*")
        return pattern.match(pc)
