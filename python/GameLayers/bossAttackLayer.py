# the following is the above javascript code ported to python

import config

class DamageOnlyBossAttackLayer:
    def execute(self, world):
        world.hero.damageOnlyVillainPhase(world.boss.attack)
