from config import config, log
from models.match import Match
from models.world import World

class Game:
    def __init__(self, policy, deckBuilder, ruleset):
        self.deckBuilder = deckBuilder
        self.policy = policy
        self.heroDeck = []
        self.bossDeck = []
        self.ruleset = ruleset

    def makeWorld(self):
        hero = self.deckBuilder.makeHero()
        boss = self.deckBuilder.makeBoss()
        if len(self.heroDeck) == 0:
            self.heroDeck = self.deckBuilder.buildFullDeck(self.deckBuilder.cards, config.DECK_SIZE)
        if len(self.bossDeck) == 0:
            self.bossDeck = self.deckBuilder.buildFullDeck(self.deckBuilder.cards, config.DECK_SIZE)
        self.world = World(self.deckBuilder.cards, hero, boss, self.heroDeck, self.bossDeck)
        self.world.isPlayerTurn = True
        return self.world

    def makeMatch(self):
        world = self.makeWorld()        
        world.heroHand = self.deckBuilder.buildHand(world.heroDeck, config.HAND_SIZE)
        layers = self.ruleset.makeLayers(self.policy, world)
        match = Match(world, layers)
        return match


    # def removeCardsFromHand(self, cards, hand):
    #     for card in cards:
    #         index = hand.index(card)
    #         if index != -1:
    #             hand.pop(index)
    #     return hand

    # def fillHand(self, hand, deck):
    #     while len(hand) < config.HAND_SIZE:
    #         hand.append(deck.pop())

    # def ensureHeroDeck(self, deck):
    #     if len(deck) < config.DECK_SIZE:
    #         deck = self.deckBuilder.buildFullDeck(self.deckBuilder.cards, config.DECK_SIZE)
    #     return deck



