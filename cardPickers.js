function pickFirstCard(hand) {
  var card = hand.pop()
  return card
}

function pickBestCard(hand) {
  var card = hand[0]
  for (var x = 0; x < hand.length; x++) {
    if (hand[x].attack > card.attack) {
      card = hand[x]
    }
  }
  return card
}

class PickCardWithRL {
  constructor(policy) {
    this.policy = policy
  }

  pickCard = function(hand) {
    return this.policy.pickCard(hand)
  }
}

export {PickCardWithRL}