from config import config

class HeroHealthBossHealthStateConstantBossAttackBuilder:
    def get_state_shape(self):
        return [config.HERO_HEALTH/config.BOSS_ATTACK,
         config.BOSS_HEALTH]

    def get_next_state(self, world, card):
        next_hero_health = max(0,world.hero.health - config.BOSS_ATTACK)
        next_boss_health = max(0,world.boss.health - card.attack)
        return [1.0*next_hero_health, 1.0*next_boss_health]