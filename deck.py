import random
import os
from PIL import Image

suit_names = ["spades", "hearts", "clubs", "diamonds"]
SPADES_NUM = 0
HEARTS_NUM = 1
CLUBS_NUM = 2
DIAMONDS_NUM = 3

suit_values = {suit_names[SPADES_NUM]: SPADES_NUM, suit_names[CLUBS_NUM]: CLUBS_NUM, 
               suit_names[HEARTS_NUM]: HEARTS_NUM, suit_names[DIAMONDS_NUM]: DIAMONDS_NUM}

HIGH_CARD = 1
PAIR = 2
TWO_PAIR = 3
THREE_OF_A_KIND = 4
STRAIGHT = 5
FLUSH = 6
FULL_HOUSE = 7
QUADS = 8
STRAIGHT_FLUSH = 9

hands = {HIGH_CARD: "High Card", PAIR: "Pair", TWO_PAIR: "Two Pair", THREE_OF_A_KIND: "Three of a Kind", STRAIGHT: "Straight",
         FLUSH: "Flush", FULL_HOUSE: "Full House", QUADS: "Four of a Kind", STRAIGHT_FLUSH: "Straight Flush"}

values = {'A': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
          'T': 10, 'J': 11, 'Q': 12, 'K': 13}

script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the images folder
images_folder = os.path.join(script_dir, "Images")

# Card Class
class Card:
    val = ''
    suit = ''
    num_val = -1
    index = 0

    image_path = ""
    image = []

    def __init__(self, card_val, card_suit, index, overridden_val = 0):
        self.val = card_val
        self.suit = card_suit
        if overridden_val != 0: self.num_val = overridden_val
        else: self.num_val = values[card_val]
        self.index = index

        if index == 0:
            image_file = f'gray_background.png'
        else:
            image_file = f'{self.val}_of_{self.suit}.png'

        self.image_path = os.path.join(images_folder, image_file)

        self.image = Image.open(self.image_path)
        self.image = self.image.resize((85, 119), Image.ANTIALIAS)

    # Object equality is now based on the values within the object instead of the object itself
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.val == other.val and self.suit == other.suit
        return False

    def __hash__(self):
        return hash((self.val, self.suit))
    
# Deck Class
class Deck:
    cards = []

    def __init__(self): 
        for suit in suit_names:
            for value in values:
                if value == 'A':
                    index = 1 + 13 * suit_values[suit]
                    self.cards.append(Card(value, suit, index))
                else:
                    index = values[value] + 13 * suit_values[suit]
                    self.cards.append(Card(value, suit, index))
                
    
    def shuffle_deck(self) :
        random.shuffle(self.cards)

def shuffle(cards):
    cards = random.shuffle(cards)
    return cards

def print_cards(given_cards):
    for card in given_cards:
        print(f'{card.val} of {card.suit}')

def print_hand(tuple):
    if tuple[0]:
        print(hands[tuple[0]])
        print_cards(tuple[1])
    else: print('not good')
    print()

def sort_cards(cards):
    return sorted(cards, key=lambda x: x.num_val, reverse=True)

def sort_cards_regular(cards):
    return sorted(cards, key=lambda x: x.num_val)

def sort_card_indices(cards, reversed=False):
    return sorted(cards, key=lambda x: x.index, reverse=reversed)

# Find if there is a flush (5 of the same suit) from the given cards
def find_flush(cards):
    suit_nums = {suit_names[SPADES_NUM]: 0, suit_names[CLUBS_NUM]: 0, 
               suit_names[HEARTS_NUM]: 0, suit_names[DIAMONDS_NUM]: 0}
    
    for card in cards:
        suit_nums[card.suit] += 1
        if suit_nums[card.suit] == 5:
            return [True, [card1 for card1 in cards if card1.suit == card.suit]]

    return [False]

# Find if there is a straight (5 consecutive cards by value) from the given cards
def find_straight(cards):
    if cards[0].val == 'A':
        newCard = Card('A', cards[0].suit, cards[0].index, 1)
        newCard.image = cards[0].image
        cards.append(newCard)

    consec_cards = [cards[0]]
    for i in range(len(cards) - 1):
        if cards[i].num_val == cards[i+1].num_val + 1: consec_cards.append(cards[i+1])
        elif cards[i].num_val == cards[i+1].num_val: continue
        else: consec_cards = [cards[i + 1]]

        if len(consec_cards) == 5:
            return [True, consec_cards]
        
    return [False]

# Find the matching card values
def find_same(cards):
    same_cards = [cards[0]]
    current_num = 1

    for i in range(len(cards) - 1):
        if cards[i].num_val == cards[i+1].num_val:
            current_num += 1
            if current_num > len(same_cards): 
                same_cards = cards[i-current_num+2:i+2]
        else: current_num = 1

    if len(same_cards) == 1:
        return [1, cards[:5]] # high card
    
    cards = [card for card in cards if card not in same_cards]

    if len(same_cards) == 4: 
        same_cards.append(cards[0])
        return [QUADS, same_cards]

    second_cards = []

    for i in range(len(cards) - 1):
        if cards[i].num_val == cards[i+1].num_val:
            second_cards = cards[i:i+2]
            break
    
    if len(same_cards) == 3:
        if len(second_cards) == 2: # full house
            same_cards += second_cards
            return [FULL_HOUSE, same_cards]
        
        same_cards.append(cards[0])
        same_cards.append(cards[1])
        return [THREE_OF_A_KIND, same_cards] # three of a kind
    
    elif len(same_cards) == 2:
        if len(second_cards) == 2: # two pair
            cards = [card for card in cards if card not in second_cards]
            same_cards += second_cards
            same_cards.append(cards[0])
            return [TWO_PAIR, same_cards]
        
        same_cards.append(cards[0])
        same_cards.append(cards[1])
        same_cards.append(cards[2])
        return [PAIR, same_cards]

# Find the highest hand value from the list of given cards
def find_hand(table_cards, personal_cards):
    total_cards = table_cards + personal_cards
    total_cards = sort_cards(total_cards)
    best_hand = []

    # straight flush
    flush_hand = find_flush(total_cards)
    if flush_hand[0]:
        best_hand = find_straight(flush_hand[1])
        if best_hand[0]: return [STRAIGHT_FLUSH, best_hand[1]]
    
    # quads and full house
    best_hand = find_same(total_cards)
    if best_hand[0] == QUADS or best_hand[0] == FULL_HOUSE: return best_hand

    # flush (already calculated)
    if flush_hand[0]: return [FLUSH, flush_hand[1][:5]]

    # straight
    straight_hand = find_straight(total_cards)
    if straight_hand[0]: return [STRAIGHT, straight_hand[1]]

    # three of a kind down to high card
    return best_hand