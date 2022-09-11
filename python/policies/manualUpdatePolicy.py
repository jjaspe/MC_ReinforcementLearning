import random
from config import config
from policies.basePolicy import BasePolicy
import tensorflow as tf

class ManualUpdatesPolicy(BasePolicy):
    def __init__(self, encoder, learningRate):
        super().__init__()
        self.encoder = encoder
        self.learningRate = learningRate
        lenUniqueCards = config.MAX_HERO_ALLY_ATTACK - config.MIN_HERO_ALLY_ATTACK + 1
        # initialize policy tensor to random values
        self.policy = tf.random.uniform([lenUniqueCards, lenUniqueCards], 0, 1, 'float32')

    def onMatchStart(self):
        self.cardIndecesPicked = []

    def update(self, score):
        avgScore = score / self.cardIndecesPicked.length
        for index in self.cardIndecesPicked:
            oneHotCard = self.encoder.getOneHotEncodedCardByIndex(index)
            updates = [n * avgScore for n in oneHotCard]
            self.updatePolicyMatrix(tf.tensor1d(updates, 'float32'))

    def updatePolicyMatrix(self, policyTensor):
        policyTensor = policyTensor.mul(self.learningRate)
        self.policy = self.policy.add(policyTensor)

    def pickCard(self, hand):
        #run hand through policy network to find best one
        #turn hand to matrix then tensor
        oneHotHand = self.encoder.oneHotEncodeCards(hand)
        handTensor = tf.tensor(oneHotHand, [oneHotHand.length, oneHotHand[0].length])
        result = handTensor.matMul(self.policy, False, True)
        maxIndexInHand = self.pickIndexOverDistribution(result)
        indexInUniqueCards = self.encoder.getIndexOfCard(hand[maxIndexInHand])
        self.cardIndecesPicked.push(indexInUniqueCards)
        card = hand[maxIndexInHand]
        return card

    def pickCards(self, hand):
        cards = [self.pickCard(hand)]
        return cards

    def peek(self):
        return self.policy.arraySync()
