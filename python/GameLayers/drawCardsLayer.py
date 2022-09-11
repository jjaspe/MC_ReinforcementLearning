import config

class RebuildInitialHandDrawCardsLayer:
    def __init__(self, hand):
        self.hand = hand

    def execute(self, world):
        world.heroHand = self.hand

class DrawFromDeckDrawCardsLayer:
    def execute(self, world):
        while(len(world.heroHand) < config.HAND_SIZE):
            world.heroHand.append(world.heroDeck.pop())


