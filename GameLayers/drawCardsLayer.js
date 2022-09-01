import { config } from '../config.js';

export class RebuildInitialHandDrawCardsLayer {
    constructor(hand){
        this.hand = hand
    }

    execute(world){
        world.heroHand = [...this.hand]
    }
}

export class DrawFromDeckDrawCardsLayer {
    execute(world){
        while(world.heroHand.length < config.HAND_SIZE)
            world.heroHand.push(world.heroDeck.pop())
    }
}