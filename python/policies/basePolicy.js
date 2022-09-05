import * as tf from '@tensorflow/tfjs';
import { config, print, debug } from '../config.js';
import { POLICY_TYPES } from '../cardPickerPolicy.js';

export class BasePolicy{  
    sigmoid = function(x) {
      return 1 / (1 + Math.exp(-x))
    }
  
    static upByMin = function (probs){
      var lowest = probs[0]
      for (var i = 1; i < probs.length; i++) {
        if (probs[i][0] < lowest) {
          lowest = probs[i][0]
        }
      }
      var sm = probs.map(n => [n[0] + (-lowest)])
      return sm
    }
  
    pickIndexOverDistribution = function(result) {    
      // var sm = result.arraySync().map(n => this.sigmoid(n))
      var sm = BasePolicy.upByMin(result.arraySync())
      // get sum of all elements in sm
      var sum =  sm.reduce((a, b) => (a + Math.pow(b,3)), 0)
      // divide each element by sum
      var resultDistribution = sm.map(n => Math.pow(n,3) / sum)
      console.log("C:",resultDistribution[32], "%");
      var random = Math.random()
      var threshold = 0
      for (var i = 0; i < resultDistribution.length; i++) {
        threshold += resultDistribution[i]
        if(random < threshold) {
          return i
        }
      }
      return resultDistribution.length - 1
    }
  
    pickOverSoftmax = function(result) {
      var exps = result.arraySync().map(n => Math.exp(n))
      var sum = exps.reduce((a, b) => (a + b), 0)
      var probs = exps.map(n => n / sum)
      var random = Math.random()
      var threshold = 0
      for (var i = 0; i < probs.length; i++) {
        threshold += probs[i]
        if(random < threshold) {
          return i
        }
      }
      return probs.length - 1
    }
  
    pickMax = function(result) {
      var maxIndex = tf.argMax(result.arraySync()).arraySync()[0]
      // console.log(maxIndex)
      return maxIndex
    }  
  
    eGreedyPicker = function(result, epsilon) {
      var random = Math.random()
      if(random < epsilon) {
        return Math.floor(Math.random() * result.shape[1])
      } else {
        return this.pickMax(result)
      }
    }
  
    buildUpToNCardCombinations = function(n, cards) {
      var combinations = []
      if(cards.length == 0) {
        return [[]]
      } else if(n == 1) {
        return cards.map(n => [n]).concat([[]])
      } else if(n > cards.length) {
        return [[...cards]].concat([[]])
      } else {
        for (var i = 0; i < cards.length; i++) {
          var remainingCards = cards.slice(i + 1)
          var remainingCombinations = this.buildUpToNCardCombinations(n - 1, remainingCards)
          for (var j = 0; j < remainingCombinations.length; j++) {
            var combination = [cards[i]]
            combination = combination.concat(remainingCombinations[j])
            combinations.push(combination)
          }
        }
        combinations.push([])
      }
      return combinations
    }
  
    buildNCardCombinations = function(n, cards) {
      var combinations = []
      if(cards.length == 0) {
        return []
      } else if(n == 1) {
        return cards.map(n => [n])
      } else {
        for (var i = 0; i < cards.length; i++) {
          var remainingCards = cards.slice(i + 1)
          var remainingCombinations = this.buildNCardCombinations(n - 1, remainingCards)
          for (var j = 0; j < remainingCombinations.length; j++) {
            var combination = [cards[i]]
            combination = combination.concat(remainingCombinations[j])
            combinations.push(combination)
          }
        }
      }
      return combinations
    }
    
    buildNCardPermutations = function(n, remainingCards, previous = [[]]) {
      var permutations = []    
      if(n == 1){
        previous.forEach(prev => {
          remainingCards.forEach(card => {
            permutations.push([...prev].concat([card]))
          });
        });
      } else {
        // For each remaining card, add it to all previous,
        // remove card remainingCards
        // call build with new set of previous, new remainingCards, and n-1 
        // After each loop, add result to permutations
        remainingCards.forEach(card => {
          var newRemainingCards = remainingCards.slice(0)
          newRemainingCards.splice(remainingCards.indexOf(card), 1)
          var newPrevious = []
          previous.forEach(prev => {
            newPrevious.push([...prev, card])
          });
          var newPermutations = this.buildNCardPermutations(n-1, newRemainingCards, newPrevious)
          permutations = permutations.concat(newPermutations)
        });
      }
      return permutations
    } 
  }