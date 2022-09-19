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