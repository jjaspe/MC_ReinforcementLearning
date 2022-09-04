import * as tf from '@tensorflow/tfjs';
import { config, print, debug } from './config.js';
import { BaseRLPolicy } from './baseRLPolicy.js';

export class PickCardAtATimePreferencePolicy extends BaseRLPolicy{
    constructor(encoder, predictionPicker, hiddenLayers = 0, learningRate = 0.1) {
      super(encoder, predictionPicker, learningRate);
      this.inputUnits = this.encoder.inputUnits;
      this.hiddenLayers = hiddenLayers;
      this.predictionPicker = predictionPicker;
      // this.model = tf.sequential();
      this.weights = tf.randomUniform([this.inputUnits, 1], 0, 1)
      // this.model.add(tf.layers.dense({units: config.HIDDEN_UNITS, inputShape: [this.inputUnits], useBias: true}));
      // this.model.add(tf.layers.dense({units: 1, useBias: true}));    
      // this.model.compile({loss: 'meanSquaredError', optimizer: tf.train.adam(this.learningRate)});  
      this.pastPredictionProbs = []
    }

    onMatchStart = function() {
      super().onMatchStart();
      this.pastPredictionProbs = [];
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
      var predictions = tf.matMul(inputMatrix, this.weights).squeeze()
      // Run each card through model to get probability of picking each card
      // var predictions = this.model.predict(inputMatrix)
      var pickedCardIndex = this.predictionPicker(predictions)
      var pickedCard = uniqueCards[pickedCardIndex]
      // Save picked Card as index array
      this.pickedActions.push(inputMatrix.arraySync()[pickedCardIndex])
      this.pastPredictionProbs.push(predictions.arraySync())
      print({damage:pickedCard.attack, cost:pickedCard.cost})

      // var newHistory = pickedCard.attack
      // this.history.push(newHistory)
      this.turns++;
      return [pickedCard]
    }
  }