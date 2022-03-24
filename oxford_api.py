"""
Describe imports
"""
import os
from os import path
import requests

if path.exists("env.py"):
    import env


class OxfordDictAPI:
    """
    This class handles the communication with the Oxford Dictionaries API
    The API is used to ensure the user guess is an actual word in the Oxford
    Dictionary.
    """

    def __init__(self):
        self.load_api_credentials()
        self.base_url = "https://od-api.oxforddictionaries.com/api/v2"
        self.headers = {"app_id": self.app_id, "app_key": self.app_key}

    def check_in_dict(self, guess):
        """
        Look up the user guess in Oxford English Dictionary.
        Return the status code.
        """
        url = self.base_url + "/entries/en-gb/" + guess.lower()
        api_response = requests.get(url, headers=self.headers)
        return api_response.status_code

    def load_api_credentials(self):
        """
        Get API credentials from env.py file.
        """
        self.app_id = os.environ["OXFORD_API_APP_ID"]
        self.app_key = os.environ["OXFORD_API_APP_KEY"]
