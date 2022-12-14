import tensorflow as tf
import numpy as np
import random
import config

def pickFirstCard(hand):
    card = hand.pop()
    return card

def pickBestCard(hand):
    card = hand[0]
    for x in range(len(hand)):
        if hand[x].attack > card.attack:
            card = hand[x]
    return card

class PickCardWithRL:
    def __init__(self, policy):
        self.policy = policy

    def pickCard(self, hand):
        return self.policy.pickCard(hand)




