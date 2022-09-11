import tensorflow as tf
from policies.basePolicy import BasePolicy
from policies.baseRLPolicy import BaseRLPolicy
from config import config

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
    
    async def update(self, score):
        avgScore = score / self.turns
        inputMatrix = tf.constant(self.pickedActions, shape = [len(self.pickedActions), self.inputUnits])
        labels = tf.constant([avgScore for n in self.pickedActions],
         shape = [len(self.pickedActions), 1],
         dtype = tf.float32)
        await self.updateModel(inputMatrix, labels)
    
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
        inputTensors = [self.encodedCardToColumnTensor(self.encoder.encodeCard(n, world), self.inputUnits)
            for n in uniqueCards]
        # Build matrix of permutations
        inputMatrix = tf.concat(inputTensors, 1).transpose()
        # Run each card through model to get probability of picking each card
        predictions = self.model.predict(inputMatrix)
        testPred = predictions.arraySync()
        testPeek = self.peek()
        pickedCardIndex = self.predictionPicker(predictions)
        pickedCard = uniqueCards[pickedCardIndex]
        # Save picked Card as index array
        self.pickedActions.append(inputMatrix.arraySync()[pickedCardIndex])
        print({'damage':pickedCard.attack, 'cost':pickedCard.cost})
        # var newHistory = pickedCard.attack
        # self.history.push(newHistory)
        self.turns += 1
        return [pickedCard]



