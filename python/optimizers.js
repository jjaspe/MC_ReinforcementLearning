import { config, print, debug } from './config.js'
import * as tf from '@tensorflow/tfjs';

class SinglePassOptimizer {
    constructor(gameInitializer, policy, scorer) {
        this.gameInitializer = gameInitializer;
        this.policy = policy
        this.encoder = this.policy.encoder;
        this.scorer = scorer;
    }

    optimize = async function (epochs = 100) {
        var victories = 0
        var history = []
        var scores = []
        for (var x = 0; x < epochs; x++) {
            this.policy.onMatchStart()
            var game = this.gameInitializer()
            var isVictory = game.start()
            victories += (isVictory ? 1 : 0)
            var score = this.scorer.scoreGame(isVictory, game.world)
            print('Score:', score)
            scores.push(score)
            await this.policy.update(score)
            history.push(100 * victories / (x + 1))
        }
        return scores
    }
}

export class BatchPassPickBestOptimizer {
    constructor(gameInitializer, policy, scorer, batchSize=20) {
        this.gameInitializer = gameInitializer;
        this.policy = policy
        this.encoder = this.policy.encoder;
        this.scorer = scorer;
        this.batchSize = batchSize;
    }

    optimize = async function (epochs = 100) {
        var victories = 0
        var history = []
        var scores = []
        for (var x = 0; x < epochs; x++) {
            debug('Starting epoch:', x)
            var bestBatchScore = -Infinity
            var batchPickedActions = []
            for (var i = 0; i < this.batchSize; i++) {
                this.policy.onMatchStart()
                var game = this.gameInitializer()
                var isVictory = game.start()
                victories += (isVictory ? 1 : 0)
                var score = this.scorer.scoreGame(isVictory, game.world)
                if (score > bestBatchScore) {
                    bestBatchScore = score
                    batchPickedActions = this.policy.pickedActions;
                }
            }
            print('Score:', bestBatchScore)
            scores.push(bestBatchScore)
            await this.policy.update(bestBatchScore)
            history.push(100 * victories / (x + 1))
        }
        return scores
    }
}

class BatchPassOptimizer {
    constructor(game, batches) {
        this.game = game
        this.policy = game.ruleset.policy
        this.encoder = this.policy.encoder;
        this.batches = batches
    }

    optimize = function (game, epochs = 100) {
        var history = []
        var totalVictories = 0
        for (var x = 0; x < epochs; x++) {
            var victories = 0;
            var batchUpdates = [];
            for (var pass = 0; pass < this.batches; pass++) {
                this.policy.onMatchStart()
                var isVictory = this.game.start()
                victories += (isVictory ? 1 : 0)
                var score = this.scoreGame(isVictory, this.game.world) / this.policy.cardIndecesPicked.length
                this.policy.cardIndecesPicked.forEach((index) => {
                    var oneHotCard = this.encoder.getOneHotEncodedCardByIndex(index)
                    var updates = oneHotCard.map(n => n *= score)
                    batchUpdates.push(updates)
                })
            }
            batchUpdates.forEach(update => {
                this.policy.updatePolicyMatrix(tf.tensor1d(update, 'float32'))
            })
            // console.log(policy.policyTensor.arraySync())
            history.push(100 * victories / this.batches)
            totalVictories += victories
        }
        console.log(totalVictories)
        return history;
    }
}

export { SinglePassOptimizer, BatchPassOptimizer }