import { Ally } from './classes.js'

class Boss extends Ally {
  constructor(name, text, health, attack, thwart) {
    super(name, text, health, attack, thwart)
  }

  getDamage = function(enemyDeck) {
    var card = enemyDeck.pop()
    var boost = card.attack
    var damage = this.attack + boost
    return damage
  }
  getThreat = function(enemyDeck) {
    var card = enemyDeck.pop()
    var boost = card.thwart
    var threat = this.thwart + boost
    return threat
  }

  /* Villain Phases */
  threatAndDamage = function(hero, scheme, villainDeck) {
    if (hero.inHeroForm = false) {
      scheme.threat = scheme.threat + this.getThreat
    } else {
      //do damage to hero
    }
  }

  damageOnly = function(hero, scheme, villainDeck) {
    hero.villainPhase(this.attack)
  }

  villainPhase = function(hero, scheme, villainDeck) {
    this.damageOnly(hero, scheme, villainDeck)
  }
}

export { Boss }