import random
import sys
import time
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# ASCII Art for the game
logo = Fore.YELLOW + '''
  ____  _            _    _            _
 |  _ \\| |          | |  (_)          | |
 | |_) | | __ _  ___| | ___  __ _  ___| | __
 |  _ <| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
 | |_) | | (_| | (__|   <| | (_| | (__|   <
 |____/|_|\\__,_|\\___|_|\\_\\ |\\__,_|\\___|_|\\_\\
                        _/ |
                       |__/
'''

suits_symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Spades': '♠', 'Clubs': '♣'}
suits_colors = {'Hearts': Fore.RED, 'Diamonds': Fore.RED, 'Spades': Fore.BLUE, 'Clubs': Fore.BLUE}
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Card Class
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.color = suits_colors[suit]
        self.ascii_art = self.generate_ascii_art()

    def generate_ascii_art(self):
        symbol = suits_symbols[self.suit]
        display_value = self.value.ljust(2) if self.value != '10' else self.value
        art = f"""{self.color}
┌─────────┐
│ {display_value}      │
│         │
│    {symbol}    │
│         │
│      {display_value} │
└─────────┘"""
        return art

    def card_value(self):
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            return 11  # Will adjust later if needed
        else:
            return int(self.value)

# Deck Class
class Deck:
    def __init__(self):
        self.cards = []
        self.build_deck()

    def build_deck(self):
        for suit in suits_symbols.keys():
            for value in values:
                self.cards.append(Card(suit, value))
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

# Hand Class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # Keep track of aces for adjusting value

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.card_value()
        if card.value == 'A':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        # Adjust the value of ace from 11 to 1 if total is over 21
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# Functions for gameplay
def clear():
    print("\n" * 100)

def display_hands(player_hand, dealer_hand, show_dealer_card=False):
    clear()
    print(logo)
    # Dealer's hand
    if show_dealer_card:
        print(Fore.YELLOW + "Dealer's Hand:")
        print_hand(dealer_hand.cards)
        print(f"Value: {dealer_hand.value}\n")
    else:
        print(Fore.YELLOW + "Dealer's Hand:")
        hidden_card = """
{0}
┌─────────┐
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
└─────────┘""".format(Fore.WHITE)
        print(hidden_card)
        print_hand(dealer_hand.cards[1:])
        print("Value: ??\n")
    # Player's hand
    print(Fore.GREEN + "Your Hand:")
    print_hand(player_hand.cards)
    print(f"Value: {player_hand.value}\n")

def print_hand(cards):
    # Print all cards side by side
    lines = ['', '', '', '', '', '', '']
    for card in cards:
        art = card.ascii_art.split('\n')
        for i in range(7):
            lines[i] += art[i] + '  '
    for line in lines:
        print(line)

def player_choice():
    choice = ''
    while choice not in ['H', 'S']:
        choice = input(Fore.CYAN + "Do you want to [H]it or [S]tand? ").upper()
    return choice

def game():
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()

    # Deal initial two cards to player and dealer
    for _ in range(2):
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())

    playing = True

    while playing:
        display_hands(player_hand, dealer_hand)
        if player_hand.value == 21:
            print(Fore.GREEN + "Blackjack! You win!")
            return
        elif player_hand.value > 21:
            print(Fore.RED + "Bust! You lose.")
            return
        choice = player_choice()
        if choice == 'H':
            player_hand.add_card(deck.deal_card())
        else:
            playing = False

    # Dealer's turn
    display_hands(player_hand, dealer_hand, show_dealer_card=True)
    while dealer_hand.value < 17:
        print(Fore.YELLOW + "Dealer hits.")
        time.sleep(1)
        dealer_hand.add_card(deck.deal_card())
        display_hands(player_hand, dealer_hand, show_dealer_card=True)
        if dealer_hand.value > 21:
            print(Fore.GREEN + "Dealer busts! You win!")
            return

    # Compare hands
    if dealer_hand.value > player_hand.value:
        print(Fore.RED + "Dealer wins.")
    elif dealer_hand.value < player_hand.value:
        print(Fore.GREEN + "You win!")
    else:
        print(Fore.BLUE + "It's a tie!")

def main():
    play_again = 'Y'
    while play_again.upper() == 'Y':
        game()
        play_again = input(Fore.CYAN + "\nDo you want to play again? [Y/N]: ")

    print(Fore.MAGENTA + "Thanks for playing!")

if __name__ == "__main__":
    main()
