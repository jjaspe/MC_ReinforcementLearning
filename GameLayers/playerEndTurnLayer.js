export class DefaultContinueLayer {
    execute(world){
        world.isPlayerTurn = false
    }
}

export class TurnBudgetUsedContinueLayer {
    execute(world){
        world.isPlayerTurn = world.turnBudget > 0
    }
}