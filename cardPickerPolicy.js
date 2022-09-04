import * as tf from '@tensorflow/tfjs';
import { config, print, debug } from './config.js';
import { BasePolicy } from './policies/basePolicy.js';
import { BaseRLPolicy } from './policies/baseRLPolicy.js';

export class PolicyFactory{    
  static makePolicy = function(policyType, encoder, learningRate) {    
    switch (policyType) {
      case POLICY_TYPES.MANUAL_UPDATES:
        return new ManualUpdatesPolicy(encoder, learningRate)
      case POLICY_TYPES.RL_PICK_MULTIPLE_CARDS:
        return new HandPermutationDensePolicy(encoder, null, config.HIDDEN_LAYERS, learningRate);
      case POLICY_TYPES.RL_PICK_CARD_AT_A_TIME:
        var policy = new PickCardAtATimeDensePolicy(encoder, null, config.HIDDEN_LAYERS, learningRate);
        return policy;
      default:
          throw 'Invalid policy type'
    }
  }
}

export const POLICY_TYPES = {
  RL_PICK_CARD_AT_A_TIME: 'RL_PICK_CARD_AT_A_TIME',
  RL_PICK_MULTIPLE_CARDS: 'RL_PICK_MULTIPLE_CARDS',
  MANUAL_UPDATES: 'MANUAL_UPDATES'
}

class ManualUpdatesPolicy extends BasePolicy{
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
    var inputMatrix = tf.tensor2d([...this.pickedActions], [this.pickedActions.length, this.inputUnits])
    var labels = tf.tensor1d([...this.pickedActions.map(n => avgScore)], 'float32')
    await this.updateModel(inputMatrix, labels)
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
    var testPred = predictions.arraySync()
    var testPeek = this.peek();
    var pickedCardIndex = this.predictionPicker(predictions)
    var pickedCard = uniqueCards[pickedCardIndex]
    // Save picked Card as index array
    this.pickedActions.push(inputMatrix.arraySync()[pickedCardIndex])
    print({damage:pickedCard.attack, cost:pickedCard.cost})
    // var newHistory = pickedCard.attack
    // this.history.push(newHistory)
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
    var inputMatrix = tf.tensor2d([...this.pickedActions], [this.pickedActions.length, this.inputUnits])
    var labels = tf.tensor1d([...this.pickedActions.map(n => avgScore)], 'float32')
    await this.updateModel(inputMatrix, labels)
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
    // Run each combination through model to get probability of picking each card
    var predictions = this.model.predict(inputMatrix)
    var pickedCombinationIndex = this.predictionPicker(predictions)
    var pickedCombination = possiblePlayedCards[pickedCombinationIndex]
    // var test = inputMatrix.arraySync()
    // Save actions for update
    this.pickedActions.push(inputMatrix.arraySync()[pickedCombinationIndex])
    print(pickedCombination.map(n => ({damage:n.attack, cost:n.cost})))
    var newHistory = pickedCombination.map(n => n.attack)
    this.history.push(newHistory)
    this.turns++;
    return pickedCombination
  }
}
