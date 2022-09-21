import tensorflow as tf
from config import log

class SinglePassOptimizer:
    def __init__(self, gameInitializer, policy, scorer):
        self.gameInitializer = gameInitializer
        self.policy = policy
        self.scorer = scorer

    def optimize(self, epochs=100):
        victories = 0
        history = []
        scores = []
        for x in range(epochs):
            self.policy.onMatchStart()
            game = self.gameInitializer()
            isVictory = game.start()
            victories += (1 if isVictory else 0)
            score = self.scorer.scoreGame(isVictory, game.world)
            log('Score:', score)
            scores.append(score)
            self.policy.update(score)
            history.append(100 * victories / (x + 1))
        return scores

class BatchPassPickBestOptimizer:
    def __init__(self, gameInitializer, policy, scorer, batchSize=20):
        self.gameInitializer = gameInitializer
        self.policy = policy
        self.encoder = self.policy.encoder
        self.scorer = scorer
        self.batchSize = batchSize

    def optimize(self, epochs=100):
        victories = 0
        history = []
        scores = []
        for x in range(epochs):
            log('Starting epoch:', x)
            bestBatchScore = -float('inf')
            batchPickedActions = []
            for i in range(self.batchSize):
                self.policy.onMatchStart()
                game = self.gameInitializer()
                isVictory = game.start()
                victories += (1 if isVictory else 0)
                score = self.scorer.scoreGame(isVictory, game.world)
                if score > bestBatchScore:
                    bestBatchScore = score
                    batchPickedActions = self.policy.pickedActions
            log('Score:', bestBatchScore)
            scores.append(bestBatchScore)
            self.policy.update(bestBatchScore)
            history.append(100 * victories / (x + 1))
        return scores

class BatchPassOptimizer:
    def __init__(self, game, batches):
        self.game = game
        self.policy = game.ruleset.policy
        self.encoder = self.policy.encoder
        self.batches = batches

    def optimize(self, game, epochs=100):
        history = []
        totalVictories = 0
        for x in range(epochs):
            victories = 0
            batchUpdates = []
            for _pass in range(self.batches):
                self.policy.onMatchStart()
                isVictory = self.game.start()
                victories += (1 if isVictory else 0)
                score = self.scoreGame(isVictory, self.game.world) / len(self.policy.cardIndecesPicked)
                for index in self.policy.cardIndecesPicked:
                    oneHotCard = self.encoder.getOneHotEncodedCardByIndex(index)
                    updates = [n * score for n in oneHotCard]
                    batchUpdates.append(updates)
            for update in batchUpdates:
                self.policy.updatePolicyMatrix(tf.tensor1d(update, 'float32'))
            history.append(100 * victories / self.batches)
            totalVictories += victories
        log(totalVictories)
        return history





