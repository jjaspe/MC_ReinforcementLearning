import math
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from policies.PredictionPickers.predictionPickers import PredictionPickers
from StateBuilders.heroHealthBossHealthBuilder import HeroHealthBossHealthStateConstantBossAttackBuilder
from config import config, log, log, debug
from policies.policyTypes import POLICY_TYPES
from models.match import Match
from DeckBuilderElements.handBuilders import HAND_BUILDER_TYPES, BaseHandBuilder
from game import Game
from GameLayers.gameScorer import ExpScorer, LogScorer
from cardEncoder import DamageAndCostEncoder
from optimizers import BatchPassPickBestOptimizer, SinglePassOptimizer
from policies.policyFactory import PolicyFactory
from DeckBuilderElements.deckBuilderFactory import DeckBuilderFactory, DECK_BUILDER_TYPES
from rulesets.playerOneCardAtATimeRuleset import PlayerOneCardAtATimeRuleset
from policies.pickCardAtATimeStatePreferencePolicy import PickCardAtATimeStatePreferencePolicy

# explain this error: ValueError: source code string cannot contain null bytes
# this error means that the string contains a null byte, which is not allowed in python


learningRates = [0.01]
epochs = config.EPOCHS
deckBuilderType = DECK_BUILDER_TYPES.DAMAGE_AND_COST
policyType = POLICY_TYPES.RL_PICK_CARD_AT_A_TIME

def OptimizeOverLearningRates(learningRates):
    results = []
    for i in range(len(learningRates)):
        handBuilder = BaseHandBuilder.makeHandBuilder(HAND_BUILDER_TYPES.N_OF_EACH)
        deckBuilder = DeckBuilderFactory.makeDeckBuilder(deckBuilderType,handBuilder)
        encoder = DamageAndCostEncoder(deckBuilder.cards)
        state_builder = HeroHealthBossHealthStateConstantBossAttackBuilder()
        policy = PickCardAtATimeStatePreferencePolicy(state_builder, PredictionPickers.pickMax,
            learningRate=learningRates[i])
        # policy = PolicyFactory.makePolicy(policyType, encoder, learningRates[i])
        game = Game(policy, deckBuilder, PlayerOneCardAtATimeRuleset())
        initializer = lambda  : game.makeMatch()
        scorer = LogScorer(1, 1)
        # optimizer = BatchPassPickBestOptimizer(initializer, policy, scorer, config.EXPLORE_BATCH_SIZE)
        optimizer = SinglePassOptimizer(initializer, policy, scorer)

        startPolicy = policy.peek()
        debug('Starting Policy:', startPolicy)
        scores = optimizer.optimize(epochs)
        results.append({'learningRate': learningRates[i], 'scores': scores})
        endPolicy = policy.peek()
        debug('Ending Policy:', endPolicy)
        # difference = tf.subtract(endPolicy, startPolicy)
        # log('Policy Change:', difference)
    return results

cardsPerType = config.DECK_SIZE/(config.MAX_HERO_ALLY_ATTACK+1)
healthFrom2s = 2*cardsPerType
turnsFrom2s = math.floor(healthFrom2s/4)
otherTurns = (config.BOSS_HEALTH - healthFrom2s)/3
optScore = config.SCORE_MULTIPLIER * (config.HERO_HEALTH - config.BOSS_ATTACK*(turnsFrom2s+otherTurns))
log('Opt Score:', optScore)

results = OptimizeOverLearningRates(learningRates)

# plot scores
for i in range(len(results)):
    plt.plot(results[i]['scores'], label='learningRate: '+str(results[i]['learningRate']))
# plt.plot([optScore]*epochs, label='optimal score')
# plt.legend()
plt.show()


