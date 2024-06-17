# Blackjack game using Python Object Oriented Programming.
# By: Stephen Prahl Jr.

import random

print("\nWelcome to Blackjack!")
print("Rules:")
print("1. The goal of blackjack is to beat the dealer's hand without going over 21.")
print("2. Face cards are worth 10. Aces are worth 1 or 11, whichever makes a better hand.")
print("3. Each player starts with two cards, one of the dealer's cards is hidden until the end.")
print("4. To 'Hit' is to ask for another card. To 'Stand' is to hold your total and end your turn.")
print("5. If you go over 21, you bust and the dealer wins.")
print("6. The dealer will hit until their cards total 17 or higher.")
print("7. If the dealer busts, you win!")
print("8. If you and the dealer have the same total, it's a push and you keep your bet.")
print("9. Good luck!")
print('')

name = input("Please enter your name: ")
print(f"Hello {name}, and welcome to the table, enjoy the game!")
print('\nThe Dealer is dealing the cards.....\n')


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.cards = [Card(value, suit) for suit in suits for value in values]

    def shuffle(self):
        if len(self.cards) < 52:
            raise ValueError("Only full decks can be shuffled")
        random.shuffle(self.cards)
        return self

    def deal(self):
        if len(self.cards) == 0:
            raise ValueError("All cards have been dealt")
        return self.cards.pop()

class Hand:
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        self.value = 0
        has_ace = False
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value == "A":
                    has_ace = True
                    self.value += 11
                else:
                    self.value += 10
        if has_ace and self.value > 21:
            self.value -= 10

    def display(self, hide_dealer_card=True):
        if self.dealer:
            print("Dealer's Hand:")
            print(" <card hidden>")
            print("", self.cards[1])
        else:
            print("Player's Hand:")
            for card in self.cards:
                print("", card)
            print("Value:", self.value)

class Game:
    def __init__(self):
        pass

    def play(self):
        playing = True
        while playing:
            self.deck = Deck()
            self.deck.shuffle()

            self.player_hand = Hand()
            self.dealer_hand = Hand(dealer=True)

            for _ in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())

            self.player_hand.calculate_value()
            self.dealer_hand.calculate_value()

            self.player_hand.display()
            self.dealer_hand.display()

            game_over = False
            while not game_over:
                player_has_blackjack, dealer_has_blackjack = self.check_for_blackjack()
                if player_has_blackjack or dealer_has_blackjack:
                    game_over = True
                    self.show_blackjack_results(
                        player_has_blackjack, dealer_has_blackjack
                    )
                    continue

                choice = input("Do you want to [H]it, [S]tand or [Q]uit: ").lower()
                while choice not in ["h", "s", "q"]:
                    choice = input("Please enter 'H', 'S' or 'Q' only: ").lower()
                if choice == "h":
                    self.player_hand.add_card(self.deck.deal())
                    self.player_hand.calculate_value()
                    self.player_hand.display()
                    if self.player_is_over():
                        print("You have lost!")
                        game_over = True
                elif choice == "s":
                    while self.dealer_hand.value < 17:
                        self.dealer_hand.add_card(self.deck.deal())
                        self.dealer_hand.calculate_value()
                    self.dealer_hand.display()
                    if self.dealer_is_over():
                        print("Dealer busts, you win!")
                    else:
                        if self.player_hand.value > self.dealer_hand.value:
                            print("You win!")
                        elif self.player_hand.value == self.dealer_hand.value:
                            print("Push!")
                        else:
                            print("You have lost!")
                    game_over = True
                elif choice == "q":
                    print("Thanks for playing!")
                    playing = False
                    game_over = True

    def player_is_over(self):
        return self.player_hand.value > 21

    def dealer_is_over(self):
        return self.dealer_hand.value > 21

    def check_for_blackjack(self):
        player = False
        dealer = False
        if self.player_hand.value == 21 and len(self.player_hand.cards) == 2:
            player = True
        if self.dealer_hand.value == 21 and len(self.dealer_hand.cards) == 2:
            dealer = True

        return player, dealer

    def show_blackjack_results(self, player_has_blackjack, dealer_has_blackjack):
        if player_has_blackjack and dealer_has_blackjack:
            print("Push! Both players have blackjack!")
        elif player_has_blackjack:
            print("You have blackjack! You win!")
        elif dealer_has_blackjack:
            print("Dealer has blackjack! Dealer wins!")

if __name__ == "__main__":
    game = Game()
    game.play()