import math
from classes import Ally
import random
import config

class World:
    def __init__(self, cards, hero, boss, heroDeck, bossDeck):
        self.cards = cards
        self.hero = hero
        self.boss = boss
        self.heroDeck = heroDeck
        self.bossDeck = bossDeck
        self.heroHand = []
        self.attackCards = []
        self.discarded = []
        self.endPlayerTurn = False

    def intializeAlly(self):
        card2 = Ally('Card', '', 1, random.randint(0, config.HAND_SIZE), random.randint(0, config.HAND_SIZE))
        card2.cost = math.floor(card2.attack / config.COST_DIVISOR)
        return card2

    def makeHand(self, handSize, deckCards):
        hand = []
        for x in range(handSize):
            hand.append(deckCards.pop())
        return hand

