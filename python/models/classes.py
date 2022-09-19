class Hand:
    def __init__(self):
        self.cards = []

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

