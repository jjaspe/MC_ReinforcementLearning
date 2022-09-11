import config

class DefaultExhaustAttackCardsLayer:
    def execute(self, world):
        pass

class DiscardCardsExhaustAttackCardsLayer:

    def execute(self, world):
        for card in world.attackCards:
            index = world.heroHand.index(card)
            if index != -1:
                world.heroHand.pop(index)


