
import argh
from connect import StdOutListener
from tweepy import OAuthHandler
from tweepy import Stream
import Queue


access_token = '883627537032785921-S3YvAf4wWX8ZZ2uMsRSecD3CJDYUzbk'
access_token_secret = 'mLNgapLcew5fiZ1FUf6D7wlAivJDpOjZ1eBjv8Di9G6zm'
consumer_key = 'sQenv4drpWaPV4OjLlLnm689u'
consumer_secret = 'GsndjQyrWi7b6WN06AZkXDQxORLpBliCR3ZvoqiYM9ToezVHty'


def add_to_structure(words):
    

def connect_to_tweeter():
    #This handles Twitter authetification and the connection to Twitter Streaming API
    tweet_queue = Queue.Queue()
    listener = StdOutListener(tweet_queue)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    # stream.filter(track=['python', 'javascript', 'ruby'])
    stream.sample()

    # print 'Total num of tweets {}'.format(listener._number_of_tweets)
    print 'queue size: {}'.format(tweet_queue.qsize())


@argh.arg('--synonyms', help='Number of synonyms', type=str, required=True)
def main(**kwargs):
    # print int(kwargs['synonyms'])
    connect_to_tweeter()

if __name__ == '__main__':
    parser = argh.ArghParser()
    parser.set_default_command(main)
    parser.dispatch()
