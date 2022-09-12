import tensorflow as tf
from policies.basePolicy import BasePolicy
from policies.baseRLPolicy import BaseRLPolicy
from config import config, log

class PickCardAtATimeDensePolicy(BaseRLPolicy):
    def __init__(self, encoder, predictionPicker, hiddenLayers = 0, learningRate = 0.1):
        super().__init__(encoder, predictionPicker, learningRate)
        self.inputUnits = self.encoder.inputUnits
        self.hiddenLayers = hiddenLayers
        self.predictionPicker = predictionPicker
        self.model = tf.keras.Sequential()
        self.model.initialWeights = tf.random.uniform([self.inputUnits, 1], 0, 1)
        self.model.add(tf.keras.layers.Dense(config.HIDDEN_UNITS, input_shape = [self.inputUnits], use_bias = True))
        self.model.add(tf.keras.layers.Dense(1, use_bias = True))
        self.model.compile(loss = 'meanSquaredError', optimizer = tf.keras.optimizers.Adam(self.learningRate))
    
    def update(self, score):
        avgScore = score / self.turns
        inputMatrix = tf.constant(self.pickedActions, shape = [len(self.pickedActions), self.inputUnits])
        labels = tf.constant([avgScore for n in self.pickedActions],
         shape = [len(self.pickedActions), 1],
         dtype = tf.float32)
        self.updateModel(inputMatrix, labels)
    
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
        testPeek = self.peek()
        pickedCardIndex = self.predictionPicker(predictions)
        pickedCard = uniqueCards[pickedCardIndex]
        # Save picked Card as index array
        self.pickedActions.append(inputMatrix[pickedCardIndex])
        log({'damage':pickedCard.attack, 'cost':pickedCard.cost})
        # var newHistory = pickedCard.attack
        # self.history.push(newHistory)
        self.turns += 1
        return [pickedCard]




