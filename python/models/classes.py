class Card:
    def __init__(self, name, text):
        self.name = name
        self.text = text
        self.cost = 0
        self.resourcesGiven = 0
        self.limitPerTurn = 0
        self.color = None
        self.type = None
        self.subtype = None
        self.maxPerPlayer = 0
        self.maxPerDeck = 0
        self.uses = 0

class Hand:
    def __init__(self):
        self.cards = []

class Ally(Card):
    def __init__(self, name, text, health, attack, thwart):
        super().__init__(name, text)
        self.health = health
        self.attack = attack
        self.status = 0
        self.thwart = thwart

class Player:
    def __init__(self):
        pass

class Resource:
    def __init__(self, type):
        self.type = type

class Status:
    def __init__(self, type):
        self.type = type

class Action:
    def __init__(self):
        self.conditions = None
        self.effects = None

class Condition:
    def __init__(self, name):
        self.name = name

class PlayHasXSubtypeCards(Condition):
    def __init__(self, amount, subtype):
        self.amount = amount
        self.subtype = subtype

class Effect:
    def __init__(self, name):
        self.name = name

if __name__ == "__main__":
    pass

