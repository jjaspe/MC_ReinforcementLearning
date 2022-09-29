import tensorflow as tf
import numpy as np
import random
from config import config
from policies.basePolicy import BasePolicy

class ActionRLPolicy(BasePolicy):    
    def normState(self, state):
        return state / [config.HERO_HEALTH, config.BOSS_HEALTH]