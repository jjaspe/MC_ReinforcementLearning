import math
import config

class UnderCostBudgetAttackLayer:
    def execute(self, world):
        cards = world.attackCards
        for card in cards:
            if card.cost <= world.turnBudget:
                world.boss.health = world.hero.attackAction(world.boss, card)
            world.turnBudget -= max(1, card.cost)
        
class DefaultAttackLayer:
    def execute(self, world):
        cards = world.attackCards
        for card in cards:
            world.boss.health = world.hero.attackAction(world.boss, card)
        world.turnBudget -= max(1, card.cost)
