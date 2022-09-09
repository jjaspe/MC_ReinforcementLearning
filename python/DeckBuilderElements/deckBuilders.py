import math
import config
from models.classes import Ally
from models.hero import Hero
from models.boss import Boss
from handBuilders import BaseHandBuilder, HAND_BUILDER_TYPES

class BaseDeckBuilder:
    def __init__(self):
        pass

    def buildCards(self):
        pass

    def buildFullDeck(self, cards, deckSize):
        deck = []
        for i in range(deckSize):
            deck.append(cards[i % len(cards)])
        return deck

    def buildDeck(self, deckSize):
        cards = self.buildCards()
        return self.buildFullDeck(cards, deckSize)

    def makeHero(self):
        return Hero('Hero', '', config.HERO_HEALTH, 0, 0, config.HERO_ATTACK, None)

    def makeBoss(self):
        return Boss('Boss', '', config.BOSS_HEALTH, config.BOSS_ATTACK, config.BOSS_SCHEME)

class DamageOnlyDeckBuilder(BaseDeckBuilder):
    def __init__(self, minDamage, maxDamage):
        super().__init__()
        self.minDamage = minDamage
        self.maxDamage = maxDamage

    def buildCards(self):
        cards = []
        for i in range(self.minDamage, self.maxDamage + 1):
            ally = Ally('Ally Damage ' + str(i), '', 0, i, 0)
            cards.append(ally)
        return cards

class DamageAndCostDeckBuilder(BaseDeckBuilder):
    def __init__(self, minDamage, maxDamage, minCost, maxCost):
        super().__init__()
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.minCost = minCost
        self.maxCost = maxCost

    def buildCards(self):
        cards = []
        for i in range(self.minDamage, self.maxDamage + 1):
            cost = math.min(self.maxCost, math.max(self.minCost, math.floor(i / 2)))
            ally = Ally('Ally Damage ' + str(i) + ' Cost: ' + str(cost), '', 0, i, 0)
            ally.cost = cost
            cards.append(ally)
        return cards

class DamageAndSquaredCostDeckBuilder(BaseDeckBuilder):
    def __init__(self, minDamage, maxDamage, minCost, maxCost):
        super().__init__()
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.minCost = minCost
        self.maxCost = maxCost

    def buildCards(self):
        cards = []
        for i in range(self.minDamage, self.maxDamage + 1):
            cost = math.min(self.maxCost, math.max(self.minCost, math.floor(i**2 / 2)))
            ally = Ally('Ally Damage ' + str(i) + ' Cost: ' + str(cost), '', 0, i, 0)
            ally.cost = cost
            cards.append(ally)
        return cards


class DamageAndCustomCostDeckBuilder(BaseDeckBuilder):
    def __init__(self, minDamage, maxDamage, costFunction):
        super().__init__()
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.costFunction = costFunction

    def buildCards(self):
        cards = []
        for i in range(self.minDamage, self.maxDamage + 1):
            if(i == 0):
                cost = 0
            elif(i == 1):
                cost = 1
            elif(i == 2):
                cost = 1
            elif(i == 3):
                cost = 2
            elif(i == 4):
                cost = 3
            elif(i == 5):
                cost = 3
            elif(i == 6):
                cost = 4
            else:
                cost = self.maxCost
            ally = Ally('Ally Damage ' + str(i) + ' Cost: ' + str(cost), '', 0, i, 0)
            ally.cost = cost
            cards.append(ally)
        return cards

    def buildFullDeck(self, cards, deckSize):
        deck = []
        attacks = [i.attack for i in cards]
        # remove dupes from attacks
        attacks = list(dict.fromkeys(attacks))
        cardsPerAttack = deckSize // len(attacks)
        for i in range(cardsPerAttack):
            for attack in attacks:
                # find card with attack
                for card in cards:
                    if(card.attack == attack):
                        deck.append(card)
                        break

        # fill out the rest of the deck with 0 attack cards
        zeroAttackCard = [card for card in cards if card.attack == 0][0]
        for i in range(deckSize - len(deck)):
            deck.append(zeroAttackCard.copy())

        return deck

class NormalizedDamageAndSquaredCostDeckBuilder(BaseDeckBuilder):
    def __init__(self, minDamage, maxDamage, minCost, maxCost):
        super().__init__()
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.minCost = minCost
        self.maxCost = maxCost
        self.scale = 100

    def buildCards(self):
        cards = []
        for i in range(self.minDamage, self.maxDamage + 1):
            cost = math.min(self.maxCost, math.max(self.minCost, math.floor(i / 2)))
            ally = Ally('Ally Damage ' + str(i) + ' Cost: ' + str(cost), '', 0, i/self.scale, 0)
            ally.cost = cost
            cards.append(ally)
        return cards

    def makeHero(self):
        return Hero('Hero', '', config.HERO_HEALTH, 0, 0, config.HERO_ATTACK/self.scale, None)

    def makeBoss(self):
        return Boss('Boss', '', config.BOSS_HEALTH, config.BOSS_ATTACK/self.scale, config.BOSS_SCHEME)

DECK_BUILDER_TYPES = {
    'DamageOnly': DamageOnlyDeckBuilder,
    'DamageAndCost': DamageAndCostDeckBuilder,
    'DamageAndSquaredCost': DamageAndSquaredCostDeckBuilder,
    'DamageAndCustomCost': DamageAndCustomCostDeckBuilder,
    'NormalizedDamageAndSquaredCost': NormalizedDamageAndSquaredCostDeckBuilder
}





