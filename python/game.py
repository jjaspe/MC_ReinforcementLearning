class Game:
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

    # def drawCard(self, hand, deck, handSize):
    #     if len(deck) < handSize:
    #         deck = makeDeck(40)
    #         print('rebuilding deck')
    #     for x in range(len(hand), handSize):
    #         hand.append(deck.pop())
    #     return deck

    def isdead(self, unit):
        if unit.health <= 0:
            return True
        else:
            return False

    def payForCards(self, playedCard, hand):
        hand.pop(0, playedCard.cost)

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
            print('Playing hand ' + str(handNumber))
            handNumber += 1
            while world.isPlayerTurn:
                self.payForCardsLayer.execute(world)
                self.pickAttackCardLayer.execute(world)
                self.attackLayer.execute(world)
                self.playerContinueTurnLayer.execute(world)
                if self.isdead(boss):
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
                    if self.isdead(hero):
                        gameEnd = True
                        break
        print('Victory' if victory else 'Defeat')
        print('Hero:', hero.health, '   ', 'Boss:', boss.health)
        return victory

if __name__ == '__main__':
    pass
