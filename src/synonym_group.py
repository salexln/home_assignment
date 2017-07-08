

class WordAppearance(object):
    def __init__(self, word):
        self.word = word
        self.appearance = 0


class SynonymGroup(object):
    def __init__(self, words):
        # holds a tupple of word: num  of appearances
        self._words_appearances = []

        for word in words:
            word = WordAppearance(word)
            self._words_appearances.append(word)

        self._total_appearances = 0

    def total_appearances(self):
        return self._total_appearances

    def words_appearances(self):
        return self._words_appearances

    def remove_word_appearance(self, word):
        for x in self._words_appearances:
            if x.word == word:
                x.appearance -= 1
                if x.appearance < 0:
                    assert ('something is wrong...')
                self._total_appearances -= 1
                break

    def update_appearance(self, word):
        # import pdb; pdb.set_trace()
        for x in self._words_appearances:
            if x.word == word:
                x.appearance += 1

                self._total_appearances += 1
                break

    def __eq__(self, other):
        return self._total_appearances == other._total_appearances

    def __lt__(self, other):
        return self._total_appearances < other._total_appearances

    def print_group(self):
        for word_appearance in self._words_appearances:
            print '{}: {}, '.format(word_appearance.word, word_appearance.appearance),
        print 'Total: {}\n'.format(self._total_appearances)
