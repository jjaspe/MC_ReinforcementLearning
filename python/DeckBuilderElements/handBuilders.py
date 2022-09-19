import tensorflow as tf
from models.killable import Killable
from config import config, log
import random

class HAND_BUILDER_TYPES:
    RANDOM= 'RandomHandBuilder'
    N_OF_EACH= 'NOfEachHandBuilder'

class BaseHandBuilder:
    def makeHandBuilder(handBuilderType):
        if handBuilderType == HAND_BUILDER_TYPES.RANDOM:
            return RandomHandBuilder(config.MIN_HERO_ALLY_ATTACK, config.MAX_HERO_ALLY_ATTACK)
        elif handBuilderType == HAND_BUILDER_TYPES.N_OF_EACH:
            return NOfEachHandBuilder(config.MIN_HERO_ALLY_ATTACK, config.MAX_HERO_ALLY_ATTACK)
        else:
            raise Exception('Invalid hand builder type')

class RandomHandBuilder(BaseHandBuilder):
    def __init__(self, minDamage, maxDamage):
        self.minDamage = minDamage
        self.maxDamage = maxDamage
    
    def buildHand(self, deck, handSize):
        hand = []
        for i in range(handSize):
            index = random.randint(0, len(deck) - 1)
            hand.append(deck[index])
            deck.pop(index)
        return hand

class NOfEachHandBuilder(BaseHandBuilder):
    def __init__(self, minDamage, maxDamage):
        self.minDamage = minDamage
        self.maxDamage = maxDamage
    
    def buildHand(self, deck, handSize):
        hand = []
        n = handSize // (self.maxDamage - self.minDamage + 1)
        for i in range(self.minDamage, self.maxDamage + 1):
            card = next((n for n in deck if n.attack == i), None)
            if not card:
                card = Killable('Ally Damage ' + str(i) + ' Cost: ' + str(config.COST), '', 0, i, 0)
            for j in range(n):
                hand.append(card)
        while len(hand) < handSize:
            hand.append(Killable('Ally Damage ' + str(0) + ' Cost: ' + str(config.COST), '', 0, 0, 0))
        return hand

class DrawFromTopOfDeckHandBuilder(BaseHandBuilder):
    def __init__(self, minDamage, maxDamage):
        self.minDamage = minDamage
        self.maxDamage = maxDamage
    
    def buildHand(self, deck, handSize):
        hand = []
        while len(hand) < handSize:
            card = deck.pop(0)
            if card.attack >= self.minDamage and card.attack <= self.maxDamage:
                hand.append(card)
            else:
                hand.append(Killable('Ally Damage ' + str(0) + ' Cost: ' + str(config.COST), '', 0, 0, 0))
                deck.append(card)
        return hand




