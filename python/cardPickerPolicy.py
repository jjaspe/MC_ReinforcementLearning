# import * as tf from '@tensorflow/tfjs';
# import { config, print, debug } from './config.js';
# import { BasePolicy } from './policies/basePolicy.js';
# import { BaseRLPolicy } from './policies/baseRLPolicy.js';
# 
# export class PolicyFactory{    
#   static makePolicy = function(policyType, encoder, learningRate) {    
#     switch (policyType) {
#       case POLICY_TYPES.MANUAL_UPDATES:
#         return new ManualUpdatesPolicy(encoder, learningRate)
#       case POLICY_TYPES.RL_PICK_MULTIPLE_CARDS:
#         return new HandPermutationDensePolicy(encoder, null, config.HIDDEN_LAYERS, learningRate);
#       case POLICY_TYPES.RL_PICK_CARD_AT_A_TIME:
#         var policy = new PickCardAtATimeDensePolicy(encoder, null, config.HIDDEN_LAYERS, learningRate);
#         return policy;
#       default:
#           throw 'Invalid policy type'
#     }
#   }
# }


# the following is the above commented javascript code converted to python

import tensorflow as tf
import numpy as np
import random
import config
from policies.baseRLPolicy import BaseRLPolicy
from policies.basePolicy import BasePolicy

POLICY_TYPES = {
    RL_PICK_CARD_AT_A_TIME: 'RL_PICK_CARD_AT_A_TIME',
    RL_PICK_MULTIPLE_CARDS: 'RL_PICK_MULTIPLE_CARDS',
    MANUAL_UPDATES: 'MANUAL_UPDATES'
}

class PolicyFactory:
    def makePolicy(policyType, encoder, learningRate):
        switcher = {
            POLICY_TYPES.MANUAL_UPDATES: ManualUpdatesPolicy(encoder, learningRate),
            POLICY_TYPES.RL_PICK_MULTIPLE_CARDS: HandPermutationDensePolicy(encoder, None, config.HIDDEN_LAYERS, learningRate),
            POLICY_TYPES.RL_PICK_CARD_AT_A_TIME: PickCardAtATimeDensePolicy(encoder, None, config.HIDDEN_LAYERS, learningRate)
        }
        return switcher.get(policyType, 'Invalid policy type')

class ManualUpdatesPolicy(BasePolicy):
    def __init__(self, encoder, predictionPicker, learningRate = 0.1):
        super().__init__(encoder, predictionPicker, learningRate)
        self.inputUnits = self.lenUniqueCards
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(config.HIDDEN_UNITS, input_shape=(self.inputUnits,), use_bias=True))
        self.model.add(tf.keras.layers.Dense(1, use_bias=True))
        self.model.compile(loss='meanSquaredError', optimizer=tf.keras.optimizers.Adam(self.learningRate))

    def update(self, score):
        avgScore = score / self.turns
        inputMatrix = tf.convert_to_tensor(self.pickedActions, dtype=tf.float32)
        labels = tf.convert_to_tensor([avgScore] * len(self.pickedActions), dtype=tf.float32)
        self.updateModel(inputMatrix, labels)

    def encodedCardToColumnTensor(self, encodedCard, inputUnits):
        combinationTensor = tf.reshape(tf.convert_to_tensor(encodedCard, dtype=tf.float32), [inputUnits, 1])
        return combinationTensor

    def pickCards(self, hand, world):
        # encode cards into tensors
        uniqueCards = self.getUniqueCards(hand)
        inputTensors = [self.encodedCardToColumnTensor(self.encoder.encodeCard(n, world), self.inputUnits) for n in uniqueCards]
        # Build matrix of permutations
        inputMatrix = tf.concat(inputTensors, 1)
        # Run each card through model to get probability of picking each card
        predictions = self.model.predict(inputMatrix)
        pickedCardIndex = self.predictionPicker(predictions)
        pickedCard = uniqueCards[pickedCardIndex]
        # Save picked Card as index array
        self.pickedActions.append(inputMatrix.numpy()[pickedCardIndex])
        print({'damage':pickedCard.attack, 'cost':pickedCard.cost})
        self.turns += 1
        return [pickedCard]

