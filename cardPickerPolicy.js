import * as tf from '@tensorflow/tfjs';
import { math, model, sigmoid } from '@tensorflow/tfjs';
import { config, print, debug } from './config.js';
import { OneCardPickAttackCardsLayer } from './GameLayers/pickAttackCardLayer.js';

export class BasePolicy{
  static makePolicy = function(policyType, encoder, learningRate) {    
    switch (policyType) {
      case POLICY_TYPES.ONE_LAYER:
        return new OneLayerPolicy(encoder, learningRate)
      case POLICY_TYPES.RL_ARG_MAX:
        var policy = new HandPermutationDensePolicy(encoder, null, config.HIDDEN_LAYERS, learningRate)
        policy.predictionPicker = policy.pickMax;
        return policy;
      case POLICY_TYPES.RL_OVER_DIST:
        var policy = new HandPermutationDensePolicy(encoder, null, config.HIDDEN_LAYERS, learningRate)
        policy.predictionPicker = policy.pickIndexOverDistribution;
        return policy;
      case POLICY_TYPES.RL_PICK_CARD_AT_A_TIME_ARG_MAX:
        var policy = new PickCardAtATimeDensePolicy(encoder, null, config.HIDDEN_LAYERS, learningRate)
        policy.predictionPicker = policy.pickMax;
        return policy;
      default:
          throw 'Invalid policy type'
    }
  }

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
    // var highest = resultDistribution[0]
    // var highestIndex = 0
    // for (var i = 1; i < resultDistribution.length; i++) {
    //   if (resultDistribution[i] > highest) {
    //     highest = resultDistribution[i]
    //     highestIndex = i
    //   }
    // }
    // console.log("H:",resultDistribution[highestIndex], "%");
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

