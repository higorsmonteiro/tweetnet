import os
import sys
import requests

class Collector:
    """Class used to collect tweets using the Twitter API.
    """
    def __init__(self):
        self._key = None
        self._secret_key = None
        self._bearer_token = None

    def process_tokens(self, path_to_file):
        """Read a JSON file with a stricted schema and save tokens for API usage.

        Args:
            path_to_file:
                Absolute path for the JSON file containing the app tokens related to
                the Twitter API. The schema for the json file must follow the structure:
                '{
                    "App": [...]
                }' 

        """
        pass