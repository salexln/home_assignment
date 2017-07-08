
import argh
from connect import StdOutListener
from synonym_group import SynonymGroup
from tweepy import OAuthHandler
from tweepy import Stream
import Queue
import threading
import time
from nltk.corpus import wordnet as wn

access_token = '883627537032785921-S3YvAf4wWX8ZZ2uMsRSecD3CJDYUzbk'
access_token_secret = 'mLNgapLcew5fiZ1FUf6D7wlAivJDpOjZ1eBjv8Di9G6zm'
consumer_key = 'sQenv4drpWaPV4OjLlLnm689u'
consumer_secret = 'GsndjQyrWi7b6WN06AZkXDQxORLpBliCR3ZvoqiYM9ToezVHty'


# def add_to_structure(words):



def get_tweeter_stream(tweet_queue):
    listener = StdOutListener(tweet_queue)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    stream.sample()
    print 'queue size: {}'.format(tweet_queue.qsize())


def get_tweeter_stream_in_thread(tweet_queue):
    t = threading.Thread(target=get_tweeter_stream, kwargs={'tweet_queue':tweet_queue})
    t.start()

def add_to_synonym_group(tweet_queue):
    # import pdb; pdb.set_trace()
    print 'bbb'
    while tweet_queue.qsize() != 0:
        print 'aaa'
        tweet = tweet_queue.get()
        print tweet
    #
    # for word in tweet:
    #     synsets = wordnet.synsets(test)
    #     s = set()
    #     for synset in synsets:
    #         s.add(synset.name().split('.')[0].encode('utf-8')
        # print s

@argh.arg('--synonyms', help='Number of synonyms', type=str, required=True)
def main(**kwargs):
    # print int(kwargs['synonyms'])
    tweet_queue = Queue.Queue()
    # print 'Starting tweeter stream'
    get_tweeter_stream_in_thread(tweet_queue)
    time.sleep(10)
    # print 'Tweeter stream is done, read {} tweets'.format(tweet_queue.qsize())

    t = threading.Thread(target=add_to_synonym_group, kwargs={'tweet_queue':tweet_queue})
    t.start()




    # words_to_groups = {}


if __name__ == '__main__':
    parser = argh.ArghParser()
    parser.set_default_command(main)
    parser.dispatch()
