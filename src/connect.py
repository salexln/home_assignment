import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import timeit
import Queue

"""
Dependencies

- pip install nltk
- nltk.download()   (download all nltk)
- pip install tweepy
"""


class StdOutListener(StreamListener):
    def __init__(self, tweet_queue):
        self._start_time = timeit.default_timer()
        self._number_of_tweets = 0
        self._tweet_queue = tweet_queue

    def on_data(self, data):
        curr_time = timeit.default_timer()
        json_data = json.loads(data)

        if self._is_english(json_data):
            splitted = json_data['text'].split()
            text = [x.encode('utf-8') for x in splitted]

            self._number_of_tweets += 1
            self._tweet_queue.put((curr_time, text))

        return True

    def on_error(self, status):
        print status

    def _is_english(self, json):
        """
        Checks if the tweet is in english
        """
        lang = json.get('lang')
        if lang == u'en':
            return True

        return False
