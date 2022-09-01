import { print, config, debug } from '../config.js'

function drawCard(hand, deck, handSize) {
  if (deck.length < handSize) {
    deck = makeDeck(40)
    print('rebuilding deck')
  }
  for (var x = hand.length; x < handSize; x++) {
    hand.push(deck.pop())
  }
  return deck
}

function isdead(unit) {
  if (unit.health <= 0) {
    return true
  }
  else
    return false
}

function payForCards(playedCard, hand) {
  hand.splice(0, playedCard.cost)
}

class Game {
  constructor(world, layers) {
    this.world = world;
    this.layers = layers;
    this.startGameLayer = layers.shift();
    this.payForCardsLayer = layers.shift();
    this.pickAttackCardLayer = layers.shift();
    this.attackLayer = layers.shift();
    this.exhaustCardLayer = layers.shift();
    this.playerContinueTurnLayer = layers.shift();
    this.rebuildHandLayer = layers.shift();
    this.bossDrawLayer = layers.shift();
    this.bossAttackLayer = layers.shift();
    this.heroDefendLayer = layers.shift();
    this.bossEndTurnLayer = layers.shift();
  }

  start = function() {
    return this.playWithLayers()
  }

  playWithLayers = function() {
    var world = this.world;
    var hero = world.hero;
    var boss = world.boss;
    var gameEnd = false
    var victory = false
    var scheme = 0
    var handNumber = 0
    this.startGameLayer.execute(world);
    while(!gameEnd){
      print('Playing hand ' + handNumber++)
      while(this.world.isPlayerTurn){
        this.payForCardsLayer.execute(world);
        this.pickAttackCardLayer.execute(world);
        this.attackLayer.execute(world);
        this.playerContinueTurnLayer.execute(world);
        if(isdead(boss)) {
          gameEnd = true
          victory = true
          break;
        }
      }      
      if(!gameEnd){
        // play the rest of the layers
        while(!this.world.isPlayerTurn){
          this.rebuildHandLayer.execute(world);
          this.bossDrawLayer.execute(world);
          this.bossAttackLayer.execute(world);
          this.heroDefendLayer.execute(world);
          this.bossEndTurnLayer.execute(world);
          if (isdead(hero)) {
            gameEnd = true
            break
          }
        }
      }   
    }
    print(victory ? 'Victory' : 'Defeat')
    print('Hero:', hero.health, '   ', 'Boss:', boss.health)   
    return victory
  }

  playWithRuleset = function() {
    var hero = this.world.hero;
    var boss = this.world.boss;
    var heroDeck = this.world.heroDeck;
    var bossDeck = this.world.bossDeck;
    var hand = this.world.heroHand;
    var gameEnd = false
    var victory = false
    var scheme = 0
    var handNumber = 0
    while (gameEnd == false) {
      print('Playing hand ' + handNumber++)
      hero.playerPhase(this.world, hand)
      if (isdead(boss)) {
        print('Victory')
        print('Hero:', hero.health, '   ', 'Boss:', boss.health)
        gameEnd = true
        victory = true
      }
      else {
        //hero.villainPhase(boss.getDamage(enemyDeck))
        boss.villainPhase(hero, scheme, bossDeck)
        if (isdead(hero)) {
          gameEnd = true
          print('Defeat')
          print('Hero:', hero.health, '   ', 'Boss:', boss.health)
        }
        // else {
        //   heroDeck = drawCard(hand, heroDeck, 5)
        //   bossDeck = drawCard(enemyHand, bossDeck, 1)
        // }
      }
    }
    return victory
  }
}

export { Game }