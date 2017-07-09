import threading


class SynonymGroup(object):
    def __init__(self, words):
        self._words_appearances = {}

        for word in words:
            self._words_appearances[word] = 0

        self._total_appearances = 0
        self._lock = threading.Lock()

    def remove_word_appearance(self, word):
        self._lock.acquire()
        """
        Decreases the appearance by one
        """
        try:
            if word in self._words_appearances and self._words_appearances[word] > 0:
                self._words_appearances[word] -= 1
                self._total_appearances -= 1
        finally:
            self._lock.release()

    def update_appearance(self, word):
        self._lock.acquire()
        """
        Incraeses the appearance by one
        """
        try:
            if word in self._words_appearances:
                self._words_appearances[word] += 1
                self._total_appearances += 1
        finally:
            self._lock.release()

    @property
    def total_appearances(self):
        total_appearances = 0
        self._lock.acquire()
        total_appearances = self._total_appearances
        self._lock.release()
        return total_appearances

    def __eq__(self, other):
        return self.total_appearances == other.total_appearances

    def __lt__(self, other):
        return self.total_appearances < other.total_appearances

    def print_group(self):
        self._lock.acquire()
        """
        prints all words and their appearance in the group, and total appearances as well
        """
        for word in self._words_appearances:
            print '{}: {}, '.format(word, self._words_appearances[word]),
        print 'Total: {}\n'.format(self._total_appearances)
        self._lock.release()
