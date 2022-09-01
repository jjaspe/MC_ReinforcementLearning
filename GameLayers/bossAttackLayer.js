export default class DamageOnlyBossAttackLayer{
    execute(world){
        world.hero.damageOnlyVillainPhase(world.boss.attack)
    }
}