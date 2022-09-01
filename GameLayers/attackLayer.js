import { config } from '../config.js'


export default class UnderCostBudgetAttackLayer {
    execute = function(world) {
        var cards = world.attackCards
        for(var i = 0; i < cards.length; i++){
            var card = cards[i]
            if(card.cost <= world.turnBudget){
                world.boss.health = world.hero.attackAction(world.boss, card)
            }
            world.turnBudget -= card.cost
        }
    }
}