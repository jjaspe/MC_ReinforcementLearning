import config

class OneCardPickAttackCardsLayer:
    def __init__(self, policy):
        self.policy = policy

    def execute(self, world):
        world.attackCards = [self.policy.pickCards(world.heroHand, world)[0]]
        # print('Picked Cards:', world.attackCards.map(n => n.attack))

class MultipleCardPickAttackCardsLayer:
    def __init__(self, policy):
        self.policy = policy

    def execute(self, world):
        world.attackCards = self.policy.pickCards(world.heroHand, world)
        # print('Picked Cards:', world.attackCards.map(n => n.attack))
        



