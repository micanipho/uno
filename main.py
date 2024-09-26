import random
from player import Player
from deck import Deck
import sys, subprocess

#----------------------------GLOBAL VARIABLES------------------------------------#

draw_pile = Deck()
discard_pile = []
skip = False
wild_card = False
card_to_match = []
wild_card_color = ""
count = 0


#-------------------------------FUNCTIONS---------------------------------------#


def clear():
    """
    clears the terminal window
    :return:
    """
    if sys.platform == "win32" or sys.platform == "win64":
        subprocess.run('cls', shell=True)
    elif sys.platform == "linux" or sys.platform == "darwin":
        subprocess.run('clear', shell=True)


def input_choice():
    """
    asks user for input of card in the format value color (e.g 4 red)
    :return: list
    """
    card = (input("Enter your card (e.g 3 blue ): ")).split()
    while len(card) != 2:
        print("Please enter card value and color separated by a space i.e 4 red \n")
        card = (input("Enter your card (e.g 3 blue ): ")).split()
    return card


def deal(active_players):
    """
    :param active_players:
    :return: none

    deals 7 random cards to all players
    """
    for p in active_players:
        p.hand = draw_pile.deal_cards()


def com_play_round(com):
    """
        Simulate a round of the game for computer player
        :param com:
        :return:
        """
    global wild_card, card_to_match, wild_card_color, skip
    colors = ['blue', 'red', 'green', 'yellow']

    if card_to_match[0] == "draw-2":
        com.pick(draw_pile.pick_card())
        com.pick(draw_pile.pick_card())

    elif card_to_match[0] == "wild-4":
        for _ in range(4):
            com.pick(draw_pile.pick_card())

    if not skip:
        com_match = []
        if not wild_card:
            if com.hand.count(["wild", "any"]) > 0:
                com_match = ["wild", "any"]
            elif com.hand.count(["wild-4", "any"]) > 0:
                com_match = ["wild-4", "any"]
            else:
                for card in com.hand:
                    if card[0] == card_to_match[0]:
                        com_match = card
                        break
                    elif card[1] == card_to_match[1]:
                        com_match = card
                        break
        else:
            wild_card = False
            for card in com.hand:
                if card[0] == card_to_match[0]:
                    com_match = card
                    break
                elif card[1] == wild_card_color:
                    com_match = card
                    break

        if com_match:

            if com_match[0] == "skip":
                skip = True

            if com_match[0] in ["wild-4", "wild"]:
                wild_card = True
                wild_card_color = colors[(random.randint(0, 3))]

            com.discard_card(com_match)
            discard_pile.append(com_match)
            card_to_match = com_match

        else:

            com.hand.append(draw_pile.pick_card())

    else:

        skip = False


import random
from player import Player
from deck import Deck
import sys, subprocess

#----------------------------GLOBAL VARIABLES------------------------------------#

draw_pile = Deck()
discard_pile = []
skip = False
wild_card = False
card_to_match = []
wild_card_color = ""
count = -1


#-------------------------------FUNCTIONS---------------------------------------#



def clear():
    """
    Clears the terminal window based on the operating system.
    """
    if sys.platform == "win32" or sys.platform == "win64":
        subprocess.run('cls', shell=True)
    elif sys.platform == "linux" or sys.platform == "darwin":
        subprocess.run('clear', shell=True)


def shuffle_deck(deck):
    for _ in range(2):
        for i in range(len(deck)):
            j = random.randint(0, len(deck) - 1)
            deck[i] =  deck[j]
            deck[j] = deck[i]
    random.shuffle(deck)
    return deck


def input_choice():
    """
    Asks the user for input of a card in the format 'value color' (e.g., '4 red').

    :return: list containing the card value and color
    """
    while True:
        card = input("Enter your card (e.g., '3 blue' or 'p' to pick): ").strip().split()
        if len(card) == 2:
            return card
        elif card == ["p"]:
            return None
        print("Invalid input. Please enter a card value and color separated by a space (e.g., '4 red').\n")


def deal(active_players):
    """
    Deals 7 random cards to all players in the active players list.

    :param active_players: List of player objects who are currently active in the game.
    """
    for player in active_players:
        player.hand = draw_pile.deal_cards()


