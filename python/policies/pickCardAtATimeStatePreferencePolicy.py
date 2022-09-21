from policies.basePolicy import BasePolicy
import tensorflow as tf
from config import config

class PickCardAtATimeStatePreferencePolicy(BasePolicy):
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
        initializer = tf.keras.initializers.Zeros()
        self.model.add(tf.keras.layers.Dense(config.HIDDEN_UNITS, input_shape = [2], use_bias = False,
        kernel_initializer = initializer))
        self.model.add(tf.keras.layers.Dense(1, use_bias = False, kernel_initializer = initializer))
        self.model.compile(optimizer = tf.keras.optimizers.Adam(self.learningRate)
        , loss='mean_squared_error'
        , metrics=['mse', 'mae'])    
    
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
        pickedCardIndex = self.predictionPicker(predictions)
        # save the picked state
        self.picked_states.append(possible_states[pickedCardIndex]) 
        # save the not picked states
        not_picked_states = [possible_states[n] for n in range(len(possible_states)) if n != pickedCardIndex]
        self.not_picked_states.append(not_picked_states)
        # return the picked card
        return [hand[pickedCardIndex]]

    def update(self, score):
        # make list with picked states
        picked_states = tf.stack(self.picked_states)
        # make labels for picked states
        picked_labels = tf.ones([len(self.picked_states), 1]) * score
        # make one dimensional list with not picked states
        not_picked_states = tf.stack(
            [state for state_list in self.not_picked_states for state in state_list])
        # make labels for not picked states
        not_picked_labels = tf.ones([len(not_picked_states), 1]) * -score
        # combine picked and not picked states
        inputs = tf.concat([picked_states, not_picked_states], 0)
        # combine picked and not picked labels
        labels = tf.concat([picked_labels, not_picked_labels], 0)
        # update model
        self.model.fit(inputs, labels, epochs = 1, verbose=0)
