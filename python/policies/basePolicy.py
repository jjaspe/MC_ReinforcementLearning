import tensorflow as tf
import numpy as np
import random

class BasePolicy:
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def upByMin(self, probs):
        lowest = probs[0]
        for i in range(1, len(probs)):
            if probs[i][0] < lowest:
                lowest = probs[i][0]
        # sm = probs.map(n => [n[0] + (-lowest)])
        sm = [n[0] + (-lowest) for n in probs]
        return sm

    def pickIndexOverDistribution(self, result):
        sm = self.upByMin(result.numpy())
        sum = 0
        for n in sm:
            sum += np.power(n, 3)
        resultDistribution = [np.power(n, 3) / sum for n in sm]
        random = np.random.random()
        threshold = 0
        for i in range(0, len(resultDistribution)):
            threshold += resultDistribution[i]
            if random < threshold:
                return i
        return len(resultDistribution) - 1

    def pickOverSoftmax(self, result):
        # exps = result.numpy().map(n => np.exp(n))
        exps = [np.exp(n) for n in result.numpy()]
        sum = 0
        for n in exps:
            sum += n
        # probs = exps.map(n => n / sum)
        probs = [n / sum for n in exps]
        random = np.random.random()
        threshold = 0
        for i in range(0, len(probs)):
            threshold += probs[i]
            if random < threshold:
                return i
        return len(probs) - 1

    def pickMax(self, result):
        maxIndex = np.argmax(result)
        return maxIndex

    def eGreedyPicker(self, result, epsilon):
        random = np.random.random()
        if random < epsilon:
            return np.random.randint(0, result.shape[1])
        else:
            return self.pickMax(result)

    def buildUpToNCardCombinations(self, n, cards):
        combinations = []
        if len(cards) == 0:
            return [[]]
        elif n == 1:
            return [[n] for n in cards] + [[]]
        elif n > len(cards):
            return [n for n in cards].concat([[]])
        else:
            for i in range(0, len(cards)):
                remainingCards = cards[i + 1:]
                remainingCombinations = self.buildUpToNCardCombinations(n - 1, remainingCards)
                for j in range(0, len(remainingCombinations)):
                    combination = [cards[i]]
                    combination = combination.concat(remainingCombinations[j])
                    combinations.push(combination)
            combinations.push([])
        return combinations

    def buildNCardCombinations(self, n, cards):
        combinations = []
        if len(cards) == 0:
            return []
        elif n == 1:
            # return cards.map(n => [n])
            return [[n] for n in cards]
        else:
            for i in range(0, len(cards)):
                remainingCards = cards[i + 1:]
                remainingCombinations = self.buildNCardCombinations(n - 1, remainingCards)
                for j in range(0, len(remainingCombinations)):
                    combination = [cards[i]]
                    combination = combination.concat(remainingCombinations[j])
                    combinations.push(combination)
        return combinations

    def buildNCardPermutations(self, n, remainingCards, previous = [[]]):
        permutations = []
        if n == 1:
            for prev in previous:
                for card in remainingCards:
                    permutations.append(prev.copy().concat([card]))
        else:
            for card in remainingCards:
                newRemainingCards = remainingCards.slice(0)
                newRemainingCards.splice(remainingCards.indexOf(card), 1)
                newPrevious = []
                for prev in previous:
                    newPrevious.append([prev.copy(), card])
                newPermutations = self.buildNCardPermutations(n - 1, newRemainingCards, newPrevious)
                permutations = permutations.concat(newPermutations)
        return permutations




