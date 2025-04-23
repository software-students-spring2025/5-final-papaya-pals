"""
This module contains functions to instantiate and manipulate the deck of cards
    for a blackjack game
"""

import random


class Deck:
    """This is the class declaration for a deck object"""

    cards = []

    def __init__(self, card_list):
        for card in card_list:
            self.cards.append(Card(card))

    def __str__(self):
        fin = ""
        for card in self.cards:
            if card.value == 10:
                fin += card.name + " "
            else:
                fin += card.name + "  "
        return fin

    def shuffle(self):
        """This function shuffles an existing deck of cards"""

        new_deck = []

        for i in range(len(self.cards), 0, -1):
            rand = random.randint(0, i - 1)

            new_deck.append(self.cards[rand])
            self.cards.remove(self.cards[rand])

        self.cards = new_deck
        return self

    def deal(self):
        """This function deals a single card from the deck"""

        return self.cards.pop()


class Card:
    """This is the class declaration for a card object"""

    value = 0
    suit = ""
    name = ""

    def __init__(self, name):
        """Create an instance of a card given an input of a name (2H, 4C, KS, AD, etc.)"""

        # type checking
        if not isinstance(name, str):
            raise TypeError(
                "to create a card instance, input a string with the format "
                "[value][first letter of suit] (example: 2H, 4D, KC, AS)"
            )
        if len(name) < 2 or len(name) > 3:
            raise TypeError(
                "to create a card instance, input a string with the format "
                "[value][first letter of suit] (example: 2H, 4D, KC, AS)"
            )

        # if name is three chars long (must be 10D, 10S, 10H, 10C - else throw error)
        if len(name) == 3:
            if name[0:2] != "10":
                raise ValueError("string is not recognizable as a card")
            if name[2:3] not in ["S", "H", "D", "C"]:
                raise ValueError("unknown suit in card instance - 1")
            self.suit = name[2:3]
            self.value = 10
            self.name = name
            return

        # For two char card names - get the value from the first char
        if name[0:1] == "A":
            self.value = 1
        elif name[0:1] == "J":
            self.value = 11
        elif name[0:1] == "Q":
            self.value = 12
        elif name[0:1] == "K":
            self.value = 13
        elif name[0:1] not in ["2", "3", "4", "5", "6", "7", "8", "9"]:
            raise ValueError("unknown card value")
        else:
            self.value = int(name[0:1])

        # get the suit from the second char
        if name[1:2] not in ["S", "H", "D", "C"]:
            raise ValueError("unknown suit in card instance - 2")
        self.suit = name[2:3]
        self.name = name

    def get_value(self):
        """This function returns the value of this card"""

        return self.value

    def get_name(self):
        """This function returns the name of this card"""

        return self.name


class Hand:
    """This is the class declaration for a hand object"""

    def __init__(self):
        self.total1 = 0
        self.total2 = 0
        self.cards = []
        self.images = []
        self.hidden = False

    def __str__(self):
        return (
            f"total: {str(self.total1)},{str(self.total2)}\ncards: "
            f"{str(self.cards)}\nimages: {str(self.images)}"
        )

    def deal(self, card, hidden):
        """Given a card as input, add this card to this hand"""

        if not isinstance(card, Card):
            raise TypeError("hand must be dealt a card object")

        # ace (special case)
        if card.value == 1:
            self.total1 += 1
            self.total2 += 11

        # all other cards
        else:
            self.total1 += card.value
            self.total2 += card.value

        self.cards.append(card.name)
        if hidden:
            self.images.append("back")
            self.hidden = True
        else:
            self.images.append(card.name)

    def reveal(self):
        """If hand has a hidden card (intended for dealer), permanently reveal this card now"""

        if "back" in self.images:
            self.images = self.cards
            self.hidden = False
