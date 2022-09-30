from policies.actionRLPolicy import ActionRLPolicy
from policies.basePolicy import BasePolicy
import tensorflow as tf
from config import config
import matplotlib.pyplot as plt

class PickCardAtATimeStatePreferencePolicy(ActionRLPolicy):
    def __init__(self, state_builder, predictionPicker,
    hiddenLayers = 0, learningRate = 0.1):
        super().__init__()
        self.learningRate = learningRate
        self.hiddenLayers = hiddenLayers
        self.predictionPicker = predictionPicker
        self.not_picked_states = []
        self.picked_states = []
        self.state_builder = state_builder

        self.model = tf.keras.Sequential()
        initializer = tf.keras.initializers.constant(1/(max(config.BOSS_HEALTH, config.HERO_HEALTH)))
        self.model.add(tf.keras.layers.Dense(1, input_shape = [2], use_bias = True,
        kernel_initializer = initializer))
        # self.model.add(tf.keras.layers.Dense(1, use_bias = True, kernel_initializer = initializer))
        self.model.compile(optimizer = tf.keras.optimizers.Adam(self.learningRate)
        , loss='mean_squared_error'
        , metrics=['mse', 'mae'])   
        self.weight_history = [] 
    
    def peek(self):
        return self.model.get_weights()    
    
    def onMatchStart(self):
        self.not_picked_states = []
        self.picked_states = []
        self.turns = 0

    def pickCards(self, hand, world):
        # for each card in hand, find the state that we would be in if we picked that card
        possible_states = [self.state_builder.get_next_state(world, card) for card in hand]
        # run each state through the model to get its predicted reward
        predictions = self.model.predict(possible_states)
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
        # make list with picked states
        picked_states_tensor = tf.stack(picked_states)
        # make labels for picked states
        picked_labels_tensor = tf.ones([len(picked_states), 1], dtype=tf.float32) * score
        # make one dimensional list with not picked states
        not_picked_states_tensor = tf.stack(
            [state for state_list in not_picked_states for state in state_list])
        # make labels for not picked states
        not_picked_labels_tensor = tf.ones([len(not_picked_states_tensor), 1], dtype=tf.float32) * -score
        # combine picked and not picked states
        inputs = tf.concat([picked_states_tensor, not_picked_states_tensor], 0)
        # combine picked and not picked labels
        labels = tf.concat([picked_labels_tensor, not_picked_labels_tensor], 0)
        return inputs, labels

    def update(self, score):
        inputs, labels = self.build_training_data(self.picked_states, self.not_picked_states, score)
        # update model
        self.model.fit(inputs, labels, epochs = 10, verbose=0)

    def plot_weights(self):
        weights = self.weight_history
        fig = plt.figure(figsize=(6, 3.2))
        ax = fig.add_subplot(111)
        ax.set_title('weight history')
        plt.imshow(weights)        
        ax.set_aspect('equal')
        cax = fig.add_axes([-1, 1, -1, 1])
        cax.get_xaxis().set_visible(False)
        cax.get_yaxis().set_visible(False)
        cax.patch.set_alpha(0)
        cax.set_frame_on(False)
        plt.colorbar(orientation='vertical')

    def batch_update(self, picked_states, not_picked_states, scores):
        # make an empty tensor to collect all inputs
        inputs = tf.zeros([0, 2], dtype=tf.float32)
        labels = tf.zeros([0, 1], dtype=tf.float32)
        for i in range(len(scores)):
            score = scores[i]
            picked_states_batch = picked_states[i]
            not_picked_states_batch = not_picked_states[i]
            inputs_batch, labels_batch = self.build_training_data(picked_states_batch, not_picked_states_batch, score)
            inputs = tf.concat([inputs, inputs_batch], 0)
            labels = tf.concat([labels, labels_batch], 0)

        self.weight_history.append(self.model.get_weights()[0])
        # update model
        self.model.fit(inputs, labels, epochs = 10, verbose=0)
