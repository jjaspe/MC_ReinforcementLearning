from config import config

class HeroHealthBossHealthStateConstantBossAttackBuilder:
    def get_state_shape(self):
        return [config.HERO_HEALTH/config.BOSS_ATTACK,
         config.BOSS_HEALTH]

    def get_next_state(self, world, card):
        return [world.hero.health - config.BOSS_ATTACK, world.boss.health - card.attack]