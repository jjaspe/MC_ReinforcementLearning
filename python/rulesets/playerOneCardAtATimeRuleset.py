from GameLayers.attackLayer import UnderCostBudgetAttackLayer
from GameLayers.bossAttackLayer import DamageOnlyBossAttackLayer
from GameLayers.bossDrawLayer import DefaultBossDrawLayer
from GameLayers.bossEndTurnLayer import DefaultBossEndTurnLayer
from GameLayers.drawCardsLayer import RebuildInitialHandDrawCardsLayer
from GameLayers.heroDefendLayer import DefaultHeroDefendLayer
from GameLayers.pickAttackCardLayer import OneCardPickAttackCardsLayer
from GameLayers.playerEndTurnLayer import DefaultPlayerEndTurnLayer, TurnBudgetUsedPlayerEndTurnLayer
from GameLayers.startGameLayer import DefaultStartGameLayer
from GameLayers.pickPayingCardsLayers import DefaultPickPayingCardsLayer
from GameLayers.exhaustAttackCardsLayer import DefaultExhaustAttackCardsLayer


class PlayerOneCardAtATimeRuleset():
    def __init__(self):        
        pass
    
    def makeLayers(self, policy, world):
        layers = [
            DefaultStartGameLayer(),
            DefaultPickPayingCardsLayer(),
            OneCardPickAttackCardsLayer(policy),
            UnderCostBudgetAttackLayer(),
            DefaultExhaustAttackCardsLayer(),
            DefaultPlayerEndTurnLayer(),
            RebuildInitialHandDrawCardsLayer(world.heroHand),
            DefaultBossDrawLayer(),
            DamageOnlyBossAttackLayer(),
            DefaultHeroDefendLayer(),
            DefaultBossEndTurnLayer()
        ]
        return layers