import tensorflow as tf
import numpy as np
from policies.basePolicy import BasePolicy
from config import config, log

class BaseRLPolicy(BasePolicy):
    def __init__(self, encoder, predictionPicker, learningRate = 0.1):
        super().__init__()
        self.history = []
        self.encoder = encoder
        self.learningRate = learningRate
        self.predictionPicker = predictionPicker
        self.lenUniqueCards = config.MAX_HERO_ALLY_ATTACK - config.MIN_HERO_ALLY_ATTACK + 1 
        self.pickedActions = []

    def onMatchStart(self):
        self.pickedActions = []
        self.turns = 0

    def debugUpdate(self, inputs, labels, previous = []):
        previous.append(self.peek())
        if len(previous) > 1:
            difference = tf.subtract(previous[len(previous) - 1], previous[0])
        return self.updateModel(inputs, labels)

    def updateModel(self, inputs, labels):
        self.model.fit(inputs, labels, epochs = 1)

    # If combination doesn't have max number of cards, pad with 0 tensors
    def padCombinationTensor(self, combinationTensor):
        maxLength = config.HERO_BUDGET
        tensorLength = combinationTensor.shape[0]
        padding = tf.zeros([maxLength - tensorLength, self.lenUniqueCards])
        return combinationTensor.concat(padding)

    def combinationToColumnTensor(self, combination):
        pass

    def peek(self):
        return self.model.get_weights()[0]






