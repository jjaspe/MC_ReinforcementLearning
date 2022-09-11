import config

class UnderCostBudgetAttackLayer:
    def execute(self, world):
        cards = world.attackCards
        for card in cards:
            if card.cost <= world.turnBudget:
                world.boss.health = world.hero.attackAction(world.boss, card)
            world.turnBudget -= card.cost
