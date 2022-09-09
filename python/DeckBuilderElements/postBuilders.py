import config
import random

class DefaultPostBuilder:
    def execute(self, cards):
        return cards

class DeckShuffler:
    def execute(self, cards):
        shuffled = []
        while len(cards) > 0:
            index = random.randint(0, len(cards) - 1)
            shuffled.append(cards[index])
            cards.pop(index)
        return shuffled

