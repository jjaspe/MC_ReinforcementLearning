import math
from models.killable import Killable
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


