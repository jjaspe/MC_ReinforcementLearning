import math
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits import mplot3d
from policies.pickCardAtATimeStatePreferencePolicyManual import PickCardAtATimeStatePreferencePolicyManual
from policies.PredictionPickers.predictionPickers import PredictionPickers
from StateBuilders.heroHealthBossHealthBuilder import HeroHealthBossHealthStateConstantBossAttackBuilder
from config import config, log, log, debug
from policies.policyTypes import POLICY_TYPES
from models.match import Match
from DeckBuilderElements.handBuilders import HAND_BUILDER_TYPES, BaseHandBuilder
from game import Game
from GameLayers.gameScorer import ExpScorer, LinearScorer, LogScorer
from cardEncoder import DamageAndCostEncoder
from optimizers import BatchPassOptimizer, BatchPassPickBestOptimizer, SinglePassOptimizer
from policies.policyFactory import PolicyFactory
from DeckBuilderElements.deckBuilderFactory import DeckBuilderFactory, DECK_BUILDER_TYPES
from rulesets.playerOneCardAtATimeRuleset import PlayerOneCardAtATimeRuleset
from policies.pickCardAtATimeStatePreferencePolicy import PickCardAtATimeStatePreferencePolicy

# explain this error: ValueError: source code string cannot contain null bytes
# this error means that the string contains a null byte, which is not allowed in python


def plot_weights(weights):    
    fig = plt.figure(figsize=(6, 3.2))
    ax = fig.add_subplot(111)
    ax.set_title('colorMap')
    plt.imshow(weights)        
    ax.set_aspect('equal')
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')

def plot_weights_mesh(policy):
    ax = plt.axes(projection='3d')
    x = np.linspace(0, config.HERO_HEALTH, config.HERO_HEALTH + 1, dtype=int)
    y = np.linspace(0, config.BOSS_HEALTH, config.BOSS_HEALTH + 1, dtype=int)
    X, Y = np.meshgrid(x, y)
    # make all tuples from x and y
    # Z = np.array([policy[x,y] for x,y in zip(np.ravel(X), np.ravel(Y))])
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.contour3D(y, x, policy, 50, cmap='binary')
    ax.set_xlabel('Hero Health')
    ax.set_ylabel('Boss Health')
    ax.set_zlabel('Weight')
    ax.view_init(60, 35)
    plt.show()

def OptimizeOverLearningRates(learningRates):
    results = []
    for i in range(len(learningRates)):
        handBuilder = BaseHandBuilder.makeHandBuilder(HAND_BUILDER_TYPES.N_OF_EACH)
        deckBuilder = DeckBuilderFactory.makeDeckBuilder(deckBuilderType,handBuilder)
        encoder = DamageAndCostEncoder(deckBuilder.cards)
        state_builder = HeroHealthBossHealthStateConstantBossAttackBuilder()
        # policy = PickCardAtATimeStatePreferencePolicy(state_builder, PredictionPickers.pickMax, learningRate=learningRates[i])
        policy = PickCardAtATimeStatePreferencePolicyManual(state_builder, PredictionPickers.pickMax, learningRate=learningRates[i])
        # policy = PolicyFactory.makePolicy(policyType, encoder, learningRates[i], PredictionPickers.pickMax)
        game = Game(policy, deckBuilder, PlayerOneCardAtATimeRuleset())
        initializer = lambda  : game.makeMatch()
        scorer = LinearScorer(1/max(config.BOSS_HEALTH, config.HERO_HEALTH))
        # optimizer = BatchPassPickBestOptimizer(initializer, policy, scorer, config.EXPLORE_BATCH_SIZE)
        optimizer = BatchPassOptimizer(initializer, policy, scorer, config.EXPLORE_BATCH_SIZE)

        startPolicy = policy.peek()
        log('Starting Policy:', startPolicy)
        scores = optimizer.optimize(epochs)
        results.append({'learningRate': learningRates[i], 'scores': scores})
        end_policy = policy.peek()
        log('Ending Policy:', end_policy)
        # plot_weights(end_policy)
    return results

learningRates = [0.1]
epochs = config.EPOCHS
deckBuilderType = DECK_BUILDER_TYPES.DAMAGE_AND_COST
policyType = POLICY_TYPES.RL_PICK_CARD_AT_A_TIME

cardsPerType = config.DECK_SIZE/(config.MAX_HERO_ALLY_ATTACK+1)
healthFrom2s = 2*cardsPerType
turnsFrom2s = math.floor(healthFrom2s/4)
otherTurns = (config.BOSS_HEALTH - healthFrom2s)/3
optScore = config.SCORE_MULTIPLIER * (config.HERO_HEALTH - config.BOSS_ATTACK*(turnsFrom2s+otherTurns))
log('Opt Score:', optScore)

results = OptimizeOverLearningRates(learningRates)

if(len(learningRates) > 1):
    fig, axs = plt.subplots(1, len(learningRates), sharey=True, tight_layout=True)
    # plot results in same screen
    for i in range(len(results)):            
        axs[i].plot(results[i]['scores'], label=('Learning Rate: ' + str(results[i]['learningRate'])))
else:
    plt.plot(results[0]['scores'], label=('Learning Rate: ' + str(results[0]['learningRate'])))

# plt.plot([optScore]*epochs, label='optimal score')
plt.legend()
plt.show()


