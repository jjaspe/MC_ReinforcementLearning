import tensorflow as tf
import numpy as np
import random

class BasePolicy:
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




