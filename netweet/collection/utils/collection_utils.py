import json
import schema
import requests

def tweet_object_fields():
    """Returns a dictionary listing all fields of the tweet object.
    
    Returns:
        tweet_fields:
            dictionary with only one key "tweet_fields" holding a list
            of strings referring all fields of the tweet object provided
            by the Twitter API (v2).
    """
    tweet_fields = { 'twitter_fields': ['id', 'text', 'attachments',
                                        'author_id', 'context_annotations',
                                        'conversation_id', 'created_at',
                                        'entities', 'geo', 'lang', 
                                        'in_reply_to_user_id', 'source',
                                        'public_metrics', 'possibly_sensitive',
                                        'referenced_tweets', 'reply_settings',
                                        'withheld'] }
    return tweet_fields

def validate_apikeys_schema(api_dict):
    """Check if the parsed JSON file satisfies the desired schema.

    Args:
        api_dict:
            Dictionary originated by reading the JSON file.
    
    Returns:
        correct:
            Boolean. 'True' if the schema is correct, 'False' otherwise.
    """
    first_level_schema = schema.Schema({"Apps": list})
    if not first_level_schema.is_valid(api_dict):
        return False
    
    second_level = api_dict["Apps"]
    valid_schema = schema.Schema([{'api_key': str, 'api_secret_key': str, 'bearer_token': str}])
    
    correct = valid_schema.is_valid(second_level)
    return correct

def validate_response(response):
    """Validate the sucess of a HTTP request from the twitter API.

    Args:
        response:
            Response object returned from the HTTP request.

    Returns:
        Boolean value. True if the basic schema is valid. False otherwise.

    Raises:
        AttributeError:
            If the argument 'response' is not a requests.Response type.
    """
    if type(response) != requests.models.Response:
        raise AttributeError("'response' variable type is not a requests.Response type.")

    high_level_schema = schema.Schema({'data': object, 'meta': object})

    response_data = response.json()
    return high_level_schema.is_valid(response_data)
