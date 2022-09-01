import { Ally } from './classes.js'
import {config} from '../config.js'


class World {
  constructor(cards, hero, boss, heroDeck, bossDeck) {
    this.cards = cards
    this.hero = hero
    this.boss = boss
    this.heroDeck = heroDeck
    this.bossDeck = bossDeck
    this.heroHand = []
    this.attackCards = []
    this.discarded = []
    this.endPlayerTurn = false
  }

  intializeAlly = function() {
    var card2 = new Ally('Card', '', 1, Math.floor(Math.random() * config.HAND_SIZE), 
    Math.floor(Math.random() * config.HAND_SIZE))
    card2.cost = Math.floor(card2.attack / config.COST_DIVISOR)
    return card2
  }

  makeHand = function(handSize, deckCards) {
    var hand = []
    for (var x = 0; x < handSize; x++)
      hand.push(deckCards.pop())
    return hand
  }
}

export { World }