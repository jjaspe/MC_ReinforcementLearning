from models.killable import Killable
from config import config, log

class Boss(Killable):
  def __init__(self, name, text, health, attack, thwart):
      super().__init__(name, text, health, attack, thwart)

  def getDamage(self, enemyDeck):
      card = enemyDeck.pop()
      boost = card.attack
      damage = self.attack + boost
      return damage

  def getThreat(self, enemyDeck):
      card = enemyDeck.pop()
      boost = card.thwart
      threat = self.thwart + boost
      return threat

  def threatAndDamage(self, hero, scheme, villainDeck):
      if hero.inHeroForm == False:
          scheme.threat = scheme.threat + self.getThreat(villainDeck)
      else:
          #do damage to hero
          log('do damage to hero')


