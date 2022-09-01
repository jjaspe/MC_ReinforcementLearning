import {config, print} from './config.js'
import { BaseDeckBuilder } from './DeckBuilderElements/deckBuilders.js'
import { BasePolicy } from './cardPickerPolicy.js'
import { DamageEncoder } from './cardEncoder.js'
import { World  } from './models/world.js'

class BaseRuleset {
  constructor(policy, deckBuilder) {
    this.deckBuilder = deckBuilder
    this.policy = policy
    this.heroDeck = []
    this.bossDeck = []
  }

  makeWorld = function() {
    var hero = this.makeHero()
    var boss = this.makeBoss()
    if(this.heroDeck.length == 0){
      this.heroDeck = this.deckBuilder.buildFullDeck(this.deckBuilder.cards, config.DECK_SIZE)
    }
    if(this.bossDeck.length == 0){
      this.bossDeck = this.deckBuilder.buildFullDeck(this.deckBuilder.cards, config.DECK_SIZE)
    }
    this.world = new World([...this.deckBuilder.cards], hero, boss, [...this.heroDeck], [...this.bossDeck])
    this.world.isPlayerTurn = true
    return this.world;
  }

  makeHero = function() {
    var hero = this.deckBuilder.makeHero()
    hero.ruleset = this;
    return hero
  }

  makeBoss = function() {
    var boss = this.deckBuilder.makeBoss()
    boss.ruleset = this;
    return boss
  }

  removeCardsFromHand =  function(cards, hand) {
    for (var i = 0; i < cards.length; i++) {
      var card = cards[i]
      var index = hand.indexOf(card)
      if (index != -1) {
        hand.splice(index, 1)
      }
    }
    return hand
  }
  
  fillHand = function(hand, deck) {
    while(hand.length < config.HAND_SIZE) {
      hand.push(deck.pop())
    }
  }

  ensureHeroDeck = function(deck) {
    if (deck.length < config.DECK_SIZE) { 
      deck = this.deckBuilder.buildFullDeck(this.deckBuilder.cards, config.DECK_SIZE)
    }
    return deck
  }
}

class DamageOnlyRuleset extends BaseRuleset{
    constructor(policy, deckBuilder) {
        super(policy,deckBuilder)
    }
    
    villainPhase = function(boss, card, hand) {
    }

    playerPhase = function(world, hand) {
        var card = this.policy.pickCards(hand)[0]
        print(`${world.hero.name} played ${card.name}`)
        world.boss.health = hero.attackAction(world.boss, card)
        print('Hero:', world.hero.health, '   ', 'Boss:', world.boss.health)
    }
}

class DamageAndCostRuleset extends BaseRuleset{
    constructor(policy, deckBuilder) {
        super(policy, deckBuilder)
    }
    
    villainPhase = function(boss, card, scheme) {
    }

    playerPhase = function(world, hand) {
        var card = this.policy.pickCards(hand)[0]
        if(card.cost <= config.HERO_BUDGET){
            world.boss.health = world.hero.attackAction(world.boss, card)
        }
        // this.removeCardsFromHand([card], hand)
        // this.fillHand(hand, world.heroDeck)
        // this.ensureHeroDeck(world.heroDeck)
    }
}

class MultiCardDamageAndCostRuleset extends BaseRuleset{
    constructor(policy, deckBuilder) {
        super(policy, deckBuilder)
    }    
    
    villainPhase = function(boss, card, scheme) {
    }

    playerPhase = function(world, hand) {
        var cards = this.policy.pickCards(hand, config.HERO_BUDGET)        
        var budget = config.HERO_BUDGET
        for(var i = 0; i < cards.length; i++){
            var card = cards[i]
            if(card.cost <= budget){
                budget -= card.cost
                world.boss.health = world.hero.attackAction(world.boss, card)
            }
        }
    }
}

export {DamageOnlyRuleset, DamageAndCostRuleset, MultiCardDamageAndCostRuleset}