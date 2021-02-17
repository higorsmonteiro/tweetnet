import os
import json
import sys
import sqlite3
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

    def get_bearer_header(self, app_index=0):
        """Return a dictionary formatted with the bearer token authorization.

        Args:
            app_index:
                The list index of the app list containing the authorization keys.
        Returns:
            Header dictionary to be used for 2.0 Authorization requests.
        Raises:
            BadAppIndexError:
                If the index of the app is negative or larger than the number of 
                existing apps.
        """
        if app_index > len(self._bearer_tokens)-1 or app_index < 0:
            raise BadAppIndexError("Bad value for the app index")

        return {"Authorization": f"Bearer {self._bearer_tokens[app_index]}"}

    def collect_data(self, search_query=None, app_index=0):
        """Make a HTTP request to collect tweets according the search string given.

        Args:
            search_string:
                String storing the search request. It can contains all operators allowed
                by the Twitter API.
        Return:
            response:
                Response object returned from the HTTP request on the Twitter API.
        Raises:
            AttributeError:
                If no query is given as argument for :search_query:
        """
        tweet_fields = "tweet.fields=author_id" # CHANGE
        if search_query is None:
            raise AttributeError("No query parsed.")

        url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
            search_query, tweet_fields
        )
        headers = self.get_bearer_header(app_index)
        response = requests.get(url, headers=headers)
        return response # FIX

    # CREATE A UTILS FUNCTION TO CHECK IF A RESPONSE IS SUCESSFUL.



class BadAppIndexError(Exception):
    pass