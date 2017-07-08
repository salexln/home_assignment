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
        # import pdb; pdb.set_trace()
        curr_time = timeit.default_timer()
        if (curr_time - self._start_time > 60):
            return False

        json_data = json.loads(data)
        if self._is_english(json_data):
            splitted = json_data['text'].split()
            text = [x.encode('utf-8') for x in splitted]
            # print text
            self._number_of_tweets += 1
            self._tweet_queue.put((curr_time, text))

        return True

    def on_error(self, status):
        print status

    def _is_english(self, json):
        lang = json.get('lang')
        if lang == u'en':
            return True

        return False



if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    # stream.filter(track=['python', 'javascript', 'ruby'])
    stream.sample()

    print 'Total num of tweets {}'.format(listener._number_of_tweets)
