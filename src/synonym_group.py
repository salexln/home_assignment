


class SynonymGroup(object):
    def __init__(self, words):
        # holds a tupple of word: num  of appearances        
        for word in words:
            self._words_appearances.append((word, 1))

        self._total_appearances = len(self._words_appearances)

    def remove_word(self, word):
        for x in self._words_appearances:
            if x.[0] == word:
                x.[1] -= 1
                if x.[1] == 0:
                    self._words_appearances.remove(x)
                self._total_appearances -= 1
                break

    def update_appearance(self, word):
        for x in self._words_appearances:
            if x.[0] == word:
                x[1] += 1

                self._total_appearances += 1
                break
