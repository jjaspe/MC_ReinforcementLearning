import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from cardEncoder import DamageAndCostEncoder
import config
from optimizers import BatchPassPickBestOptimizer
from policyFactory import PolicyFactory
from python.DeckBuilderElements.deckBuilders import DECK_BUILDER_TYPES
from GameLayers.startGameLayer import DefaultStartGameLayer
from GameLayers.pickPayingCardsLayers import DefaultPickPayingCardsLayer
from GameLayers.pickAttackCardLayer import OneCardPickAttackCardsLayer
from GameLayers.attackLayer import UnderCostBudgetAttackLayer
from GameLayers.bossAttackLayer import DamageOnlyBossAttackLayer
from GameLayers.heroDefendLayer import DefaultHeroDefendLayer
from GameLayers.bossEndTurnLayer import DefaultBossEndTurnLayer
from GameLayers.exhaustAttackCardsLayer import DefaultExhaustAttackCardsLayer
from GameLayers.playerEndTurnLayer import TurnBudgetUsedContinueLayer
from GameLayers.drawCardsLayer import RebuildInitialHandDrawCardsLayer
from GameLayers.bossDrawLayer import DefaultBossDrawLayer
from policies.basePolicy import POLICY_TYPES
from models.game import Game
from python.DeckBuilderElements.handBuilders import HAND_BUILDER_TYPES, BaseHandBuilder
from python.DeckBuilderElements.deckBuilders import BaseDeckBuilder
from rulesets import BaseRuleset
from gameScorer import ExpScorer

learningRates = [1]
epochs = config.EPOCHS
deckBuilderType = DECK_BUILDER_TYPES.DAMAGE_AND_CUSTOM_COST
policyType = POLICY_TYPES.RL_PICK_CARD_AT_A_TIME

def GameInitializer (ruleset, deckBuilder, policy):
    world = ruleset.makeWorld()
    world.heroHand = deckBuilder.buildHand(world.heroDeck, config.HAND_SIZE)
    layers = [
        DefaultStartGameLayer(),
        DefaultPickPayingCardsLayer(),
        OneCardPickAttackCardsLayer(policy),
        UnderCostBudgetAttackLayer(),
        DefaultExhaustAttackCardsLayer(),
        TurnBudgetUsedContinueLayer(),
        RebuildInitialHandDrawCardsLayer(world.heroHand),
        DefaultBossDrawLayer(),
        DamageOnlyBossAttackLayer(),
        DefaultHeroDefendLayer(),
        DefaultBossEndTurnLayer()
    ]
    game = Game(world, layers)
    return game

async def OptimizeOverLearningRates(learningRates):
    results = []
    for i in range(len(learningRates)):
        handBuilder = BaseHandBuilder.makeHandBuilder(HAND_BUILDER_TYPES.N_OF_EACH)
        deckBuilder = BaseDeckBuilder.makeDeckBuilder(deckBuilderType,handBuilder)
        encoder = DamageAndCostEncoder(deckBuilder.cards)
        policy = PolicyFactory.makePolicy(policyType, encoder, learningRates[i])
        policy.predictionPicker = lambda n : policy.pickMax(n)
        ruleset = BaseRuleset(policy, deckBuilder)
        initializer = lambda _ : GameInitializer(ruleset, deckBuilder, policy)
        scorer = ExpScorer(1, 1)
        optimizer = BatchPassPickBestOptimizer(initializer, policy, scorer, config.EXPLORE_BATCH_SIZE)

        startPolicy = policy.peek()
        print('Starting Policy:', startPolicy)
        scores = await optimizer.optimize(epochs)
        results.append({'learningRate': learningRates[i], scores: scores})
        endPolicy = policy.peek()
        print('Ending Policy:', endPolicy)
        difference = tf.sub(endPolicy, startPolicy).arraySync()
        print('Policy Change:', difference)




