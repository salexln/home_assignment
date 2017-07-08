import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


access_token = ''
access_token_secret = ''
consumer_key = ''
consumer_secret = ''

"""
Dependencies

- pip install nltk
- nltk.download()   (download all nltk)
- pip install tweepy
"""


class StdOutListener(StreamListener):

    def on_data(self, data):
        print '*'*50
        # print data
        json_data = json.loads(data)
        if self._is_english(json_data):
            splitted = json_data['text'].split()
            text = [x.encode('utf-8') for x in splitted]
            print text

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
