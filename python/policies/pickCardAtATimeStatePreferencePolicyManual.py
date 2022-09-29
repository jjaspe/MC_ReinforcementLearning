from policies.actionRLPolicy import ActionRLPolicy
from policies.basePolicy import BasePolicy
import tensorflow as tf
from config import config
import numpy as np

'''
    This is a policy that uses a hardcoded map of states to rewards
    to determine the best action to take.
    When deciding what card to pick, it will look at the next state
    based on choosing each card, and then use the hardcoded map to
    get the rewards of each possible next state, and use predictionPicker
    to pick a card based on the rewards.
    When updating the hardcoded map, it will take the score of the match,
    the states played during that match, the states refused during that match,
    and change the map in the direction that will make it closer to the score
    for the picked, and further from the score for the refused, scaled by the
    learning rate.
'''

class PickCardAtATimeStatePreferencePolicyManual(ActionRLPolicy):
    def __init__(self, state_builder, predictionPicker, learningRate = 0.1):
        super().__init__()
        self.learningRate = learningRate
        self.predictionPicker = predictionPicker
        self.not_picked_states = []
        self.picked_states = []
        self.state_builder = state_builder
        self.state_weights = np.zeros((config.HERO_HEALTH+1, config.BOSS_HEALTH+1), dtype=float)       
    
    def peek(self):
        return self.state_weights  
    
    def onMatchStart(self):
        self.not_picked_states = []
        self.picked_states = []
        self.turns = 0

    def getStateReward(self, state):
        return self.state_weights[int(state[0]), int(state[1])]

    def pickCards(self, hand, world):
        # for each card in hand, find the state that we would be in if we picked that card
        possible_states = [self.state_builder.get_next_state(world, card) for card in hand]
        # run each state through the model to get its predicted reward
        predictions = [self.getStateReward(state) for state in possible_states]
        # pick the card with the highest predicted reward
        picked_card_index = self.predictionPicker(predictions)
        # save the picked state
        self.picked_states.append(possible_states[picked_card_index]) 
        # save the not picked states
        not_picked_states = [possible_states[n] for n in range(len(possible_states)) if n != picked_card_index]
        self.not_picked_states.append(not_picked_states)
        # return the picked card
        picked_card = hand[picked_card_index]
        return [picked_card]

    def build_training_data(self, picked_states, not_picked_states, score):
        # make labels for picked states
        picked_labels_tensor = np.ones((len(picked_states), 1), dtype=float) * score
        # make one dimensional list with not picked states
        not_picked_states_tensor = np.concatenate(not_picked_states, 0)
        # make labels for not picked states
        not_picked_labels_tensor = np.ones((len(not_picked_states_tensor), 1), dtype=float) * -score
        # combine picked and not picked states
        inputs = np.concatenate([picked_states, not_picked_states_tensor], 0)
        # combine picked and not picked labels
        labels = np.concatenate([picked_labels_tensor, not_picked_labels_tensor], 0)
        return inputs, labels

    def update(self, score):
        input_states, labels = self.build_training_data(self.picked_states, self.not_picked_states, score)
        self.update_weights(input_states, labels)

    def batch_update(self, picked_states, not_picked_states, scores):
        # make an empty tensor to collect all inputs
        input_states = np.zeros((0, 2), dtype=float)
        labels = np.zeros((0, 1), dtype=float)
        for i in range(len(scores)):
            score = scores[i]
            picked_states_batch = picked_states[i]
            not_picked_states_batch = not_picked_states[i]
            inputs_batch, labels_batch = self.build_training_data(picked_states_batch, not_picked_states_batch, score)
            input_states = np.concatenate([input_states, inputs_batch], 0)
            labels = np.concatenate([labels, labels_batch], 0)

        self.update_weights(input_states, labels)

    def update_weights(self, input_states, labels):
        for i in range(len(labels)):
            # cast input_stats[i] to int
            indeces = input_states[i].astype(int)
            change = self.learningRate * (labels[i] - self.state_weights[indeces[0], indeces[1]])
            self.state_weights[indeces[0], indeces[1]] += self.learningRate * change[0]
