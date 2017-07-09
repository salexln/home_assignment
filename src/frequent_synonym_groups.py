from connect import StdOutListener
from synonym_group import SynonymGroup
from tweepy import OAuthHandler
from tweepy import Stream
import Queue
import threading
import time
from nltk.corpus import wordnet as wn
import argparse

access_token = '883627537032785921-S3YvAf4wWX8ZZ2uMsRSecD3CJDYUzbk'
access_token_secret = 'mLNgapLcew5fiZ1FUf6D7wlAivJDpOjZ1eBjv8Di9G6zm'
consumer_key = 'sQenv4drpWaPV4OjLlLnm689u'
consumer_secret = 'GsndjQyrWi7b6WN06AZkXDQxORLpBliCR3ZvoqiYM9ToezVHty'


class FrequentSynonyms(object):
    def __init__(self, synonyms):
        self._tweet_queue = Queue.Queue()
        self._number_of_top_synonyms = synonyms
        self._word_to_synonym_group = {}
        self._synonym_groups = []

    def _start_tweeter_stream(self):
        listener = StdOutListener(self._tweet_queue)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, listener)

        stream.sample()
        print 'queue size: {}'.format(self._tweet_queue.qsize())

    def start_tweeter_stream_in_thread(self):
        """
        Starts new thread that will run the twitter stream
        """
        print '*** Staring Twitter stream ***'
        t = threading.Thread(target=self._start_tweeter_stream)
        t.start()

    def get_synonym_group_from_word(self, word):
        """
        Using WordNet returns the synonym group for a given word
        """
        synonym_group = []

        # we do not want number and words like 'a' and 'I'
        if word[0].isalpha() and len(word) > 1:
            synsets = []
            try:
                synsets = wn.synsets(word)
            except Exception:
                synsets = []

            # we use set for word uniqness:
            s = set(synset.name().split('.')[0].encode('utf-8') for synset in synsets)

            if len(s) != 0:
                synonym_group = [x for x in s]
        return synonym_group

    def _add_to_synonym_group(self):
        """
        Adds the synonym group to the data structure
        """
        while True:
            # this may be faster than the read from Twitter stream, so we need to wait
            if self._tweet_queue.qsize() == 0:
                continue

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

                    self._synonym_groups.append(new_synonym_group)

                    # add entries for all words in synonym_group:
                    for w in synonyms:
                        self._word_to_synonym_group[word] = new_synonym_group
                else:
                    # update existing synonym group
                    synonym_group = self._word_to_synonym_group.get(word)
                    synonym_group.update_appearance(word)

    def start_adding_to_synonym_group_in_thread(self):
        """
        Runs the thread that adds synonym groups to data structure
        """
        t = threading.Thread(target=self._add_to_synonym_group)
        t.start()

    def _find_most_frequent_synonym_groups(self):
        """
        Retruns N nost frequent synonym groups every 2 seconds
        """
        while True:
            time.sleep(2)

            sorted_groups = sorted(self._synonym_groups, reverse=True)

            if len(sorted_groups) > 0:
                print '\n***** Most frequent appearances: *****'
                idx = 0
                while idx < self._number_of_top_synonyms:
                    sorted_groups[idx].print_group()
                    idx += 1

                    # in case the top number is greater than number of groups so far
                    if idx > len(sorted_groups):
                        break

    def find_most_frequent_synonym_groups_in_thread(self):
        """
        Runs the thread that returns N synonym groups
        """
        t = threading.Thread(target=self._find_most_frequent_synonym_groups)
        t.start()


def run(args):
    frequent_synonyms = FrequentSynonyms(int(args.synonyms))
    frequent_synonyms.start_tweeter_stream_in_thread()
    frequent_synonyms.start_adding_to_synonym_group_in_thread()
    frequent_synonyms.find_most_frequent_synonym_groups_in_thread()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parser')
    parser.add_argument('--synonyms', help='Number of synonyms', type=str, required=True)
    args = parser.parse_args()
    run(args)
