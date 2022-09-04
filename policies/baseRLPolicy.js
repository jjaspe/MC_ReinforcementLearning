import { BasePolicy } from "./basePolicy.js";
import { config } from "../config.js";

export class BaseRLPolicy extends BasePolicy{
    constructor(encoder, predictionPicker, learningRate = 0.1) {
      super()
      this.history = []
      this.encoder = encoder
      this.learningRate = learningRate;
      this.predictionPicker = predictionPicker
      this.lenUniqueCards = config.MAX_HERO_ALLY_ATTACK - config.MIN_HERO_ALLY_ATTACK + 1 
      // bind this for combinationToColumnTensor
      this.combinationToColumnTensor = this.combinationToColumnTensor.bind(this)
      this.pickedActions = []
    }
  
    onMatchStart = function() {
      this.pickedActions = [];
      this.turns = 0;
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