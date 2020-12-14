import random

# First step is to set out the possible suits and values that a card can be

suits = ("Clubs", "Spades", "Hearts", "Diamonds")
ranks_values = {"Ace": 11, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9,
                "Ten": 10, "Jack": 10, "Queen": 10, "King": 10}


# Import the random module because likelihood is I'm going to use that to shuffle the deck


# Now to setup the class for a card

class Card:
    """This is the class for cards in the deck. It contains attributes, as well as a string value to provide a
    string of what the card is"""

    def __init__(self, rank, value, suit):
        self.rank = rank
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"


# Now to set out the class for a deck

class Deck(object):
    """Class for a deck in the game"""

    def __init__(self):
        self.deck = []
        for suit in suits:
            for item in ranks_values:
                card_n = Card(item, ranks_values[item], suit)
                self.deck.append(card_n)

    def __str__(self):
        self.card_deck_string = ""
        for card in self.deck:
            self.card_deck_string += str(card) + ", "
        return f"The cards currently still in the deck are:\n\n{self.card_deck_string}"

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


# Now we need a class for the hand of either the player or dealer. This should have methods to add a card to the hand,
# and then to count the total at all times

class Hand(object):
    """Hand class, intended for both the player and the dealer. Aces are tracked in order to be able to reduce the
    total later, if it comes to more than 21"""

    def __init__(self):
        self.cards = []
        self.total = 0
        self.aces = 0

    def __str__(self):
        self.card_hand_string = ""
        for card in self.cards:
            self.card_hand_string += str(card) + ", "
        return f"{self.card_hand_string}"

    def total_count(self):
        self.total = 0
        for card in self.cards:
            self.total += card.value
        while self.total > 21:
            if self.aces > 0:
                self.total -= 10
                self.aces -= 1
            else:
                break

    def print_hand_total(self, player_name="player"):
        Hand.total_count(self)
        print(f"The total value of the cards in the {player_name}'s hand is {self.total}")


# And finally, setting out the class for the player's pot of money

class Pot(object):
    """This is the class set for the players pot (their money to bet with)"""

    def __init__(self):
        self.money = int(input("How much money would you like to start with in your pot? "))
        self.bet = 0
        self.money_start = self.money

    def __str__(self):
        return f"You have {self.money} available in your pot"

    def win_bet(self):
        self.money += self.bet

    def lose_bet(self):
        self.money -= self.bet

    def place_bet(self):
        bet_accepted = "No"
        while bet_accepted == "No":
            try:
                self.bet = int(input("Please enter how much you would like to bet on this game as an integer value: "))
            except ValueError:
                print("Please make sure you enter an integer value")
                continue
            else:
                pass
            if self.bet > self.money:
                print("You do not have enough money to place that bet, please try again")
            else:
                print("Bet accepted, thank you")
                bet_accepted = "Yes"


# Now to define the functions required to play the game
# First is the function to add a card to the player's hand

def add_card(hand_add, deck_add):
    hand_add.cards.append(deck_add.deal())
    hand_add.total += hand_add.cards[len(hand_add.cards) - 1].value
    if hand_add.cards[len(hand_add.cards) - 1].rank == "Ace":
        hand_add.aces += 1


# Next function is for a player to take their turn. Rather than focus on which player is taking their turn, I've set it
# so that the turn is actually more interested in which hand is being played. I thought this would be fine as
# this game will be a game of only two turns, so I don't really need a player class to determine whose turn it is.
# Also, only one player has a pot, so it seemed pointless

def player_turn(player_hand_turn, player_hand_deck):
    player_turn_play = True
    while player_turn_play:
        player_hand_turn.print_hand_total("player")
        if player_hand_turn.total > 21:
            player_turn_play = False
            break
        turn_action = input("Would you like to stick or twist? ")
        if turn_action.upper() == "STICK":
            player_turn_play = False
            break
        elif turn_action.upper() == "TWIST":
            add_card(player_hand_turn, player_hand_deck)
            print(f"You've been dealt the {str(player_hand_turn.cards[len(player_hand_turn.cards) - 1])}")
            continue
        else:
            print("Please ensure you write either stick or twist")


# Now to write a function for the dealer's turn. This will work by casino blackjack rules,
# in that they will always play if their total is below 17, and will always stick on values at or above this.
# QUESTION: CAN THE DEALER HIT AFTER 17 IF THEY'RE LOSING?

def dealer_turn(dealer_hand_turn, dealer_hand_deck):
    dealer_turn_play = True
    while dealer_turn_play:
        dealer_hand_turn.print_hand_total("dealer")
        if dealer_hand_turn.total > 21:
            dealer_turn_play = False
            break
        elif dealer_hand_turn.total < 17:
            add_card(dealer_hand_turn, dealer_hand_deck)
            print(f"The dealer has been dealt the {str(dealer_hand_turn.cards[len(dealer_hand_turn.cards) - 1])}")
            continue
        else:
            dealer_turn_player = False
            break


