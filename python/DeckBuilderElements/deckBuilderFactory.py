from DeckBuilderElements.deckBuilders import *
from config import config, log

class DECK_BUILDER_TYPES:
    DAMAGE_ONLY= DamageOnlyDeckBuilder
    DAMAGE_AND_COST= DamageAndCostDeckBuilder
    DAMAGE_AND_SQUARED_COST = DamageAndSquaredCostDeckBuilder
    DAMAGE_AND_CUSTOM_COST = DamageAndCustomCostDeckBuilder
    NORMALIZED_DAMAGE_AND_SQUARED_COST = NormalizedDamageAndSquaredCostDeckBuilder

class DeckBuilderFactory:
    def makeDeckBuilder(deckBuilderType, handBuilder):
        minAttack = config.MIN_HERO_ALLY_ATTACK
        maxAttack = config.MAX_HERO_ALLY_ATTACK
        minCost = config.MIN_HERO_ALLY_COST
        maxCost = config.MAX_HERO_ALLY_COST
        deckBuilder = None
        if deckBuilderType == DECK_BUILDER_TYPES.DAMAGE_ONLY:
            deckBuilder = DamageOnlyDeckBuilder(minAttack, maxAttack)
        elif deckBuilderType == DECK_BUILDER_TYPES.DAMAGE_AND_COST:
            deckBuilder = DamageAndCostDeckBuilder(minAttack, maxAttack, minCost, maxCost)
        elif deckBuilderType == DECK_BUILDER_TYPES.DAMAGE_AND_SQUARED_COST:
            deckBuilder = DamageAndSquaredCostDeckBuilder(minAttack, maxAttack, minCost, maxCost)
        elif deckBuilderType == DECK_BUILDER_TYPES.DAMAGE_AND_CUSTOM_COST:
            deckBuilder = DamageAndCustomCostDeckBuilder(minAttack, maxAttack, minCost, maxCost)
        else:
            raise Exception('Unknown deck builder type: ' + str(deckBuilderType))
            
        deckBuilder.cards = deckBuilder.buildCards()
        deckBuilder.fullDeck = deckBuilder.buildFullDeck(deckBuilder.cards, config.DECK_SIZE)
        deckBuilder.fullDeck = deckBuilder.postBuilder.execute(deckBuilder.fullDeck)
        deckBuilder.handBuilder = handBuilder
        return deckBuilder
