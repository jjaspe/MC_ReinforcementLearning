import tensorflow as tf
from config import log
import numpy as np

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
            match = self.gameInitializer()
            isVictory = match.start()
            victories += (1 if isVictory else 0)
            score = self.scorer.scoreGame(isVictory, match.world)
            log('Score:', score)
            scores.append(score)
            self.policy.update(score)
            history.append(100 * victories / (x + 1))
        return scores

class BatchPassPickBestOptimizer:
    def __init__(self, initializer, policy, scorer, batchSize=20):
        self.initializer = initializer
        self.policy = policy
        # self.encoder = self.policy.encoder
        self.scorer = scorer
        self.batchSize = batchSize

    def optimize(self, epochs=100):
        victories = 0
        history = []
        scores = []
        for x in range(epochs):
            log('Starting epoch:', x)
            bestBatchScore = -float('inf')
            best_picked_states = []
            best_not_picked_states = []
            for i in range(self.batchSize):
                self.policy.onMatchStart()
                match = self.initializer()
                isVictory = match.start()
                victories += (1 if isVictory else 0)
                score = self.scorer.scoreGame(isVictory, match.world)
                if score > bestBatchScore:
                    bestBatchScore = score
                    best_picked_states = [self.policy.picked_states]
                    best_not_picked_states = [self.policy.not_picked_states]
            log('Score:', bestBatchScore)
            self.policy.batch_update(best_picked_states, best_not_picked_states, [bestBatchScore])
            scores.append(bestBatchScore)
            # self.policy.update(bestBatchScore)
            history.append(100 * victories / (x + 1))
        return scores

class BatchPassOptimizer:
    def __init__(self, initializer, policy, scorer, batches):
        self.policy = policy
        self.batches = batches
        self.initializer = initializer
        self.scorer = scorer

    def optimize(self, epochs=100):
        history = []
        totalVictories = 0
        all_scores = []
        for x in range(epochs):
            victories = 0
            batch_picked = []
            batch_not_picked = []
            scores = []
            for _pass in range(self.batches):
                self.policy.onMatchStart()
                match = self.initializer()
                isVictory = match.start()
                victories += (1 if isVictory else 0)
                score = self.scorer.scoreGame(isVictory, match.world)
                scores.append(score)
                batch_picked.append(self.policy.picked_states)
                batch_not_picked.append(self.policy.not_picked_states)
            self.policy.batch_update(batch_picked, batch_not_picked, scores)
            history.append(100 * victories / self.batches)
            totalVictories += victories
            # add all scores from scores into all_scores
            all_scores.extend(scores)
        log(totalVictories)
        return all_scores





