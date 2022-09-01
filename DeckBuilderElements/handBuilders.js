import {Ally} from '../models/classes.js'
import {config, print} from '../config.js'

export const HAND_BUILDER_TYPES = {
    RANDOM: 'RandomHandBuilder',
    N_OF_EACH: 'NOfEachHandBuilder'
}

export class BaseHandBuilder {
    static makeHandBuilder = function(handBuilderType){
        switch (handBuilderType) {
            case HAND_BUILDER_TYPES.RANDOM:
                return new RandomHandBuilder(config.MIN_HERO_ALLY_ATTACK, config.MAX_HERO_ALLY_ATTACK)
            case HAND_BUILDER_TYPES.N_OF_EACH:
                return new NOfEachHandBuilder(config.MIN_HERO_ALLY_ATTACK, config.MAX_HERO_ALLY_ATTACK)
            default:
                throw new Error('Invalid hand builder type')
        }
    }
}

export class RandomHandBuilder extends BaseHandBuilder{
    constructor(minDamage, maxDamage) {
        super();
        this.minDamage = minDamage
        this.maxDamage = maxDamage
    }
    
    buildHand = function(deck, handSize) {
        var hand = []
        for (var i = 0; i < handSize; i++) {
            var index = Math.floor(Math.random() * deck.length)
            hand.push(deck[index])
            deck.splice(index, 1)
        }
        return hand
    }
}

export class NOfEachHandBuilder extends BaseHandBuilder{
    constructor(minDamage, maxDamage) {
        super();
        this.minDamage = minDamage
        this.maxDamage = maxDamage
    }
    
    buildHand = function(deck, handSize){
        var hand = []
        var n = Math.floor(handSize / (this.maxDamage - this.minDamage + 1))
        for (var i = this.minDamage; i <= this.maxDamage; i++) {
            var card = deck.find(n => n.attack == i)
            if (!card) {
                card = new Ally('Ally Damage ' + i + ' Cost: ' + cost, '', 0, i, 0)
            }
            for (var j = 0; j < n; j++) {
                hand.push(card)
            }
        }
        while(hand.length < handSize){
            hand.push(new Ally('Ally Damage ' + 0 + ' Cost: ' + cost, '', 0, 0, 0))
        }
        return hand
    }
}

export class DrawFromTopOfDeckHandBuilder extends BaseHandBuilder{
    constructor(minDamage, maxDamage) {
        super();
        this.minDamage = minDamage
        this.maxDamage = maxDamage
    }
    
    buildHand = function(deck, handSize){
        var hand = []
        while(hand.length < handSize){
            var card = deck.shift()
            if (card.attack >= this.minDamage && card.attack <= this.maxDamage) {
                hand.push(card)
            }else{
                hand.push(new Ally('Ally Damage ' + i + ' Cost: ' + cost, '', 0, i, 0))
                deck.push(card)
            }
        }
        return hand
    }
}

