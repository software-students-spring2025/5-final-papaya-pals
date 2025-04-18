"""This module contains functions to instantiate and manipulate the deck of cards for a blackjack game"""

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
        new_deck = []

        for i in range(len(self.cards), 0, -1):
            rand = random.randint(0, i-1)

            new_deck.append(self.cards[rand])
            self.cards.remove(self.cards[rand])
        
        self.cards = new_deck
        return self
    
    def deal(self):
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
            raise TypeError("to create a card instance, input a string with the format [value][first letter of suit] (example: 2H, 4D, KC, AS)")
        if len(name) < 2 or len(name) > 3:
            raise TypeError("to create a card instance, input a string with the format [value][first letter of suit] (example: 2H, 4D, KC, AS)")
        
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
            raise ValueError('unknown card value')
        else:
            self.value = int(name[0:1])
        
        # get the suit from the second char
        if name[1:2] not in ["S", "H", "D", "C"]:
            raise ValueError("unknown suit in card instance - 2")
        self.suit = name[2:3]
        self.name = name


class Hand:

    total = []
    cards = []

    def __init__(self):
        self.total = [0]
        self.cards = []

    def deal(self, card):
        if not isinstance(card, Card):
            raise TypeError("hand must be dealt a card object")
        
        # ace (special case)
        if card.value == 1:
            if len(self.total) == 1:
                num = self.total[0]
                self.total[0] += 1
                self.total.append(num + 11)
            else:
                self.total[0] += 1
                self.total[1] += 11

            # remove the larger total if it's a bust
            if self.total[1] > 21:
                self.total.pop()

        # all other cards
        else:
            self.total[0] += card.value
            if len(self.total) == 2:
                self.total[1] += card.value
                if self.total[1] > 21:
                    self.total.pop()

        self.cards.append(card)

    def __str__(self):
        fin = str(self.total)
        fin += " - "
        for card in self.cards:
            if card.value == 10:
                fin += card.name + " "
            else:
                fin += card.name + "  "
        return fin


        

my_card_list = [
    "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AH", 
    "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AS", 
    "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC", 
    "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD"
    ]

d = Deck(my_card_list)

print(d)
print()
d.shuffle()

print(d)

player = Hand()
dealer = Hand()

print(player)

print(dealer)

player.deal(d.deal())
dealer.deal(d.deal())
player.deal(d.deal())
dealer.deal(d.deal())
print()

print(player)

print(dealer)