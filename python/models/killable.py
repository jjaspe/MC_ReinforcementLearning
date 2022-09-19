
from models.card import Card


class Killable(Card):
    def __init__(self, name, text, health, attack, thwart):
        super().__init__(name, text)
        self.health = health
        self.attack = attack
        self.status = 0
        self.thwart = thwart

    def is_dead(self):
        return self.health <= 0