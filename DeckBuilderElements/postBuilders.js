export class DefaultPostBuilder {
    execute(cards){}
}

export class DeckShuffler{
    execute(cards){
        var shuffled = []
        while(cards.length > 0){
            var index = Math.floor(Math.random() * cards.length)
            shuffled.push(cards[index])
            cards.splice(index, 1)
        }
        return shuffled          
    }
}