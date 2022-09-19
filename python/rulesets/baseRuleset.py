class BaseRuleset:
    def __init__(self):
        pass

    def setLayers(self, layers):
        self.startGameLayer = layers.pop(0)
        self.payForCardsLayer = layers.pop(0)
        self.pickAttackCardLayer = layers.pop(0)
        self.attackLayer = layers.pop(0)
        self.exhaustCardLayer = layers.pop(0)
        self.playerContinueTurnLayer = layers.pop(0)
        self.rebuildHandLayer = layers.pop(0)
        self.bossDrawLayer = layers.pop(0)
        self.bossAttackLayer = layers.pop(0)
        self.heroDefendLayer = layers.pop(0)
        self.bossEndTurnLayer = layers.pop(0)
