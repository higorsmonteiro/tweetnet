import json
import schema

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
                                        'non_public_metrics', 'public_metrics',
                                        'organic_metrics', 'possible_sensitive',
                                        'referenced_tweets', 'reply_settings',
                                        'withheld'] }
    return tweet_fields

def check_apikeys_schema(api_dict):
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


