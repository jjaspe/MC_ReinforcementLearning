import {config} from '../config.js'

export default class DefaultBossEndTurnLayer {
    execute = function(world){
        world.isPlayerTurn = true;
    }
}