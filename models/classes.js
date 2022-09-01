class Card {
  constructor(name, text,) {
    this.name = name
    this.text = text
    this.cost = 0
    this.resourcesGiven = 0
    this.limitPerTurn = 0
    this.color = null
    this.type = null
    this.subtype = null
    this.maxPerPlayer = 0
    this.maxPerDeck = 0
    this.uses = 0
  }
}

class Hand {
  constructor() {
    this.cards = []
  }
}



class Ally extends Card {
  constructor(name, text, health, attack,thwart) {
    super(name, text)
    this.health = health
    this.attack = attack
    this.status = 0
    this.thwart=thwart
  }
}

class Player {
  constructor() { }
}


class Resource {
  constructor(type) {
    this.type = type
  }
}

class Status {
  constructor(type) {
    this.type = type
  }
}

class Action {
  constructor() {
    this.conditions = null
    this.effects = null
  }
}

class Condition {
  constructor(name) {
    this.name = name
  }
}

class PlayHasXSubtypeCards extends Condition {
  constructor(amount, subtype) {
    this.amount = amount
    this.subtype = subtype
  }
}

class Effect {
  constructor(name) {
    this.name = name
  }
}
export {Card , Ally}