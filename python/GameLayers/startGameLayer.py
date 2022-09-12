from config import config, log

class DefaultStartGameLayer:
    def execute(self, world):
        world.isPlayerTurn = True
        world.turnBudget = config.HERO_BUDGET
