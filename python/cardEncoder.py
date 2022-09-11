import tensorflow as tf
import numpy as np
import config

class BaseEncoder:
    def __init__(self, cards):
        self.cards = cards
        self.getOneHotEncodedCardByIndex = self.getOneHotEncodedCardByIndex.bind(self)

    def getOneHotEncodedCardByIndex(self, index):
        return self.cardMatrix.arraySync()[index]

    def buildCardMatrix(self, uniqueCards):
        indeces = uniqueCards.map(lambda _, i: i)
        iTensor = tf.tensor1d(indeces, 'int32')
        oh = tf.oneHot(iTensor, uniqueCards.length)
        return oh

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
        self.uniqueCards = self.getDistinctCardsByDamage(cards)
        self.inputUnits = self.uniqueCards.length
        self.cardMatrix = self.buildCardMatrix(self.uniqueCards)

    def getDistinctCardsByDamage(self, cards):
        damages = []
        uniqueCards = []
        for i in range(0, len(cards)):
            if damages.indexOf(cards[i].attack) == -1:
                damages.push(cards[i].attack)
                uniqueCards.push(cards[i])
        return uniqueCards

    def oneHotEncodeCards(self, cards):
        damages = self.uniqueCards.map(lambda n: n.attack)
        indeces = cards.map(lambda n: damages.indexOf(n.attack))
        matrix = self.cardMatrix.arraySync()
        oneHots = indeces.map(lambda n: matrix[n])
        return oneHots

    def getIndexOfCard(self, card):
        damages = self.uniqueCards.map(lambda n: n.attack)
        index = damages.indexOf(card.attack)
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
        oh = self.oneHotEncodeCards([card])[0]
        oh.push(world.turnBudget/ config.HERO_BUDGET)
        return oh





