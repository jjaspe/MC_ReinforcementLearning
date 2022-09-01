import * as tf from '@tensorflow/tfjs'
import {config} from './config.js'

class BaseEncoder {
  constructor(cards) {
    this.cards = cards
    this.getOneHotEncodedCardByIndex = this.getOneHotEncodedCardByIndex.bind(this)
  }

  getOneHotEncodedCardByIndex = function(index) {
    return this.cardMatrix.arraySync()[index]
  }

  buildCardMatrix = function(uniqueCards) {
    var indeces = uniqueCards.map((_, i) => i) 
    var iTensor = tf.tensor1d(indeces, 'int32')
    var oh = tf.oneHot(iTensor, uniqueCards.length)
    return oh
  }

  getOneHotEncodedCombinationByIndeces = function(indeces) {
    var matrix = this.cardMatrix.arraySync()
    var oneHots = indeces.map(n => matrix[n])
    return oneHots
  }

  getCardByOneHotEncoding = function(oneHotCard) {
    var index = this.cardMatrix.indexOf(oneHotCard)
    return uniqueCards[index]
  }
}


export class DamageEncoder extends BaseEncoder {
  constructor(cards) {
    super(cards)
    this.uniqueCards = this.getDistinctCardsByDamage(cards)
    this.inputUnits = this.uniqueCards.length;
    this.cardMatrix = this.buildCardMatrix(this.uniqueCards)
  }

  getDistinctCardsByDamage = function(cards) {
    var damages = []
    var uniqueCards = []
    for (var i = 0; i < cards.length; i++) {
      if (damages.indexOf(cards[i].attack) == -1) {
        damages.push(cards[i].attack)
        uniqueCards.push(cards[i])
      }
    }
    return uniqueCards;
  }

  oneHotEncodeCards = function(cards) {
    var damages = this.uniqueCards.map(n => n.attack);
    var indeces = cards.map(n => damages.indexOf(n.attack))
    var matrix = this.cardMatrix.arraySync()
    var oneHots = indeces.map(n => matrix[n])
    return oneHots;
  }

  getIndexOfCard = function(card) {
    var damages = this.uniqueCards.map(n => n.attack);
    var index = damages.indexOf(card.attack)
    return index
  }

  getIndecesOfCards = function(cards) {
    return cards.map(n => this.getIndexOfCard(n))
  }

  encodeCard = function(card, world) {
    return this.oneHotEncodeCards([card])[0]
  }
}

export class DamageAndCostEncoder extends DamageEncoder {
  constructor(cards) {
    super(cards)
    this.inputUnits = this.inputUnits + 1 // for cost
  }

  encodeCard = function(card, world) {
    var oh = oneHotEncodeCards([card])[0]
    oh.push(world.turnBudget/ config.HERO_BUDGET);
  }
}