class PickCardAtATimeDensePolicy(BaseRLPolicy):
    def __init__(self, encoder, predictionPicker, hiddenLayers=0, learningRate = 0.1):
        super().__init__(encoder, predictionPicker, learningRate)
        self.inputUnits = self.lenUniqueCards
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(config.HIDDEN_UNITS, input_shape=(self.inputUnits,), use_bias=True))
        # self.model.add(tf.keras.layers.LayerNormalization(axis=-1))
        for i in range(hiddenLayers):
            self.model.add(tf.keras.layers.Dense(config.HIDDEN_UNITS, input_shape=(config.HIDDEN_UNITS,), use_bias=True))
        self.model.add(tf.keras.layers.Dense(1, use_bias=True))
        self.model.compile(loss='meanSquaredError', optimizer=tf.keras.optimizers.Adam(learningRate))
        self.encodedCardToColumnTensor = self.encodedCardToColumnTensor.bind(self)

    def update(self, score):
        avgScore = score / self.turns
        inputMatrix = tf.convert_to_tensor(self.pickedActions, dtype=tf.float32)
        labels = tf.convert_to_tensor([avgScore]*len(self.pickedActions), dtype=tf.float32)
        self.updateModel(inputMatrix, labels)

    def encodedCardToColumnTensor(self, encodedCard, inputUnits):
        combinationTensor = tf.reshape(tf.convert_to_tensor(encodedCard, dtype=tf.float32), [inputUnits, 1])
        return combinationTensor

    def pickCards(self, hand, world):
        # encode cards into tensors
        uniqueCards = self.getUniqueCards(hand)
        inputTensors = [self.encodedCardToColumnTensor(self.encoder.encodeCard(n, world), self.inputUnits) for n in uniqueCards]
        # Build matrix of permutations
        inputMatrix = tf.concat(inputTensors, 1)
        # Run each card through model to get probability of picking each card
        predictions = self.model.predict(inputMatrix)
        pickedCardIndex = self.predictionPicker(predictions)
        pickedCard = uniqueCards[pickedCardIndex]
        # Save picked Card as index array
        self.pickedActions.append(inputMatrix.numpy()[pickedCardIndex])
        print({'damage':pickedCard.attack, 'cost':pickedCard.cost})
        self.turns += 1
        return [pickedCard]


class HandPermutationDensePolicy(BaseRLPolicy):
    def __init__(self, encoder, predictionPicker, hiddenLayers=0, learningRate = 0.1):
        super().__init__(encoder, predictionPicker, learningRate)
        self.inputUnits = self.lenUniqueCards*config.HERO_BUDGET
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(config.HIDDEN_UNITS, input_shape=(self.inputUnits,), use_bias=True))
        for i in range(hiddenLayers):
            self.model.add(tf.keras.layers.Dense(config.HIDDEN_UNITS, input_shape=(config.HIDDEN_UNITS,), use_bias=True))
        self.model.add(tf.keras.layers.Dense(1, use_bias=True))
        self.model.compile(loss='meanSquaredError', optimizer=tf.keras.optimizers.Adam(self.learningRate))
        self.oneHotCombinationToColumnTensor = self.oneHotCombinationToColumnTensor.bind(self)

    def update(self, score):
        avgScore = score / self.turns
        inputMatrix = tf.convert_to_tensor(self.pickedActions, dtype=tf.float32)
        labels = tf.convert_to_tensor([avgScore]*len(self.pickedActions), dtype=tf.float32)
        self.updateModel(inputMatrix, labels)

    def oneHotCombinationToColumnTensor(self, oneHotCombination, inputUnits):
        combinationTensor = tf.convert_to_tensor(oneHotCombination, dtype=tf.float32)
        paddedCombinationTensor = self.padCombinationTensor(combinationTensor)
        # reshape combinationTensort to be 1 column
        reshapedCombination = tf.reshape(paddedCombinationTensor, [inputUnits, 1])      
        return reshapedCombination

    def getProbabilityForPermutation(self, permutation, allPermutations, probabilities):
        for i in range(len(allPermutations)):
            if permutation == allPermutations[i]:
                return probabilities[i]
        raise Exception('Permutation not found')

    def pickCards(self, hand, world):
        # Make all combinations of up to n cards from hand
        possiblePlayedCards = self.buildNCardPermutations(config.HERO_BUDGET, hand)
        inputTensors = [self.oneHotCombinationToColumnTensor(self.encoder.oneHotEncodeCards(n), self.inputUnits) for n in possiblePlayedCards]
        # Build matrix of permutations
        inputMatrix = tf.concat(inputTensors, 1)
        # Run each combination through model to get probability of picking each card
        predictions = self.model.predict(inputMatrix)
        pickedCombinationIndex = self.predictionPicker(predictions)
        pickedCombination = possiblePlayedCards[pickedCombinationIndex]
        # var test = inputMatrix.arraySync()
        # Save actions for update
        self.pickedActions.append(inputMatrix[pickedCombinationIndex].numpy())
        print(pickedCombination)
        newHistory = [n.attack for n in pickedCombination]
        self.history.append(newHistory)
        self.turns += 1
        return pickedCombination





