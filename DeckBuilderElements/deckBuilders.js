import { Ally } from '../models/classes.js'
import { config } from '../config.js'
import { Hero } from '../models/hero.js'
import { Boss } from '../models/boss.js'
import { BaseHandBuilder, HAND_BUILDER_TYPES } from './handBuilders.js'
import { DeckShuffler, DefaultPostBuilder } from './postBuilders.js'

class BaseDeckBuilder {
  static makeDeckBuilder = function(deckBuilderType, handBuilder) {
    var deckBuilder = null
    switch (deckBuilderType) {
      case DECK_BUILDER_TYPES.DAMAGE_ONLY:
        deckBuilder = new DamageOnlyDeckBuilder(config.MIN_HERO_ALLY_ATTACK, config.MAX_HERO_ALLY_ATTACK);
        break;
      case DECK_BUILDER_TYPES.DAMAGE_AND_COST:
        deckBuilder = new DamageAndCostDeckBuilder(config.MIN_HERO_ALLY_ATTACK, config.MAX_HERO_ALLY_ATTACK,
          config.MIN_HERO_ALLY_COST, config.MAX_HERO_ALLY_COST)
          break;
      case DECK_BUILDER_TYPES.DAMAGE_AND_CUSTOM_COST_SHUFFLED:
        deckBuilder = new DamageAndCustomCostShuffledDeckBuilder(config.MIN_HERO_ALLY_ATTACK, config.MAX_HERO_ALLY_ATTACK,
          config.MIN_HERO_ALLY_COST, config.MAX_HERO_ALLY_COST)
        deckBuilder.postBuilder = new DeckShuffler();
          break;
      case DECK_BUILDER_TYPES.DAMAGE_AND_SQUARED_COST:
        deckBuilder = DamageAndSquaredCostDeckBuilder(config.MIN_HERO_ALLY_ATTACK, config.MAX_HERO_ALLY_ATTACK,
          config.MIN_HERO_ALLY_COST, config.MAX_HERO_ALLY_COST)
          break;
      case DECK_BUILDER_TYPES.NORMALIZED_DAMAGE_AND_SQUARED_COST:
        deckBuilder = new NormalizedDamageAndSquaredCostDeckBuilder(config.MIN_HERO_ALLY_ATTACK, config.MAX_HERO_ALLY_ATTACK,
          config.MIN_HERO_ALLY_COST, config.MAX_HERO_ALLY_COST)
          break;
      case DECK_BUILDER_TYPES.DAMAGE_AND_CUSTOM_COST:
        deckBuilder = new DamageAndCustomCostDeckBuilder(config.MIN_HERO_ALLY_ATTACK, config.MAX_HERO_ALLY_ATTACK,
          config.MIN_HERO_ALLY_COST, config.MAX_HERO_ALLY_COST)
          break;
      case DECK_BUILDER_TYPES.DAMAGE_AND_CUSTOM_COST_CUSTOM_HAND:
        deckBuilder = new DamageAndCustomCostDeckBuilder(config.MIN_HERO_ALLY_ATTACK, config.MAX_HERO_ALLY_ATTACK,
          config.MIN_HERO_ALLY_COST, config.MAX_HERO_ALLY_COST)
          break;
      default:
        throw 'Invalid deck builder type'
    }
    deckBuilder.cards = deckBuilder.buildCards()
    deckBuilder.fullDeck = deckBuilder.buildFullDeck(deckBuilder.cards, config.DECK_SIZE)
    deckBuilder.fullDeck = deckBuilder.postBuilder.execute(deckBuilder.fullDeck)
    deckBuilder.handBuilder = handBuilder
    return deckBuilder
  }

  constructor(){
    this.postBuilder = new DefaultPostBuilder();
  }

  makeHero = function() {
    return new Hero('Hero', '', config.HERO_HEALTH, 0, 0, config.HERO_ATTACK, null)
  }

  makeBoss = function() {
    return new Boss('boss', '', config.BOSS_HEALTH, config.BOSS_ATTACK, config.BOSS_SCHEME)
  }

  buildHand = function(deck, size){
    return this.handBuilder.buildHand(deck, size)
  }

  buildFullDeck = function(cards, deckSize) {
    var deck = []
    var len = cards.length
    for (var x = 0; x < deckSize; x++) {
      var card = cards[Math.floor(Math.random() * (len))]
      deck.push({ ...card })
    }
    return deck
  }
}

class DamageOnlyDeckBuilder extends BaseDeckBuilder{
  constructor(min, max) {
    super();
    this.minDamage = min
    this.maxDamage = max
  }

  buildCards = function() {
    var cards = []
    for (var i = this.minDamage; i <= this.maxDamage; i++) {      
      cards.push(new Ally('Ally Damage ' + i, '', 0, i, 0))
    }
    return cards
  }
}

class DamageAndCostDeckBuilder extends BaseDeckBuilder {
  constructor(minDamage, maxDamage, minCost, maxCost) {
    super();
    this.minDamage = minDamage
    this.maxDamage = maxDamage
    this.minCost = minCost
    this.maxCost = maxCost
  }

