import config
import tensorflow as tf
import numpy as np
import random
import math
from baseRLPolicy import BaseRLPolicy


class PickCardAtATimePreferencePolicy(BaseRLPolicy):
    def __init__(self, encoder, predictionPicker, hiddenLayers = 0, learningRate = 0.1):
        super().__init__(encoder, predictionPicker, learningRate)
        self.inputUnits = self.encoder.inputUnits
        self.hiddenLayers = hiddenLayers
        self.predictionPicker = predictionPicker
        # self.model = tf.sequential();
        self.weights = tf.random.uniform([self.inputUnits, 1], 0, 1)
        # self.model.add(tf.layers.dense({units: config.HIDDEN_UNITS, inputShape: [this.inputUnits], useBias: true}));
        # self.model.add(tf.layers.dense({units: 1, useBias: true}));    
        # self.model.compile({loss: 'meanSquaredError', optimizer: tf.train.adam(this.learningRate)});  
        self.pastPredictionProbs = []

    def onMatchStart(self):
        super().onMatchStart()
        self.pastPredictionProbs = []

    def update(self, score):
        avgScore = score / self.turns
        inputMatrix = tf.convert_to_tensor(self.pickedActions, np.float32)
        labels = tf.convert_to_tensor([avgScore for n in self.pickedActions], np.float32)
        self.updateModel(inputMatrix, labels)

    def getUniqueCards(self, hand):
        uniqueCards = []
        for card in hand:
            if len([c for c in uniqueCards if c.name == card.name]) == 0:
                uniqueCards.push(card)
        return uniqueCards

    def encodedCardToColumnTensor(self, encodedCard, inputUnits):
        combinationTensor = tf.convert_to_tensor(encodedCard,[inputUnits,1], np.float32) 
        return combinationTensor

    def pickCards(self, hand, world):
        # encode cards into tensors
        uniqueCards = self.getUniqueCards(hand)
        inputTensors =  [self.encodedCardToColumnTensor(self.encoder.encodeCard(card, world), self.inputUnits) 
            for card in uniqueCards]
        # Join tensors into one tensor
        inputMatrix = tf.concat(inputTensors, 1)
        predictions = tf.matmul(inputMatrix, self.weights).squeeze()
        # Run each card through model to get probability of picking each card
        # var predictions = this.model.predict(inputMatrix)
        pickedCardIndex = self.predictionPicker(predictions)
        pickedCard = uniqueCards[pickedCardIndex]
        # Save picked Card as index array
        self.pickedActions.push(inputMatrix.arraySync()[pickedCardIndex])
        self.pastPredictionProbs.push(predictions.arraySync())
        # log({damage:pickedCard.attack, cost:pickedCard.cost})

        # var newHistory = pickedCard.attack
        # this.history.push(newHistory)
        self.turns+=1
        return [pickedCard]



