import deck
import table

suit_names = ["Spades", "Clubs", "Hearts", "Diamonds"]
SPADES_NUM = 0
CLUBS_NUM = 1
HEARTS_NUM = 2
DIAMONDS_NUM = 3

num_players = int(input('How many Players? '))
players = []
for i in range(num_players):
    players.append(table.Player(i))
        
poker_table = table.Table(players)

while(True):
    poker_table.deal()
    poker_table.flop()
    poker_table.turn()
    poker_table.river()
    poker_table.find_winning_hand()
    input("Press enter for next hand")

'''
# straight flush 5 high
deck.print_hand(deck.find_hand([deck.Card('3', suit_names[CLUBS_NUM]), deck.Card('A', suit_names[CLUBS_NUM]), deck.Card('7', suit_names[CLUBS_NUM]),
           deck.Card('2', suit_names[CLUBS_NUM]), deck.Card('4', suit_names[CLUBS_NUM])], [deck.Card('A', suit_names[HEARTS_NUM]),
           deck.Card('5', suit_names[CLUBS_NUM])]))

# quad 3's with Ace high
deck.print_hand(deck.find_hand([deck.Card('3', suit_names[CLUBS_NUM]), deck.Card('A', suit_names[CLUBS_NUM]), deck.Card('3', suit_names[HEARTS_NUM]),
           deck.Card('3', suit_names[DIAMONDS_NUM]), deck.Card('3', suit_names[SPADES_NUM])], [deck.Card('A', suit_names[HEARTS_NUM]),
           deck.Card('6', suit_names[CLUBS_NUM])]))

# full house 3s full of Aces
deck.print_hand(deck.find_hand([deck.Card('3', suit_names[CLUBS_NUM]), deck.Card('A', suit_names[CLUBS_NUM]), deck.Card('4', suit_names[HEARTS_NUM]),
           deck.Card('3', suit_names[DIAMONDS_NUM]), deck.Card('3', suit_names[SPADES_NUM])], [deck.Card('A', suit_names[HEARTS_NUM]),
           deck.Card('6', suit_names[CLUBS_NUM])]))

# flush: King high (straight also on the board)
deck.print_hand(deck.find_hand([deck.Card('3', suit_names[CLUBS_NUM]), deck.Card('K', suit_names[CLUBS_NUM]), deck.Card('7', suit_names[CLUBS_NUM]),
           deck.Card('2', suit_names[CLUBS_NUM]), deck.Card('4', suit_names[CLUBS_NUM])], [deck.Card('A', suit_names[HEARTS_NUM]),
           deck.Card('5', suit_names[CLUBS_NUM])]))

# straight: Jack high (three of a kind also on the board)
deck.print_hand(deck.find_hand([deck.Card('T', suit_names[CLUBS_NUM]), deck.Card('8', suit_names[HEARTS_NUM]), deck.Card('7', suit_names[CLUBS_NUM]),
           deck.Card('T', suit_names[CLUBS_NUM]), deck.Card('J', suit_names[CLUBS_NUM])], [deck.Card('T', suit_names[HEARTS_NUM]),
           deck.Card('9', suit_names[SPADES_NUM])]))

# three of a kind: threes
deck.print_hand(deck.find_hand([deck.Card('3', suit_names[CLUBS_NUM]), deck.Card('J', suit_names[CLUBS_NUM]), deck.Card('4', suit_names[HEARTS_NUM]),
           deck.Card('3', suit_names[DIAMONDS_NUM]), deck.Card('3', suit_names[SPADES_NUM])], [deck.Card('A', suit_names[HEARTS_NUM]),
           deck.Card('6', suit_names[CLUBS_NUM])]))

# two pair: Aces and 4s
deck.print_hand(deck.find_hand([deck.Card('3', suit_names[CLUBS_NUM]), deck.Card('A', suit_names[CLUBS_NUM]), deck.Card('4', suit_names[HEARTS_NUM]),
           deck.Card('3', suit_names[DIAMONDS_NUM]), deck.Card('4', suit_names[SPADES_NUM])], [deck.Card('A', suit_names[HEARTS_NUM]),
           deck.Card('6', suit_names[CLUBS_NUM])]))

# pair: 3s
deck.print_hand(deck.find_hand([deck.Card('3', suit_names[CLUBS_NUM]), deck.Card('A', suit_names[CLUBS_NUM]), deck.Card('4', suit_names[HEARTS_NUM]),
           deck.Card('3', suit_names[DIAMONDS_NUM]), deck.Card('8', suit_names[SPADES_NUM])], [deck.Card('K', suit_names[HEARTS_NUM]),
           deck.Card('6', suit_names[CLUBS_NUM])]))

# Ace high
deck.print_hand(deck.find_hand([deck.Card('J', suit_names[CLUBS_NUM]), deck.Card('A', suit_names[CLUBS_NUM]), deck.Card('4', suit_names[HEARTS_NUM]),
           deck.Card('3', suit_names[DIAMONDS_NUM]), deck.Card('8', suit_names[SPADES_NUM])], [deck.Card('K', suit_names[HEARTS_NUM]),
           deck.Card('6', suit_names[CLUBS_NUM])]))
'''
