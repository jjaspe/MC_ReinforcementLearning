import tensorflow as tf
from config import config, log
from policies.baseRLPolicy import BaseRLPolicy

class PickHandPermutationPolicy(BaseRLPolicy):
    def __init__(self, encoder, predictionPicker, hiddenLayers=0, learningRate = 0.1):
        super().__init__(encoder, predictionPicker, learningRate)
        self.inputUnits = self.lenUniqueCards*config.HERO_BUDGET
        self.model = tf.keras.Sequential()
        self.model.initialWeights = tf.random.uniform([self.inputUnits, 1], 0, 1)
        self.model.add(tf.keras.layers.Dense(config.HIDDEN_UNITS, input_shape=(self.inputUnits,), use_bias=True))
        # self.model.add(tf.layers.layerNormalization({axis: -1}));
        for i in range(hiddenLayers):
            self.model.add(tf.keras.layers.Dense(config.HIDDEN_UNITS, input_shape=(config.HIDDEN_UNITS,), use_bias=True))
        self.model.add(tf.keras.layers.Dense(1, use_bias=True))
        self.model.compile(loss='meanSquaredError', optimizer=tf.keras.optimizers.Adam(self.learningRate))

    def update(self, score):
        avgScore = score / self.turns
        inputMatrix = tf.convert_to_tensor(self.pickedActions, dtype=tf.float32)
        labels = tf.convert_to_tensor([avgScore]*len(self.pickedActions), dtype=tf.float32)
        self.updateModel(inputMatrix, labels)

    def oneHotCombinationToColumnTensor(self, oneHotCombination, inputUnits):
        combinationTensor = tf.convert_to_tensor(oneHotCombination, dtype=tf.float32)
        combinationTensor = tf.reshape(combinationTensor, [combinationTensor.shape[0], self.lenUniqueCards])
        paddedCombinationTensor = self.padCombinationTensor(combinationTensor)
        # reshape combinationTensort to be 1 column
        reshapedCombination = tf.reshape(paddedCombinationTensor, [inputUnits, 1])
        return reshapedCombination

    def getProbabilityForPermutation(self, permutation, allPermutations, probabilities):
        for i in range(len(allPermutations)):
            if permutation == allPermutations[i]:
                return probabilities[i]
        raise Exception('Permutation not found')

    def pickCards(self, hand):
        # Make all combinations of up to n cards from hand
        possiblePlayedCards = self.buildNCardPermutations(config.HERO_BUDGET, hand)
        inputTensors = [self.oneHotCombinationToColumnTensor(self.encoder.oneHotEncodeCards(n), self.inputUnits) for n in possiblePlayedCards]
        # Build matrix of permutations
        inputMatrix = tf.concat(inputTensors, 1).transpose()
        # Run each combination through model to get probability of picking each card
        predictions = self.model.predict(inputMatrix)
        pickedCombinationIndex = self.predictionPicker(predictions)
        pickedCombination = possiblePlayedCards[pickedCombinationIndex]
        # Save actions for update
        self.pickedActions.append(inputMatrix.numpy()[pickedCombinationIndex])
        log(pickedCombination)
        newHistory = [n.attack for n in pickedCombination]
        self.history.append(newHistory)
        self.turns += 1
        return pickedCombination




