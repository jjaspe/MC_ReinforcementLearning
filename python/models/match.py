from config import config, log

class Match:
    def __init__(self, world, layers):
        self.world = world
        self.layers = layers
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

    def start(self):
        return self.playWithLayers()

    def playWithLayers(self):
        world = self.world
        hero = world.hero
        boss = world.boss
        gameEnd = False
        victory = False
        scheme = 0
        handNumber = 0
        self.startGameLayer.execute(world)
        while not gameEnd:
            log('Playing hand ' + str(handNumber))
            handNumber += 1
            while world.isPlayerTurn:
                self.payForCardsLayer.execute(world)
                self.pickAttackCardLayer.execute(world)
                self.attackLayer.execute(world)
                self.playerContinueTurnLayer.execute(world)
                if boss.is_dead():
                    gameEnd = True
                    victory = True
                    break
            if not gameEnd:
                # play the rest of the layers
                while not world.isPlayerTurn:
                    self.rebuildHandLayer.execute(world)
                    self.bossDrawLayer.execute(world)
                    self.bossAttackLayer.execute(world)
                    self.heroDefendLayer.execute(world)
                    self.bossEndTurnLayer.execute(world)
                    if hero.is_dead():
                        gameEnd = True
                        break
        log('Victory' if victory else 'Defeat')
        log('Hero:', hero.health, '   ', 'Boss:', boss.health)
        return victory
