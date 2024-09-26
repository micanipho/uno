import random


class Deck:
    def __init__(self):
        self.deck = []
        self.num_cards = 0
        self.generate_deck()

    def generate_deck(self):
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'skip', 'reverse', 'draw-2']
        colors = ['blue', 'red', 'green', 'yellow']

        for n in numbers:
            if n == '0':
                self.deck += [[n, c] for c in colors]
            else:
                self.deck += [[n, c] for c in colors]
                self.deck += [[n, c] for c in colors]

        for a in range(4):
            self.deck += [['wild', 'any']]
            self.deck += [['wild-4', 'any']]

    def pick_card(self):
        return self.deck.pop(random.randint(0, len(self.deck) - 1))

    def deal_cards(self):
        hand = []
        for _ in range(7):
            hand.append(self.pick_card())

        return hand

    def count_cards(self):
        self.num_cards = len(self.deck)

    def update_deck(self, cards):
        self.deck += cards

    def shuffle_deck(self):
        for _ in range(2):
            for i in range(len(self.deck)):
                j = random.randint(0, len(self.deck) - 1)
                self.deck[i] = self.deck[j]
                self.deck[j] = self.deck[i]
        random.shuffle(self.deck)
