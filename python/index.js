import { PolicyFactory, POLICY_TYPES } from './cardPickerPolicy.js'
import { BasePolicy } from './policies/basePolicy.js';
import { Game } from './models/game.js'
import { DECK_BUILDER_TYPES, BaseDeckBuilder } from './DeckBuilderElements/deckBuilders.js'
import * as tf from '@tensorflow/tfjs';
import {print, config, debug} from './config.js'
// import plot libraryt
// import {plot, PlotData} from 'nodeplotlib';
import {plot} from 'nodeplotlib';
import {BatchPassPickBestOptimizer, SinglePassOptimizer} from './optimizers.js'
import {DamageAndCostRuleset, DamageOnlyRuleset,} from './rulesets.js'
import { DamageAndCostEncoder, DamageEncoder } from './cardEncoder.js';
import DefaultBossDrawLayer from './GameLayers/bossDrawLayer.js';
import {RebuildInitialHandDrawCardsLayer} from './GameLayers/drawCardsLayer.js';
import {DefaultContinueLayer, TurnBudgetUsedContinueLayer} from './GameLayers/playerEndTurnLayer.js';
import DefaultPickPayingCardsLayer from './GameLayers/pickPayingCardsLayers.js';
import {OneCardPickAttackCardsLayer,
  MultipleCardPickAttackCardsLayer} from './GameLayers/pickAttackCardLayer.js';
import UnderCostBudgetAttackLayer from './GameLayers/attackLayer.js';
import DamageOnlyBossAttackLayer from './GameLayers/bossAttackLayer.js';
import DefaultHeroDefendLayer from './GameLayers/heroDefendLayer.js';
import DefaultBossEndTurnLayer from './GameLayers/bossEndTurnLayer.js';
import { DefaultExhaustAttackCardsLayer } from './GameLayers/exhaustAttackCardsLayer.js';
import { DefaultScorer, ExpScorer } from './GameLayers/gameScorer.js';
import { BaseHandBuilder, HAND_BUILDER_TYPES } from './DeckBuilderElements/handBuilders.js';
import { DefaultStartGameLayer } from './GameLayers/startGameLayer.js';

var learningRates = [1]
var epochs = config.EPOCHS
var deckBuilderType = DECK_BUILDER_TYPES.DAMAGE_AND_CUSTOM_COST
var policyType = POLICY_TYPES.RL_PICK_CARD_AT_A_TIME

function GameInitializer (ruleset, deckBuilder, policy) {
  var world = ruleset.makeWorld()
  world.heroHand = deckBuilder.buildHand(world.heroDeck, config.HAND_SIZE)
  var layers = [
    new DefaultStartGameLayer(),
    new DefaultPickPayingCardsLayer(),
    new OneCardPickAttackCardsLayer(policy),
    new UnderCostBudgetAttackLayer(),
    new DefaultExhaustAttackCardsLayer(),
    new TurnBudgetUsedContinueLayer(),
    new RebuildInitialHandDrawCardsLayer(world.heroHand),
    new DefaultBossDrawLayer(),
    new DamageOnlyBossAttackLayer(),
    new DefaultHeroDefendLayer(),
    new DefaultBossEndTurnLayer()
  ]
  var game = new Game(world, layers)
  return game
}

async function OptimizeOverLearningRates(learningRates){
  var results = []
  for(var i = 0; i < learningRates.length; i++) {
      var handBuilder = BaseHandBuilder.makeHandBuilder(HAND_BUILDER_TYPES.N_OF_EACH);
      var deckBuilder = BaseDeckBuilder.makeDeckBuilder(deckBuilderType,handBuilder);    
      var encoder = new DamageAndCostEncoder(deckBuilder.cards)
      var policy = PolicyFactory.makePolicy(policyType, encoder, learningRates[i])
      policy.predictionPicker = n => policy.pickMax(n);
      var ruleset = new DamageAndCostRuleset(policy, deckBuilder)
      var initializer = () => GameInitializer(ruleset, deckBuilder, policy);
      var scorer = new ExpScorer(1, 1);
      var optimizer = new BatchPassPickBestOptimizer(initializer, policy, scorer, config.EXPLORE_BATCH_SIZE);

      var startPolicy = policy.peek()
      print('Starting Policy:', startPolicy)
      var scores = await optimizer.optimize(epochs)
      results.push({learningRate: learningRates[i], scores: scores})
      var endPolicy = policy.peek()
      print('Ending Policy:', endPolicy)
      var difference = tf.sub(endPolicy, startPolicy).arraySync()
      print('Policy Change:', difference)

      var data = [{
        y: scores,
        xaxis: 'Iteration',
        yaxis: 'Scores',
        text: 'Policy Optimization Learning Rate:' + learningRates[i],
        // type : 'scatter',
        mode: 'markers',
        layout: [{
          title: 'Policy Optimization Learning Rate:' + learningRates[i],
          showlegend: true
        }]
      }]
      if(config.PLOT){
        plot(data)
      }     
      // var historySums = policy.history.map(x => x.reduce((a,b) => a + b, 0))
      // var data2 = [{
      //   y: historySums,
      //   xaxis: 'Iteration',
      //   yaxis: 'Damages Chosen',
      //   mode: 'markers',
      //   layout: [{
      //     showlegend: true
      //   }]
      // }]
      // if(config.PLOT){
      //   plot(data2)
      // }     
    }
}

var cardsPerType = config.DECK_SIZE/(config.MAX_HERO_ALLY_ATTACK+1)
var healthFrom2s = 2*cardsPerType
var turnsFrom2s = Math.floor(healthFrom2s/4)
var otherTurns = (config.BOSS_HEALTH - healthFrom2s)/3
var optScore = config.SCORE_MULTIPLIER * (config.HERO_HEALTH - config.BOSS_ATTACK*(turnsFrom2s+otherTurns))
console.log('Opt Score:' + optScore)

await OptimizeOverLearningRates(learningRates)



/**
   * @typedef {PlotData} NewType
   */

// quit process after 3 seconds
setTimeout(() => {
  process.exit(0)
}, 5000)

