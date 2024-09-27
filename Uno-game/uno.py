from deck import *
from player import *

#----------------------------------Global variables----------------------------------------------#

# TODO: Initialise a draw pile deck

draw_pile = Deck()

# TODO: Initialise a discard pile

discard_pile = []

# TODO: Shuffle cards

draw_pile.shuffle_deck()

# TODO:Add card to discard pile and  make sure the card is a no action or wild card

discard_pile.append(draw_pile.pick_card()) # removes card from draw pile then adds it to discard pile

# TODO: Initialise a direction variable 1 being clockwise and -1 being counter-clockwise

play_direction = 1

# TODO: Ask user how many players to play
num_players = 0

# continue asking user number of player until a number between 2-10 is entered.
while not 2<= num_players <= 10:
    try:
        num_players = int(input("How many players would you like to play? "))
    except ValueError:
        print("Please enter an integer between 2 and 10.")
        num_players = int(input("How many players would you like to play? "))

# TODO: Initialise players and their hands

players = []
player_turn = 0
j = 1
skip = False
for i in range(num_players):
    name = input(f"Player {i + 1} what is your name? ")
    print("\nType 'com' for a computer player\n")
    if name == "com" and len(players) > 0:
        players.append(Player(f"com-{j}"))
        j += 1
    else:
        if name == "com":
            name = "_com"
        players.append(Player(name))

# TODO: Deal 7 cards to each player

# Loops through every player and deals 7 cards
for player in players:
    for _ in range(7):
        player.hand.append(draw_pile.pick_card()) # picks a card from draw pile and adds it to player hand
#------------------------------------------------FUNCTIONS-----------------------------------------------------#

def is_valid(card, hand):
    """
    Checks if the card is in the hand or not
    :param card -> list
    :param hand -> list
    :return: boolean
    """
    if card in hand:
        return True
    elif card[0] in ["wild", "wild-4"]:
        if ["wild", "any"] in hand or ["wild-4", "any"] in hand:
            return True
    return False


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


def show_hand(hand):
    global discard_pile
    """
    Prints the hand to the console.
    :param hand -> list
    :return: None
    """
    print("Your hand is:\n----------------------\n")
    for card in hand:
        print(f"{card}")
    print(f"\nCard to match: {discard_pile[-1]}")


def handle_played_card(card, current_player):
    """
    Handles the logic for playing a card, and updates the players hand.
    :param card -> list
    :param current_player -> player object
    :return: None
    """
    global discard_pile, skip
    if current_player.name == "com":
        pass
    else:
        # TODO: if card is valid pop it from player hand and add it to the discard pile
        current_player.hand.remove(card)

        # TODO: if card to play is a wild card then ask user the color they want

        if card[0] in ["wild", "wild-4"]:
            wild_card_color = input("What color would you like your wild card to be? ")
            discard_pile.append([card[0], wild_card_color]) # adds card to discard pile with the chosen color
        else:
            if card[0] == "skip":
                skip = True
            discard_pile.append(card)


def play(current_player):
    """
    Simulates a round for a human player    :param current_player:  -> object
    :return: None
    """
    global skip
    print(f"{current_player.name}'s turn\n")
# TODO: loop through each player and ask if they wanna discard or pick a card

    # TODO: show hand then ask user what card to discard.
    if not skip:
        show_hand(current_player.hand)
        pick_or_discard = input("Do you want to discard or pick a card? d/p : ")
        if pick_or_discard == "d":
            card_to_play = input_choice()
            # TODO: If they pick then pick card from draw pile otherwise check if the card they wanna discard is valid
            if card_to_play is not None:
                while not is_valid(card_to_play, current_player.hand):
                    card_to_play = input_choice()
                    if card_to_play is None:
                        current_player.pick(draw_pile.pick_card())
                        break
                if is_valid(card_to_play, current_player.hand):
                    handle_played_card(card_to_play, current_player)
            else:
                current_player.pick(draw_pile.pick_card())

        else:
            current_player.pick(draw_pile.pick_card()) # picks card from draw pile

    else:
        skip = False

while True:


    play(players[player_turn])


    if discard_pile[-1] == "reverse":
        play_direction *= -1

    player_turn += play_direction

    if player_turn == num_players:
        player_turn = 0
    elif player_turn == -1:
        player_turn = num_players - 1


# TODO: check if card to match is an action card if so then perform the action
# TODO: check if players still have cards then calculate points and end the game or round
