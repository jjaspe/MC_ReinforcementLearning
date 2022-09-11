from config import config
from models.world import World

class BaseRuleset:
    def __init__(self, policy, deckBuilder):
        self.deckBuilder = deckBuilder
        self.policy = policy
        self.heroDeck = []
        self.bossDeck = []

    def makeWorld(self):
        hero = self.makeHero()
        boss = self.makeBoss()
        if len(self.heroDeck) == 0:
            self.heroDeck = self.deckBuilder.buildFullDeck(self.deckBuilder.cards, config.DECK_SIZE)
        if len(self.bossDeck) == 0:
            self.bossDeck = self.deckBuilder.buildFullDeck(self.deckBuilder.cards, config.DECK_SIZE)
        self.world = World(self.deckBuilder.cards, hero, boss, self.heroDeck, self.bossDeck)
        self.world.isPlayerTurn = True
        return self.world

    def makeHero(self):
        hero = self.deckBuilder.makeHero()
        hero.ruleset = self
        return hero

    def makeBoss(self):
        boss = self.deckBuilder.makeBoss()
        boss.ruleset = self
        return boss

    def removeCardsFromHand(self, cards, hand):
        for card in cards:
            index = hand.index(card)
            if index != -1:
                hand.pop(index)
        return hand

    def fillHand(self, hand, deck):
        while len(hand) < config.HAND_SIZE:
            hand.append(deck.pop())

    def ensureHeroDeck(self, deck):
        if len(deck) < config.DECK_SIZE:
            deck = self.deckBuilder.buildFullDeck(self.deckBuilder.cards, config.DECK_SIZE)
        return deck



