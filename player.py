class Player:

    def __init__(self, name):
        self.hand = []
        self.points = 0
        self.name = name

    def pick(self, card):
        self.hand.append(card)

    def discard_card(self, card):
        self.hand.remove(card)

    def calculate_points(self, hand):
        total = 0
        for card in hand:
            if card[0] in ["draw-2", "skip", "reverse"]:
                total += 20
            elif card[0] in ["wild-4", "wild"]:
                total += 50
            else:
                total += int(card[0])

        self.points += total
