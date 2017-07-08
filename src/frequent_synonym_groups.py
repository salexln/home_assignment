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

class FrequentSynonyms(object):
    def __init__(self, synonyms):
        self._tweet_queue = Queue.Queue()
        self._number_of_top_synonyms = synonyms
        self._word_to_synonym_group = {}

    def _start_tweeter_stream(self):
        listener = StdOutListener(self._tweet_queue)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, listener)

        stream.sample()
        print 'queue size: {}'.format(self._tweet_queue.qsize())

    def start_tweeter_stream_in_thread(self):
        print '*** Staring Twitter stream ***'
        t = threading.Thread(target=self._start_tweeter_stream)
        t.start()

    def get_synonym_group_from_word(self, word):
        synonym_group = []

        if word[0].isalpha():
            synsets = []
            try:
                synsets = wn.synsets(word)
            except Exception:
                synsets = []

            # we use set for word uniqness:
            s = set()
            for synset in synsets:
                s.add(synset.name().split('.')[0].encode('utf-8'))

            if len(s) != 0:
                synonym_group = [x for x in s]
        return synonym_group

    def _add_to_synonym_group(self):
        while self._tweet_queue.qsize() != 0:
            tweet = self._tweet_queue.get()[1]
            for word in tweet:
                synonyms = self.get_synonym_group_from_word(word)

                if len(synonyms) == 0:
                    continue

                # check is the group exists:
                if self._word_to_synonym_group.get(word) is None:
                    # add a new synonym group
                    new_synonym_group = SynonymGroup(synonyms)
                    new_synonym_group.update_appearance(word)
                    # add entries for all words in synonym_group:
                    for w in synonyms:
                        self._word_to_synonym_group[word] = new_synonym_group
                else:
                    # update existing synonym group
                    synonym_group = self._word_to_synonym_group.get(word)
                    synonym_group.update_appearance(word)

    def start_adding_to_synonym_group_thread(self):
        t = threading.Thread(target=self._add_to_synonym_group)
        t.start()


@argh.arg('--synonyms', help='Number of synonyms', type=str, required=True)
def main(**kwargs):

    frequent_synonyms = FrequentSynonyms(int(kwargs['synonyms']))

    frequent_synonyms.start_tweeter_stream_in_thread()
    time.sleep(10)
    frequent_synonyms.start_adding_to_synonym_group_thread()


if __name__ == '__main__':
    parser = argh.ArghParser()
    parser.set_default_command(main)
    parser.dispatch()