def com_play_round(com):
    """
    Simulates a round of the game for a computer player.

    :param com: The computer player object.
    """
    global wild_card, card_to_match, wild_card_color, skip


    # Handle draw actions for special cards
    if card_to_match[0] == "draw-2":
        com.pick(draw_pile.pick_card())
        com.pick(draw_pile.pick_card())
    elif card_to_match[0] == "wild-4":
        for _ in range(4):
            com.pick(draw_pile.pick_card())

    # Proceed only if the player is not skipped
    if not skip:
        com_match = com_find_matching_card(com.hand)
        if com_match:
            com_handle_played_card(com, com_match)
        else:
            com.hand.append(draw_pile.pick_card())
    else:
        skip = False


def com_find_matching_card(hand):
    """
    Finds a card in hand that matches the card to match.

    :param hand: List of cards in hand.
    :return: The first matching card or None.
    """
    if ["wild", "any"] in hand:
        return ["wild", "any"]
    elif ["wild-4", "any"] in hand:
        return ["wild-4", "any"]
    elif ["skip", card_to_match[1]] in hand:
        return ["skip", card_to_match[1]]
    elif ["draw-2", card_to_match[1]] in hand:
        return ["draw-2", card_to_match[1]]
    else:
        for card in hand:
            if card[0] == card_to_match[0] or card[1] == card_to_match[1]:
                return card
    return None


def com_handle_played_card(com, card):
    """
    Handles the action of the computer player playing a card.

    :param com: The computer player object.
    :param card: The card being played.
    """
    global wild_card, wild_card_color, skip, card_to_match


    if card[0] == "skip":
        skip = True
    if card[0] in ["wild-4", "wild"]:
        # make list of colors from computer hand
        colors = [card[1] for card in com.hand if card[1] != "any"]
        wild_card = True
        wild_card_color = random.choice(colors)

    com.discard_card(card)
    discard_pile.append(card)
    if card[0] in ["wild", "wild-4"]:
        card_to_match = [card[0], wild_card_color]
    else:
        card_to_match = card


def play_round(player):
    """
    Simulate a round of the game for player
    :param player:
    :return:
    """
    global card_to_match, skip, wild_card, wild_card_color
    print(f"\n{player.name}'s turn\n")

    if card_to_match[0] == "draw-2":
        player.pick(draw_pile.pick_card())
        player.pick(draw_pile.pick_card())

    elif card_to_match[0] == "wild-4":
        for _ in range(4):
            player.pick(draw_pile.pick_card())

    if not skip:
        print(f"Your hand: {player.hand}\nCard to match: {card_to_match}")

        pick_or_discard = input("Would you like to discard or play? (d/p) ")

        if pick_or_discard == "d":
            card_to_discard = input_choice()
            color = card_to_discard[1]
            value = card_to_discard[0]

            while card_to_discard not in player.hand:
                print("Please enter a matching card value and color from your hand.")
                card_to_discard = input_choice()
                value = card_to_discard[0]
                color = card_to_discard[1]

            if not wild_card:

                if value in ["wild", "wild-4"]:
                    wild_card_color = input("\nWhich color do you want : ")
                    wild_card = True

                else:
                    valid_card = value == card_to_match[0] or color == card_to_match[1]
                    while not valid_card:
                        print(f"Please enter a card matching {card_to_match} by value or color .")
                        card_to_discard = input_choice()
                        value = card_to_discard[0]
                        color = card_to_discard[1]

                card_to_discard = [value, color]

                player.discard_card(card_to_discard)
                discard_pile.append(card_to_discard)

                if value == "skip":
                    skip = True
                if value in ["wild", "wild-4"]:
                    card_to_match = [value, wild_card_color]
                else:
                    card_to_match = [value, color]
            else:
                wild_card = False
                if value in ["wild", "wild-4"]:
                    wild_card_color = input("\nWhich color do you want : ")
                    wild_card = True
                else:
                    valid_card = color == card_to_match[1]
                    while not valid_card:
                        print(f"Please enter a card matching {card_to_match} color.")
                        card_to_discard = input_choice()
                        value = card_to_discard[0]
                        color = card_to_discard[1]

                card_to_discard = [value, color]

                player.discard_card(card_to_discard)
                discard_pile.append(card_to_discard)

                if value == "skip":
                    skip = True
                if value in ["wild", "wild-4"]:
                    card_to_match = [value, wild_card_color]
                else:
                    card_to_match = [value, color]
        else:
            player.hand.append(draw_pile.pick_card())
    else:
        skip = False
    clear()