  buildCards = function() {
    var cards = []
    for (var i = this.minDamage; i <= this.maxDamage; i++) {
      var cost = Math.min(this.maxCost, Math.max(this.minCost, Math.floor(i/2)))
      var ally = new Ally('Ally Damage ' + i + ' Cost: ' + cost, '', 0, i, 0)
      ally.cost = cost
      cards.push(ally)
    }
    return cards
  }
}

class DamageAndSquaredCostDeckBuilder extends BaseDeckBuilder {
  constructor(minDamage, maxDamage, minCost, maxCost) {
    super();
    this.minDamage = minDamage
    this.maxDamage = maxDamage
    this.minCost = minCost
    this.maxCost = maxCost
  }

  buildCards = function() {
    var cards = []
    for (var i = this.minDamage; i <= this.maxDamage; i++) {
      var cost = Math.min(this.maxCost, Math.max(this.minCost, Math.floor(i*i/4)))
      var ally = new Ally('Ally Damage ' + i + ' Cost: ' + cost, '', 0, i, 0)
      ally.cost = cost
      cards.push(ally)
    }
    return cards
  }
}

class DamageAndCustomCostDeckBuilder extends BaseDeckBuilder {
  constructor(minDamage, maxDamage, minCost, maxCost) {
    super();
    this.minDamage = minDamage
    this.maxDamage = maxDamage
    this.minCost = minCost
    this.maxCost = maxCost
  }

  buildCards = function() {
    var cards = []
    for (var i = this.minDamage; i <= this.maxDamage; i++) {
      var cost = 1
      switch (i) {
        case 0:
          cost = 1
          break;
        case 1:
          cost = 1
          break;
        case 2:
          cost = 1
          break;
        case 3:
          cost = 2
          break;
        // case 4:
        //   cost = 3
        //   break;
        // case 5:
        //   cost = 3
        //   break;
        // case 6:
        //   cost = 4
        //   break;
        default:
          cost = this.maxCost
          break;
      }
      var ally = new Ally('Ally Damage ' + i + ' Cost: ' + cost, '', 0, i, 0)
      ally.cost = cost
      cards.push(ally)
    }
    return cards
  }

  buildFullDeck = function(cards, deckSize) {
    var deck = []
    
    var attacks = cards.map(n => n.attack)
    // remove duplicates
    attacks = attacks.filter((v,i) => attacks.indexOf(v) == i)
    var cardsPerAttack = Math.floor(deckSize / attacks.length)
    for (var x = 0; x < cardsPerAttack; x++) {
      for (var i = 0; i < attacks.length; i++) {
        var attack = attacks[i]      
        var card = cards.find(n => n.attack == attack)
        deck.push({ ...card })
      }
    }
    // fill out the rest of the deck with 0 attack cards
    var zeroAttackCard = cards.find(n => n.attack == 0)
    for (var i = 0; i < deckSize - deck.length; i++) {
      deck.push({ ...zeroAttackCard})
    }
    
    return deck
  }
}

class NormalizedDamageAndSquaredCostDeckBuilder extends BaseDeckBuilder {
  scale = 100;

  constructor(minDamage, maxDamage, minCost, maxCost) {
    super();
    this.minDamage = minDamage
    this.maxDamage = maxDamage
    this.minCost = minCost
    this.maxCost = maxCost
  }

  buildCards = function() {
    var cards = []
    for (var i = this.minDamage; i <= this.maxDamage; i++) {
      var cost = Math.min(this.maxCost, Math.max(this.minCost, Math.floor(i/2)))
      var ally = new Ally('Ally Damage ' + i + ' Cost: ' + cost, '', 0, i/this.scale, 0)
      ally.cost = cost
      cards.push(ally)
    }
    return cards
  }

  makeHero = function() {
    return new Hero('Hero', '', config.HERO_HEALTH/this.scale, 0, 0, config.HERO_ATTACK, null)
  }

  makeBoss = function() {
    return new Boss('Boss', '', config.BOSS_HEALTH/this.scale, config.BOSS_ATTACK/this.scale, config.BOSS_SCHEME)
  }
}

const DECK_BUILDER_TYPES = {
  DAMAGE_ONLY: 'damageOnly',
  DAMAGE_AND_COST: 'damageAndCost',
  DAMAGE_AND_SQUARED_COST: 'damageAndSquaredCost',
  NORMALIZED_DAMAGE_AND_SQUARED_COST: 'normalizedDamageAndSquaredCost',
  DAMAGE_AND_CUSTOM_COST: 'damageAndCustomCost',
  DAMAGE_AND_CUSTOM_COST_SHUFFLED: 'damageAndCustomCostShuffled',
  DAMAGE_AND_CUSTOM_COST_CUSTOM_HAND: 'damageAndCustomCostCustomHand',
  DAMAGE_AND_CUSTOM_COST_CUSTOM_HAND_SHUFFLED: 'damageAndCustomCostCustomHand',
}

export { DECK_BUILDER_TYPES, BaseDeckBuilder, 
  DamageOnlyDeckBuilder, DamageAndCostDeckBuilder, 
  DamageAndSquaredCostDeckBuilder, 
  NormalizedDamageAndSquaredCostDeckBuilder, DamageAndCustomCostDeckBuilder
   }