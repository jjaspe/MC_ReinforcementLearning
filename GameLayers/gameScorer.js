import {config} from '../config.js'

export class DefaultScorer {
    constructor(healthPower){
        this.healthPower = healthPower
    }
    scoreGame = function(isVictory, world) {
        var baseScore = config.SCORE_MULTIPLIER
        var score = baseScore * (isVictory ? Math.pow(world.hero.health, this.healthPower) 
            : -Math.pow(world.boss.health, Math.floor(this.healthPower)))
        return score
    }
}

export class ExpScorer {
    constructor(powerConstant, linearConstant){    
        this.powerConstant = powerConstant
        this.linearConstant = linearConstant
    }

    scoreGame = function(isVictory, world) {
        var hero = Math.max(0, world.hero.health)
        var boss = Math.max(0, world.boss.health)
        var score = (isVictory ? 1 : -1)*Math.pow(10, this.powerConstant*(hero+boss))
        return score*this.linearConstant;
    }
}

export class LogScorer {
    constructor(c1, c2){
        this.c1 = c1
        this.c2 = c2
    }

    scoreGame = function(isVictory, world) {
        var hero = Math.max(0, world.hero.health)
        var boss = Math.max(0, world.boss.health)
        var score = isVictory?1:-1
        score *= this.c1*(Math.log(hero+boss))
        return score
    }
}