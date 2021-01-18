import requests
import validators


class Utils:
    """
    Useful and common functions
    """

    @staticmethod
    def is_url_valid(url):
        """
        :param url: Url to check
        :type url: str
        :return: If url is an url True , else False
        :rtype: boolean
        """
        valid = validators.url(url)
        if valid:
            return True
        else:
            print("Invalid url")
            return False

    @staticmethod
    def send_data_to_api(url, payload):
        """
        Send Post data to API
        :param url: The first number to add
        :param payload: The second number to add
        :type url: str
        :type payload: dict
        :return: The HTTP Status code
        :rtype: int
        """
        if Utils.is_url_valid(url):
            r = requests.post(url, data=payload)
            return r.status_code

    @staticmethod
    def get_data_from_api(url):
        """
         Get data from API
        :param url: The first number to add
        :type url: str
        :rtype: dict
        """
        return requests.get(url).json()
