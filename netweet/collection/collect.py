import os
import json
import sys
import sqlite3
import requests
import netweet.collection.utils as utils # fix

class Collector:
    """Class used to collect tweets using the Twitter API.
    """
    def __init__(self):
        self.number_apps = None
        self._keys = None
        self._secret_keys = None
        self._bearer_tokens = None

        self.db_connector = None
        self.db_cursor = None
        self.db_path = None

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

        # Validate the schema of the API KEYS file.
        if not utils.validate_apikeys_schema(app):
            raise BadSchemaError("""The schema of the file containing the keys does not 
                                  follow the required schema.""")
        
        app_list = app["Apps"]
        self._keys = [ x["api_key"] for x in app_list ]
        self._secret_keys = [ x["api_secret_key"] for x in app_list ]
        self._bearer_tokens = [ x["bearer_token"] for x in app_list ]
        self.number_apps = len(self._keys)

    def connect_database(self, db_path="/tmp/example.db"):
        """Connect with the database for tweet storage.

        Args:
            db_path:
                Path to existing database. If the database does not exist, then it will
                be created. If the path is not parsed, then a temporary database 'example.db' 
                will be created at "/tmp/"
        Returns:
            No returns.
        """
        self.db_path = db_path
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

    def request_data(self, search_query=None, app_index=0):
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
        tweet_obj_fields = utils.tweet_object_fields()
        tweet_fields = ','.join(tweet_obj_fields["twitter_fields"])
        params = {'query': search_query, 
                  'tweet.fields': tweet_fields}

        if search_query is None:
            raise AttributeError("No query parsed.")

        base_url = "https://api.twitter.com/2/tweets/search/recent?"
        headers = self.get_bearer_header(app_index)
        response = requests.get(base_url, headers=headers, params=params)
        return response

    def collect(self, query_list):
        """Pass a list of search queries to make a continuous collection of 
        tweets for each one.

        """
        try:
            while True:
                # For each app, we iterate through the query list and make the API request.
                for current_app in range(self.number_apps):
                    for q_index, current_query in enumerate(query_list):
                        response = self.request_data(search_query=current_query, app_index=current_app)
                        if utils.validate_response(response):
                            # STORE DATA
                            data = response.json()
                            print(data.keys())
                            #pass
                        else:
                            raise BadResponseError()
        except KeyboardInterrupt:
            return -1
        except BadResponseError:
            return -1


# Exceptions
class BadAppIndexError(Exception):
    pass

class BadSchemaError(Exception):
    pass

class BadResponseError(Exception):
    pass