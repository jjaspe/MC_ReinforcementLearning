export class DefaultExhaustAttackCardsLayer {
    execute(world) {
    }
}

export class DiscardCardsExhaustAttackCardsLayer {
    execute(world) {
        world.attackCards.forEach(card => {
            var index = world.heroHand.indexOf(card)
            if (index != -1) {
                world.heroHand.splice(index, 1)
            }
        });
    }
}