def main():
    global discard_pile, draw_pile, card_to_match, skip
    # Initialize players

    num_players = int(input("How many players would you like to play? "))

    players = []
    j = 1
    for i in range(num_players):
        name = input(f"Player {i + 1} what is your name? ")
        if name == "com" and len(players) > 0:
            players.append(Player(f"com{j}"))
            j += 1
        else:
            print("\nType 'com' for a computer player\n")
            if name == "com":
                name = "_com"
            players.append(Player(name))

    # deal cards to players

    deal(players)

    # Place one card to discard pile

    discard_pile.append(draw_pile.pick_card())
    card_to_match = discard_pile[0]
    while card_to_match in ["wild-4", "wild"]:
        card_to_match = draw_pile.pick_card()

    game_over = False
    rounds = 1
    print(f"\nRounds: {rounds}\n")

    # main loop of the game

    while not game_over:

        global winner, points, count

        # reverses order if reverse card is played
        if card_to_match[0] == "reverse":
            count *= -1
            if count < 0:
                count = len(players) - 1

        if count == len(players) - 1:
            count = 0
        else:
            count += 1

        # checks if there is a computer player or human player
        if players[count].name[0:3] == "com":
            com_play_round(players[count])
        else:
            _ = input("Press enter to continue...")
            play_round(players[count])

        if len(players[count].hand) == 2:
            for loser in players:
                if players[count] == loser:
                    continue
                players[count].calculate_points(loser.hand)

            if players[count].points > 500:
                winner = players[count].name
                points = players[count].points
                return
            else:
                rounds += 1
                print(f"Rounds: {rounds}\n")
                draw_pile.update_deck(discard_pile)
                discard_pile = []
                draw_pile.update_deck(shuffle_deck(draw_pile.deck))
                deal(players)
                discard_pile.append(draw_pile.pick_card())
                card_to_match = discard_pile[0]

        draw_pile.count_cards()
        if draw_pile.num_cards < len(players) * 7:
            draw_pile.update_deck(discard_pile)
            draw_pile.update_deck(shuffle_deck(draw_pile.deck))
            discard_pile = []




play = input("Would you like to play Uno? (y/n) ")
while play == 'y':
    global winner, points
    main()
    print(f"\nGame Over!\nThe winner is {winner} with {points} points\n")
    play = input("Would you like to play Uno again? (y/n) ")



def main():
    global discard_pile, draw_pile, card_to_match, skip
    # Initialize players
    num_players = 0
    while not 2 <= num_players <= 10:
        print("Please enter a number between 2 and 10.")
        try:
            num_players = int(input("How many players would you like to play? "))
        except ValueError:
            raise ValueError("Please enter an integer")

    print("\nType 'com' for a computer player\n")
    players = []
    j = 1
    for i in range(num_players):
        name = input(f"Player {i + 1} what is your name? ")
        if name == "com":
            players.append(Player(f"com{j}"))
            j += 1
        else:
            players.append(Player(name))

    # deal cards to players

    if draw_pile.num_cards < num_players * 7:
        draw_pile.update_deck(discard_pile)
        discard_pile = []

    deal(players)

    # Place one card to discard pile

    discard_pile.append(draw_pile.pick_card())
    card_to_match = discard_pile[0]

    while card_to_match in [["wild-4", "any"], ["wild", "any"]]:
        card_to_match = draw_pile.pick_card()

    game_over = False
    rounds = 1
    print(f"\nRounds: {rounds}\n")

    # Game flow between players

    while not game_over:
        global winner, points, count

        if card_to_match[0] == "reverse":
            count *= -1
            if count < 0:
                count = len(players) - 1

        if draw_pile.num_cards < num_players * 7 + 1:
            draw_pile.update_deck(discard_pile)
            discard_pile = []

        if players[count].name[0:3] == "com":
            com_play_round(players[count])
        else:
            play_round(players[count])

        if len(players[count].hand) == 2:
            for loser in players:
                if players[count] == loser:
                    continue
                players[count].calculate_points(loser.hand)

            if players[count].points > 200:
                winner = players[count].name
                points = players[count].points
                return
            else:
                rounds += 1
                print(f"Rounds: {rounds}\n")
                draw_pile.shuffle_deck()
                deal(players)
                discard_pile.append(draw_pile.pick_card())
                card_to_match = discard_pile[0]

        if count == len(players) - 1:
            count = 0
        else:
            count += 1


play = input("Would you like to play Uno? (y/n) ")
while play == 'y':
    global winner, points
    main()
    print(f"\nGame Over!\nThe winner is {winner} with {points} points\n")
    play = input("Would you like to play Uno again? (y/n) ")
