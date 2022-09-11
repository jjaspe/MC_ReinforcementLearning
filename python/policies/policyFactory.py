import config
from policyTypes import POLICY_TYPES
from manualUpdatePolicy import ManualUpdatesPolicy
from pickHandPermutationPolicy import  PickHandPermutationPolicy
from pickCardAtATimePolicy import PickCardAtATimeDensePolicy


class PolicyFactory:
    @staticmethod
    def makePolicy(policyType, encoder, learningRate):
        switcher = {
            POLICY_TYPES.MANUAL_UPDATES: ManualUpdatesPolicy(encoder, learningRate),
            POLICY_TYPES.RL_PICK_MULTIPLE_CARDS: PickHandPermutationPolicy(encoder, None, config.HIDDEN_LAYERS, learningRate),
            POLICY_TYPES.RL_PICK_CARD_AT_A_TIME: PickCardAtATimeDensePolicy(encoder, None, config.HIDDEN_LAYERS, learningRate)
        }
        return switcher.get(policyType, "Invalid policy type")