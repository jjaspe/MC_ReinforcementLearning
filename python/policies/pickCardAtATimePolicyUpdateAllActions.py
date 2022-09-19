import tensorflow as tf
from policies.basePolicy import BasePolicy
from policies.baseRLPolicy import BaseRLPolicy
from config import config, log

class PickCardAtATimeUpdateAllActionsPolicy(BaseRLPolicy):
    def __init__(self, encoder, predictionPicker, hiddenLayers = 0, learningRate = 0.1):
        super().__init__(encoder, predictionPicker, learningRate)
        self.inputUnits = self.encoder.inputUnits
        self.hiddenLayers = hiddenLayers
        self.predictionPicker = predictionPicker
        self.notPickedActions = []
        self.model = tf.keras.Sequential()
        self.model.initialWeights = tf.random.uniform([self.inputUnits, 1], 0, 1)
        self.model.add(tf.keras.layers.Dense(config.HIDDEN_UNITS, input_shape = [self.inputUnits], use_bias = True))
        self.model.add(tf.keras.layers.Dense(1, use_bias = True))
        self.model.compile(optimizer = tf.keras.optimizers.Adam(self.learningRate), loss='mean_squared_error')
    
    def update(self, score):
        avgScore = score / self.turns
        action_counts = len(self.pickedActions)
        # make a matrix of the picked actions
        pickedActionMatrix = tf.stack(self.pickedActions)
        pickedActionLabels = tf.constant([avgScore for n in self.pickedActions],
         shape = [action_counts, 1],
         dtype = tf.float32)
        nonPickedActionMatrix = tf.stack(self.notPickedActions)
        nonPickedActionLabels = tf.constant([-avgScore for n in self.notPickedActions],
            shape = [len(self.notPickedActions), 1],
            dtype = tf.float32)
        fullActionMatrix = tf.concat([pickedActionMatrix, nonPickedActionMatrix], 0)
        fullActionLabels = tf.concat([pickedActionLabels, nonPickedActionLabels], 0)
        self.updateModel(fullActionMatrix, fullActionLabels)
    
    def getUniqueCards(self, hand):
        uniqueCards = []
        for card in hand:
            if next((n for n in uniqueCards if n.name == card.name), None) == None:
                uniqueCards.append(card)
        return uniqueCards
    
    def encodedCardToColumnTensor(self, encodedCard, inputUnits):
        combinationTensor = tf.constant(encodedCard, shape = [inputUnits, 1], dtype = tf.float32)
        return combinationTensor
    
    def pickCards(self, hand, world):
        # encode cards into tensors
        uniqueCards = self.getUniqueCards(hand)
        encoded_cards = [self.encoder.encodeCard(n, world) for n in uniqueCards]
        inputTensors = [self.encodedCardToColumnTensor(n, self.inputUnits) for n in encoded_cards]
        # Build matrix of permutations
        inputMatrix = tf.transpose(tf.concat(inputTensors, 1))
        # Run each card through model to get probability of picking each card
        predictions = self.model.predict(inputMatrix)
        pickedCardIndex = self.predictionPicker(predictions)
        pickedCard = uniqueCards[pickedCardIndex]
        # Save picked Card as index array
        self.pickedActions.append(inputMatrix[pickedCardIndex])
        currentNotPickedActions = [inputMatrix[n] for n in range(len(inputMatrix)) if n != pickedCardIndex]
        self.notPickedActions.extend(currentNotPickedActions)
        log({'damage':pickedCard.attack, 'cost':pickedCard.cost})
        # var newHistory = pickedCard.attack
        # self.history.push(newHistory)
        self.turns += 1
        return [pickedCard]