  pickMax = function(result) {
    var maxIndex = tf.argMax(result.arraySync()).arraySync()[0]
    console.log(maxIndex)
    return maxIndex
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

class OneLayerPolicy extends BasePolicy{
  constructor(encoder) {
    super()
    this.encoder = encoder
    this.learningRate = 0.1;
    var lenUniqueCards = config.MAX_HERO_ALLY_ATTACK - config.MIN_HERO_ALLY_ATTACK + 1
    this.policyTensor = tf.randomUniform([1, lenUniqueCards], 0, 1)
  }

  onMatchStart = function() {
    this.cardIndecesPicked = []
  }

  update = function (score) {
      var avgScore = score / this.cardIndecesPicked.length
      this.cardIndecesPicked.forEach((index) => {
          var oneHotCard = this.encoder.getOneHotEncodedCardByIndex(index)
          var updates = oneHotCard.map(n => n *= avgScore)
          this.updatePolicyMatrix(tf.tensor1d(updates, 'float32'))
        })
  }

  updatePolicyMatrix = function(policyTensor) {
    policyTensor = policyTensor.mul(this.learningRate)
    this.policyTensor = this.policyTensor.add(policyTensor)
  }

  pickCard = function(hand) {
    //run hand through policy network to find best one
    //turn hand to matrix then tensor
    var oneHotHand = this.encoder.oneHotEncodeCards(hand)
    var handTensor = tf.tensor(oneHotHand, [oneHotHand.length, oneHotHand[0].length])
    var result = handTensor.matMul(this.policyTensor, false, true)
    var maxIndexInHand = this.pickIndexOverDistribution(result)
    var indexInUniqueCards = this.encoder.getIndexOfCard(hand[maxIndexInHand])
    this.cardIndecesPicked.push(indexInUniqueCards)
    var card = hand[maxIndexInHand]
    return card
  }

  pickCards = function(hand) {
    var cards = [this.pickCard(hand)]
    return cards
  }

  peek = function(){
    return this.policyTensor.arraySync()
  }
}

class BaseRLPolicy extends BasePolicy{
  constructor(encoder, predictionPicker, learningRate = 0.1) {
    super()
    this.history = []
    this.encoder = encoder
    this.learningRate = learningRate;
    this.predictionPicker = predictionPicker
    this.lenUniqueCards = config.MAX_HERO_ALLY_ATTACK - config.MIN_HERO_ALLY_ATTACK + 1 
    // bind this for combinationToColumnTensor
    this.combinationToColumnTensor = this.combinationToColumnTensor.bind(this)
  }

  debugUpdate = function (inputs, labels, previous = []) {
    previous.push(this.peek())
    if (previous.length > 1) {
      var difference = tf.sub(previous[previous.length - 1], previous[0])
      debug1(difference.arraySync())      
    }    
    return this.updateModel(inputs, labels)
  }

  updateModel = async function(inputs, labels) {
    await this.model.fit(inputs, labels, {epochs: 1},);
  }

  // If combination doesn't have max number of cards, pad with 0 tensors
  padCombinationTensor = function(combinationTensor) {
    var maxLength = config.HERO_BUDGET
    var tensorLength = combinationTensor.shape[0]
    var padding = tf.zeros([maxLength - tensorLength, this.lenUniqueCards])
    return combinationTensor.concat(padding)
  }

  combinationToColumnTensor = function(combination) {
    
  }

  peek = function(){
    return this.model.getWeights()[0].arraySync()
  }
}

export class PickCardAtATimeDensePolicy extends BaseRLPolicy{
  constructor(encoder, predictionPicker, hiddenLayers = 0, learningRate = 0.1) {
    super(encoder, predictionPicker, learningRate);
    this.inputUnits = this.encoder.inputUnits;
    this.hiddenLayers = hiddenLayers;
    this.predictionPicker = predictionPicker;
    this.model = tf.sequential();
    this.model.initialWeights = tf.randomUniform([this.inputUnits, 1], 0, 1)
    this.model.add(tf.layers.dense({units: config.HIDDEN_UNITS, inputShape: [this.inputUnits], useBias: true}));
    this.model.add(tf.layers.dense({units: 1, useBias: true}));    
    this.model.compile({loss: 'meanSquaredError', optimizer: tf.train.adam(this.learningRate)});  
  }

  update = async function (score) {
    var avgScore = score / this.turns;
    var oneHotCards = this.pickedIndexCards.map(n => this.encoder.getOneHotEncodedCardByIndex([n]))
    var oneHotCombTensors = oneHotCards.map(this.encodedCardToColumnTensor).map(n => n.transpose())
    
    var labels = tf.tensor1d([avgScore], 'float32')
    await this.updateModel(oneHotCombTensors[0], labels)
  }

  onMatchStart = function() {
    this.pickedIndexCards = [];
    this.turns = 0;
  }

  getUniqueCards = function(hand) {
    var uniqueCards = []
    hand.forEach((card) => {
      if(uniqueCards.find(n => n.name == card.name) == undefined) {
        uniqueCards.push(card)
      }
    })
    return uniqueCards
  }

  encodedCardToColumnTensor = function(encodedCard, inputUnits) {
    var combinationTensor = tf.tensor(encodedCard,[inputUnits,1], 'float32') 
    return combinationTensor
  }

  pickCards = function(hand, world) {
    // encode cards into tensors
    var uniqueCards = this.getUniqueCards(hand);
    var inputTensors = uniqueCards.map(n => {
      var encoded = this.encoder.encodeCard(n, world)
      return this.encodedCardToColumnTensor(encoded, this.inputUnits)
    });
    // Build matrix of permutations
    var inputMatrix = inputTensors.reduce((a, b) => a.concat(b,1)).transpose()
    // Run each card through model to get probability of picking each card
    var predictions = this.model.predict(inputMatrix)
    // var prob22 = this.getProbabilityForPermutation([0,0,1,0], inputMatrix.arraySync(), predictions.arraySync())
    var pickedCardIndex = this.predictionPicker(predictions)
    var pickedCard = uniqueCards[pickedCardIndex]
    // var test = predictions.arraySync()
    // Save picked Card as index array
    var indecesInUniqueCards = this.encoder.getIndexOfCard(pickedCard)
    this.pickedIndexCards.push(indecesInUniqueCards)
    print({damage:pickedCard.attack, cost:pickedCard.cost})
    var newHistory = pickedCard.attack
    this.history.push(newHistory)
    this.turns++;
    return [pickedCard]
  }
}

export class HandPermutationDensePolicy extends BaseRLPolicy{
  constructor(encoder, predictionPicker, hiddenLayers=0, learningRate = 0.1) {
    super(encoder, predictionPicker, learningRate);
    this.inputUnits = this.lenUniqueCards*config.HERO_BUDGET;
    this.model = tf.sequential();
    this.model.initialWeights = tf.randomUniform([this.inputUnits, 1], 0, 1)
    this.model.add(tf.layers.dense({units: config.HIDDEN_UNITS, inputShape: [this.inputUnits], useBias: true}));
    // this.model.add(tf.layers.layerNormalization({axis: -1}));
    for(var i = 0; i < hiddenLayers; i++) {
      this.model.add(tf.layers.dense({units: config.HIDDEN_UNITS, inputShape: [config.HIDDEN_UNITS], useBias: true}));
    }
    this.model.add(tf.layers.dense({units: 1, useBias: true}));    
    this.model.compile({loss: 'meanSquaredError', optimizer: tf.train.adam(this.learningRate)});   
    this.oneHotCombinationToColumnTensor = this.oneHotCombinationToColumnTensor.bind(this)
  }
  
  update = async function (score) {
    var avgScore = score / this.turns;
    var oneHotCombinations = this.pickedIndexCombinations.map(n => n.map(this.encoder.getOneHotEncodedCardByIndex))
    var oneHotCombTensors = oneHotCombinations.map(this.oneHotCombinationToColumnTensor).map(n => n.transpose())
    
    var labels = tf.tensor1d([avgScore], 'float32')
    await this.updateModel(oneHotCombTensors[0], labels)
  }

  onMatchStart = function() {
    this.pickedIndexCombinations = [];
    this.turns = 0;
  }

  oneHotCombinationToColumnTensor = function(oneHotCombination, inputUnits) {
    var combinationTensor = tf.tensor(oneHotCombination,[oneHotCombination.length,this.lenUniqueCards], 'float32')
    var paddedCombinationTensor = this.padCombinationTensor(combinationTensor)
    // reshape combinationTensort to be 1 column
    var reshapedCombination = paddedCombinationTensor.reshape([inputUnits, 1])      
    return reshapedCombination
  }

  getProbabilityForPermutation = function(permutation, allPermutations, probabilities){
    for(var i = 0; i < allPermutations.length; i++){
      if(permutation.toString() === allPermutations[i].toString()){
        return probabilities[i]
      }
    }
    throw new Error('Permutation not found')
  }

  pickCards = function(hand) {
    // Make all combinations of up to n cards from hand
    var possiblePlayedCards = this.buildNCardPermutations(config.HERO_BUDGET, hand)
    var inputTensors = possiblePlayedCards.map(n => {
      var oneHotCombination = this.encoder.oneHotEncodeCards(n)
      return this.oneHotCombinationToColumnTensor(oneHotCombination, this.inputUnits)
    })
    // Build matrix of permutations
    var inputMatrix = inputTensors.reduce((a, b) => a.concat(b,1)).transpose()
    var perm22 = [0,0,1,0,0,0,1,0];
    var perm30 = [0,0,0,1,1,0,0,0];
    // Run each combination through model to get probability of picking each card
    var predictions = this.model.predict(inputMatrix)
    var prob22 = this.getProbabilityForPermutation(perm22, inputMatrix.arraySync(), predictions.arraySync())
    var pickedCombinationIndex = this.predictionPicker(predictions)
    var pickedCombination = possiblePlayedCards[pickedCombinationIndex]
    var test = predictions.arraySync()
    // Save picked combination as index array
    var indecesInUniqueCards = this.encoder.getIndecesOfCards(pickedCombination)
    this.pickedIndexCombinations.push(indecesInUniqueCards)
    print(pickedCombination.map(n => ({damage:n.attack, cost:n.cost})))
    var newHistory = pickedCombination.map(n => n.attack)
    this.history.push(newHistory)
    this.turns++;
    return pickedCombination
  }
}

export const POLICY_TYPES = {
  RL_PICK_CARD_AT_A_TIME_ARG_MAX: 'RL_PICK_CARD_AT_A_TIME_ARG_MAX',
  RL_ARG_MAX: 'RL_ARG_MAX',
  RL_OVER_DIST: 'RL_OVER_DIST',
  ONE_LAYER: 'ONE_LAYER'
}
