import math
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from config import config, log, log, debug
from GameLayers.startGameLayer import DefaultStartGameLayer
from GameLayers.pickPayingCardsLayers import DefaultPickPayingCardsLayer
from GameLayers.pickAttackCardLayer import OneCardPickAttackCardsLayer
from GameLayers.attackLayer import UnderCostBudgetAttackLayer
from GameLayers.bossAttackLayer import DamageOnlyBossAttackLayer
from GameLayers.heroDefendLayer import DefaultHeroDefendLayer
from GameLayers.bossEndTurnLayer import DefaultBossEndTurnLayer
from GameLayers.exhaustAttackCardsLayer import DefaultExhaustAttackCardsLayer
from GameLayers.playerEndTurnLayer import TurnBudgetUsedPlayerEndTurnLayer
from GameLayers.drawCardsLayer import RebuildInitialHandDrawCardsLayer
from GameLayers.bossDrawLayer import DefaultBossDrawLayer
from policies.policyTypes import POLICY_TYPES
from models.match import Match
from DeckBuilderElements.handBuilders import HAND_BUILDER_TYPES, BaseHandBuilder
from game import Game
from GameLayers.gameScorer import ExpScorer
from cardEncoder import DamageAndCostEncoder
from optimizers import BatchPassPickBestOptimizer
from policies.policyFactory import PolicyFactory
from DeckBuilderElements.deckBuilderFactory import DeckBuilderFactory, DECK_BUILDER_TYPES
from rulesets.playerOneCardAtATimeRuleset import PlayerOneCardAtATimeRuleset

# explain this error: ValueError: source code string cannot contain null bytes
# this error means that the string contains a null byte, which is not allowed in python


learningRates = [1]
epochs = config.EPOCHS
deckBuilderType = DECK_BUILDER_TYPES.DAMAGE_AND_CUSTOM_COST
policyType = POLICY_TYPES.RL_PICK_CARD_AT_A_TIME

def OptimizeOverLearningRates(learningRates):
    results = []
    for i in range(len(learningRates)):
        handBuilder = BaseHandBuilder.makeHandBuilder(HAND_BUILDER_TYPES.N_OF_EACH)
        deckBuilder = DeckBuilderFactory.makeDeckBuilder(deckBuilderType,handBuilder)
        encoder = DamageAndCostEncoder(deckBuilder.cards)
        policy = PolicyFactory.makePolicy(policyType, encoder, learningRates[i])
        policy.predictionPicker = lambda n : policy.pickMax(n)
        game = Game(policy, deckBuilder, PlayerOneCardAtATimeRuleset())
        initializer = lambda  : game.makeMatch()
        scorer = ExpScorer(1, 1)
        optimizer = BatchPassPickBestOptimizer(initializer, policy, scorer, config.EXPLORE_BATCH_SIZE)

        startPolicy = policy.peek()
        log('Starting Policy:', startPolicy)
        scores = optimizer.optimize(epochs)
        results.append({'learningRate': learningRates[i], 'scores': scores})
        endPolicy = policy.peek()
        log('Ending Policy:', endPolicy)
        difference = tf.subtract(endPolicy, startPolicy)
        log('Policy Change:', difference)
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


