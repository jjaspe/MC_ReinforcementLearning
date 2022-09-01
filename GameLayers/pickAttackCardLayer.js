import {config, print, debug} from '../config.js'

export class OneCardPickAttackCardsLayer{
    constructor(policy){
        this.policy = policy
    }

    execute(world){
        world.attackCards = [this.policy.pickCards(world.heroHand, world)[0]]
        print('Picked Cards:', world.attackCards.map(n => n.attack))
    }
}

export class MultipleCardPickAttackCardsLayer{
    constructor(policy){
        this.policy = policy
    }

    execute(world){
        world.attackCards = this.policy.pickCards(world.heroHand, world)
        print('Picked Cards:', world.attackCards.map(n => n.attack))
    }
}