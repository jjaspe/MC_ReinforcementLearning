import { Ally } from './classes.js'
import { config } from './config.js'

class Hero extends Ally {
  constructor(name, text, health, attack, thawrt, defense, alterEgo) {
    super(name, text, health, attack, thawrt)
    this.alterEgo = alterEgo
    this.defense = defense
    this.inHeroForm = true
    this.ready = true
    this.maxHealth = health
    this.ruleset = null;
  }

  shouldHeroDefend = function() {
    return (this.health < 14 && this.health > 10)
  }

  shouldHeroSwitch = function() {
    return (this.health < 10 && this.inHeroForm) || (this.health >= 10 && !this.inHeroForm)
  }
  reducedDamage = function(damage) {
    return damage - this.defense
  }

  switch = function() {
    this.inHeroForm = !this.inHeroForm
  }

  /* Actions */
  thwartAction = function(scheme, card) {
    scheme.threat = scheme.threat - card.thwart
    return scheme.threat
  }

  attackAction = function(boss, card) {
    var damage = card.attack
    boss.health = boss.health - damage
    //print('Hit boss for ' + damage + ' damage')
    return boss.health
  }

  takeDamage = function(damage) {
    this.health = this.health - Math.max(damage, 0)
  }

  /* Villain Phases */
  damageOnlyVillainPhase = function(damage) {
    this.takeDamage(damage)
  }

  damageAndDefendVillainPhase = function() {
    this.ready = true
    if (this.inHeroForm) {
      if (this.shouldHeroDefend()) {
        this.takeDamage(this.reducedDamage(damage))
        this.ready = false
      }
      else {
        this.takeDamage(damage)
      }
    }
  }

  /* Player Phases */
  damageThwartAndHealPlayerPhase = function(boss, card, scheme) {
    if (this.shouldHeroSwitch()) {
      this.switch()
    }
    if (this.inHeroForm && this.ready && scheme.threat > 14) {
      scheme.threat = Math.max(this.thwartAction(scheme, card), 0)
    }
    if (this.inHeroForm && this.ready) {
      boss.health = this.attackAction(boss, card)
      this.ready = false
    }
    else {
      if (!this.inHeroForm) {
        this.alterEgo.playerPhase(boss, card, this)
      }
    }
  }

  /* Phases */
  villainPhase = function(damage) {
    this.damageOnlyVillainPhase(damage)
  }

  playerPhase = function(world, hand) {
    this.ruleset.playerPhase(world, hand)
  }
}

class AlterEgo extends Ally {
  regen = 0

  constructor(name, text, health, regen) {
    super(name, text, health, 0, 0)
    this.regen = regen
  }
  playerPhase = function(boss, card, hero) {
    hero.health = Math.min(this.regen + hero.health, hero.maxHealth)

  }
}
export { Hero, AlterEgo }