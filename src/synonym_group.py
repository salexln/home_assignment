
class SynonymGroup(object):
    def __init__(self, words):
        self._words_appearances = {}

        for word in words:
            self._words_appearances[word] = 0

        self._total_appearances = 0

    def remove_word_appearance(self, word):
        """
        Decreases the appearance by one
        """
        if word in self._words_appearances:
            self._words_appearances[word] -= 1
            self._total_appearances -= 1

            if self._words_appearances[word] < 0:
                raise Exception('We removed {} too many times'.format(word))

    def update_appearance(self, word):
        """
        Incraeses the appearance by one
        """
        if word in self._words_appearances:
            self._words_appearances[word] += 1
            self._total_appearances += 1

    def __eq__(self, other):
        return self._total_appearances == other._total_appearances

    def __lt__(self, other):
        return self._total_appearances < other._total_appearances

    def print_group(self):
        """
        prints all words and their appearance in the group, and total appearances as well
        """
        for word in self._words_appearances:
            print '{}: {}, '.format(word, self._words_appearances[word]),
        print 'Total: {}\n'.format(self._total_appearances)
