import config

class DefaultBossEndTurnLayer:
    def execute(self, world):
        world.isPlayerTurn = True
