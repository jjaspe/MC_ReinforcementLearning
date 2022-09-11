import config

class DefaultPlayerEndTurnLayer:
    def execute(self, world):
        world.isPlayerTurn = False

class TurnBudgetUsedPlayerEndTurnLayer:
    def execute(self, world):
        world.isPlayerTurn = world.turnBudget > 0



