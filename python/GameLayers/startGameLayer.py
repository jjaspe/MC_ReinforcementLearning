import config

class DefaultStartGameLayer:
    def execute(self, world):
        world.isPlayerTurn = True
        world.turnBudget = config.HERO_BUDGET
