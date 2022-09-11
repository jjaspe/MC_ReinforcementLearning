# the following is the above code in python

class config:
    HAND_SIZE= 8
    DECK_SIZE= 100
    COST_DIVISOR= 2
    BOSS_HEALTH= 16
    BOSS_ATTACK= 3
    BOSS_SCHEME= 1
    HERO_HEALTH= 13
    HERO_ATTACK= 0
    MAX_HERO_ALLY_ATTACK= 3
    MIN_HERO_ALLY_ATTACK= 0
    MAX_HERO_ALLY_COST= 50
    MIN_HERO_ALLY_COST= 0
    HERO_BUDGET= 2
    PLAYER_TURN_LAYERS= 5
    ALLOW_PRINT= False
    ALLOW_DEBUG_PRINT= True
    PLOT= True
    HIDDEN_UNITS= 40
    HIDDEN_LAYERS= 0
    EPOCHS= 100
    EXPLORE_BATCH_SIZE= 100
    SCORE_MULTIPLIER= 1


def log(self, *stuff):
    if config.ALLOW_PRINT:
        print(*stuff)

def debug(self, *stuff):
    if config.ALLOW_DEBUG_PRINT:
        print(*stuff)

# Path: python\config.py

