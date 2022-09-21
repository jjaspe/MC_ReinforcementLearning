from config import config, log
from policies.pickCardAtATimePolicyUpdateAllActions import PickCardAtATimeUpdateAllActionsPolicy
from policies.policyTypes import POLICY_TYPES
from policies.manualUpdatePolicy import ManualUpdatesPolicy
from policies.pickHandPermutationPolicy import  PickHandPermutationPolicy
from policies.pickCardAtATimePolicy import PickCardAtATimeDensePolicy


class PolicyFactory:
    @staticmethod
    def makePolicy(policyType, encoder, learningRate, predictionPicker):
        switcher = {
            POLICY_TYPES.MANUAL_UPDATES: ManualUpdatesPolicy(encoder, learningRate),
            POLICY_TYPES.RL_PICK_MULTIPLE_CARDS: PickHandPermutationPolicy(encoder, None, config.HIDDEN_LAYERS, learningRate),
            POLICY_TYPES.RL_PICK_CARD_AT_A_TIME: PickCardAtATimeUpdateAllActionsPolicy(encoder, predictionPicker, config.HIDDEN_LAYERS, learningRate)
        }
        return switcher.get(policyType, "Invalid policy type") 
