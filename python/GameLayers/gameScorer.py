import math
import config

class DefaultScorer:
    def __init__(self, healthPower):
        self.healthPower = healthPower

    def scoreGame(self, isVictory, world):
        baseScore = config.SCORE_MULTIPLIER
        victoryScore = math.pow(world.hero.health, self.healthPower)
        defeatScore = -math.pow(world.boss.health, math.floor(self.healthPower))
        score = baseScore * (victoryScore if isVictory else defeatScore)
        return score

class ExpScorer:
    def __init__(self, powerConstant, linearConstant):    
        self.powerConstant = powerConstant
        self.linearConstant = linearConstant

    def scoreGame(self, isVictory, world):
        hero = max(0, world.hero.health)
        boss = max(0, world.boss.health)
        score = (1 if isVictory else -1)*math.pow(2, self.powerConstant*(hero+boss))
        return score*self.linearConstant;

class LogScorer:
    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2

    def scoreGame(self, isVictory, world):
        hero = max(0, world.hero.health)
        boss = max(0, world.boss.health)
        score = 1 if isVictory else -1
        score *= self.c1*(math.log(hero+boss))
        return score

