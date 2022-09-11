from models.classes import Ally

class Hero(Ally):
  def __init__(self, name, text, health, attack, thwart):
    super().__init__(name, text, health, attack, thwart)
    self.alterEgo = None
    self.defense = 0
    self.inHeroForm = True
    self.ready = True
    self.maxHealth = health
    self.ruleset = None

  def shouldHeroDefend(self):
    return self.health < 14 and self.health > 10

  def shouldHeroSwitch(self):
    return (self.health < 10 and self.inHeroForm) or (self.health >= 10 and not self.inHeroForm)

  def reducedDamage(self, damage):
    return damage - self.defense

  def switch(self):
    self.inHeroForm = not self.inHeroForm

  def thwartAction(self, scheme, card):
    scheme.threat = scheme.threat - card.thwart
    return scheme.threat

  def attackAction(self, boss, card):
    damage = card.attack
    boss.health = boss.health - damage
    #print('Hit boss for ' + damage + ' damage')
    return boss.health

  def takeDamage(self, damage):
    self.health = self.health - max(damage, 0)

  def damageOnlyVillainPhase(self, damage):
    self.takeDamage(damage)

  def damageAndDefendVillainPhase(self, damage):
    self.ready = True
    if self.inHeroForm:
      if self.shouldHeroDefend():
        self.takeDamage(self.reducedDamage(damage))
        self.ready = False
      else:
        self.takeDamage(damage)

  def damageThwartAndHealPlayerPhase(self, boss, card, scheme):
    if self.shouldHeroSwitch():
      self.switch()
    if self.inHeroForm and self.ready and scheme.threat > 14:
      scheme.threat = max(self.thwartAction(scheme, card), 0)
    if self.inHeroForm and self.ready:
      boss.health = self.attackAction(boss, card)
      self.ready = False
    else:
      if not self.inHeroForm:
        self.alterEgo.playerPhase(boss, card, self)

  def villainPhase(self, damage):
    self.damageOnlyVillainPhase(damage)

  def playerPhase(self, world, hand):
    self.ruleset.playerPhase(world, hand)

class AlterEgo(Ally):
  def __init__(self, name, text, health, regen):
    super().__init__(name, text, health, 0, 0)
    self.regen = regen

  def playerPhase(self, boss, card, hero):
    hero.health = min(self.regen + hero.health, hero.maxHealth)