# The next two functions are for printing the hand cards and total value at the beginning and end of the game. I NEED TO CHANGE THIS SO THAT THE DEALER'S FIRST CARD IS SHOWN, AS PER BLACKJACK RULES

def show_values_beginning(player_hand_beginning):
    print(f"The player and dealer have both been dealt 2 cards. Currently, the dealer's hand is secret, but the player "
          f"has been dealt {str(player_hand_beginning)}with a total of {player_hand_beginning.total}.")


def show_values_end(player_hand_end, dealer_hand_end):
    player_hand_end.total_count()
    dealer_hand_end.total_count()
    print(f"Both players have now stuck. At the end of the game, the player has ended with a hand of"
          f" {str(player_hand_end)}, with a total of {player_hand_end.total}.\n\n"
          f"The dealer has ended with a hand of {str(dealer_hand_end)}with a total of {dealer_hand_end.total}")


# Now for functions that are used for the different end scenarios

def player_busts(player_pot_bust):
    print("Oh no, you've gone bust!")
    player_pot_bust.lose_bet()
    print(f"You now have {player_pot_bust.money} available in your pot.")


def player_wins(player_pot_win):
    print("Well done, you won!")
    player_pot_win.win_bet()
    print(f"You now have {player_pot_win.money} available in your pot.")


def player_blackjack(player_pot_win2):
    print("Congratulations, you got a blackjack from your deal - you win!")
    player_pot_win2.win_bet()
    print(f"You now have {player_pot_win2.money} available in your pot.")


def dealer_busts(player_pot_win3):
    print("The dealer's gone bust, looks like you win!")
    player_pot_win3.win_bet()
    print(f"You now have {player_pot_win3.money} available in your pot.")


def dealer_wins(player_pot_lose2):
    print("Bad luck, the dealer's beat you!")
    player_pot_lose2.lose_bet()
    print(f"You now have {player_pot_lose2.money} available in your pot.")


def push():
    print("It's a tie, so neither player wins! Your money is returned, with no losses or winnings")


# Now, to play the game! First off, we want to set any required variables for the game to run, and define the class
# of any variables we're planning to use in the game. Important to note that setting the player_pot to be a Pot class
# will mean the first thing that happens regardless is the player will be asked to say how much money they want
# to start the game with

playing = True
player_pot: Pot = Pot()

print("Welcome to Bolton's Blackjack! The rules of the game are standard casino blackjack. You'll be playing against "
      "an automated dealer, who will stick at anything 17 or above. Good luck!")

# Now, we want this to be a game that can be played until the player
# # chooses to stop or runs out of money, so we'll put it in a big while loop

while playing:

    # Will have two loops, so that we can break this loop for different scenarios (e.g. early blackjack from deal)
    # to be able to get back to the player being asked if they'd like to play again quickly

    main_deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()

    game_live = True

    while game_live:

        print(f"Your total pot is currently at {player_pot.money}")
        player_pot.place_bet()

        print("We'll now shuffle, and deal to the player and dealer")

        main_deck.shuffle()

        add_card(player_hand, main_deck)
        add_card(dealer_hand, main_deck)
        add_card(player_hand, main_deck)
        add_card(dealer_hand, main_deck)

        show_values_beginning(player_hand)

        # Run a check for a blackjack right off the gate, as the player instantly wins if so

        player_hand.total_count()
        if player_hand.total == 21:
            player_blackjack(player_pot)
            game_live = False
            break

        print("Now that cards have been dealt, you'll take your turn")

        player_turn(player_hand, main_deck)
        if player_hand.total > 21:
            player_busts(player_pot)
            game_live = False
            break

        # Now to do the dealer turn. This should all be automated

        print("Now for the dealer's turn!")

        dealer_turn(dealer_hand, main_deck)
        if dealer_hand.total > 21:
            dealer_busts(player_pot)
            game_live = False
            break

        print("Both players have now played, and neither have gone bust! So, who's the winner?")

        if player_hand.total == dealer_hand.total:
            push()
            game_live = False
            break
        elif player_hand.total > dealer_hand.total:
            player_wins(player_pot)
            game_live = False
            break
        else:
            dealer_wins(player_pot)
            game_live = False
            break

    # Next bit asks the player if they'd like to play again

    carry_on_playing = input("Would you like to play the game again? Please enter yes or no ")
    input_accepted = False
    while not input_accepted:
        if carry_on_playing.upper() == "YES":
            input_accepted = True
            break
        elif carry_on_playing.upper() == "NO":
            print(f"Thanks for playing! You've left with a pot of {player_pot.money}")
            if player_pot.money > player_pot.money_start:
                print("Congratulations, you left with more money than you started with")
            elif player_pot.money < player_pot.money_start:
                print("Unlucky, you left with less money than you started with")
            input_accepted = True
            break
        else:
            print("Please ensure you write either yes or no")
    if carry_on_playing.upper() == "NO":
        break

# Aim is to set the game so it 0. Lets the player place a bet from their pot 1. Deals two player to each 2.
# Checks if the player has a blackjack right away 3. If not, let the player deal until they decide to stop or go bust
# 4. Do the same for the dealer 5. Decide the outcome at the end
