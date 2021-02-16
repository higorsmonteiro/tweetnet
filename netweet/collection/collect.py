import os
import json
import sys
import requests

class Collector:
    """Class used to collect tweets using the Twitter API.
    """
    def __init__(self):
        self._keys = None
        self._secret_keys = None
        self._bearer_tokens = None

        self.db_connector = None
        self.db_cursor = None

    @property
    def keys(self):
        """Set API keys as a read-only property
        """
        return self._keys

    @property
    def secret_keys(self):
        """Set API secret keys as a read-only propery
        """
        return self._secret_keys

    @property
    def bearer_tokens(self):
        """Set API bearer tokens as a read-only property
        """
        return self._bearer_tokens

    def process_tokens(self, path_to_file):
        """Read a JSON file with a stricted schema and save tokens for API usage.

        Args:
            path_to_file:
                Absolute path for the JSON file containing the app tokens related to
                the Twitter API. The schema for the json file must follow the structure:
                '{
                    "Apps": [{"api_key": "...",
                             "api_secret_key": "...",
                             "bearer_token": "..."}, {...}, ..., {...}]
                }'
        Returns:
            No return. Only set the appropriate keys according to the parsed file.
        """
        with open(path_to_file, "r") as f:
            app = json.load(f)

        app_list = app["Apps"]
        self._keys = [ x["api_key"] for x in app_list ]
        self._secret_keys = [ x["api_secret_key"] for x in app_list ]
        self._bearer_tokens = [ x["bearer_token"] for x in app_list ]

    def connect_database(self, db_path="/tmp/example.db"):
        """Connect with the database for tweet storage.

        Args:
            db_path:
                Path to existing database. If the database does not exist, the it will
                be created. If the path is not parsed, then a temporary database 'example.db' 
                will be created at "/tmp/"
        Returns:
            No returns.
        """
        self.db_connector = sqlite3.connect(db_path)
        self.db_connector.close()
