import tensorflow as tf
import numpy as np
from config import config

class BaseEncoder:
    def __init__(self, cards):
        self.cards = cards

    def getOneHotEncodedCardByIndex(self, index):
        return self.cardMatrix.arraySync()[index]

    def buildCardMatrix(self, uniqueCards):
        indeces = range(len(uniqueCards))
        matrix = tf.one_hot(indeces, len(uniqueCards))
        return matrix

    def getOneHotEncodedCombinationByIndeces(self, indeces):
        matrix = self.cardMatrix.arraySync()
        oneHots = indeces.map(lambda n: matrix[n])
        return oneHots

    def getCardByOneHotEncoding(self, oneHotCard):
        index = self.cardMatrix.indexOf(oneHotCard)
        return self.uniqueCards[index]

class DamageEncoder(BaseEncoder):
    def __init__(self, cards):
        super().__init__(cards)
        self.uniqueCards = self.getDistinctCardsByAttack(cards)
        self.card_attacks = [n.attack for n in self.uniqueCards]
        self.inputUnits = len(self.uniqueCards)
        self.cardMatrix = self.buildCardMatrix(self.uniqueCards)

    def getDistinctCardsByAttack(self, cards):
        uniqueAttacks = list(set(self.card_attacks))
        uniqueCards = [next((c for c in cards if c.attack == n), None) for n in uniqueAttacks]
        return uniqueCards

    def oneHotEncodeCards(self, cards):
        one_hots = [list(map(lambda n: 1 if n == card.attack else 0, self.card_attacks)) for card in cards]
        return one_hots

    def getIndexOfCard(self, card):
        index = self.card_attacks.indexOf(card.attack)
        return index

    def getIndecesOfCards(self, cards):
        return cards.map(lambda n: self.getIndexOfCard(n))

    def encodeCard(self, card, world):
        return self.oneHotEncodeCards([card])[0]

class DamageAndCostEncoder(DamageEncoder):
    def __init__(self, cards):
        super().__init__(cards)
        self.inputUnits = self.inputUnits + 1 # for cost

    def encodeCard(self, card, world):
        oneHotEncodedTensor = self.oneHotEncodeCards([card])[0]
        budget_weight = world.turnBudget/ config.HERO_BUDGET
        # add budget weight to tensor
        oneHotEncodedTensor = tf.concat([oneHotEncodedTensor, [budget_weight]], 0)
        return oneHotEncodedTensor





