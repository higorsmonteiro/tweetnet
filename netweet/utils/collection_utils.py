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

