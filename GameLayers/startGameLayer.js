import {config} from '../config.js'

export class DefaultStartGameLayer {
    execute = function(world){
        world.isPlayerTurn = true;
        world.turnBudget = config.HERO_BUDGET;
    }
}