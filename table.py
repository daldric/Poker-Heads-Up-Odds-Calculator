import deck
from math import comb

suit_names = ["spades", "clubs", "hearts", "diamonds"]
SPADES_NUM = 0
CLUBS_NUM = 1
HEARTS_NUM = 2
DIAMONDS_NUM = 3

values = ['A', '2', '3', '4', '5', '6', '7', '8', '9',
          'T', 'J', 'Q', 'K']

class Player:
    current_stack = 0
    current_hand = []
    pocket_hand = []
    position = -1
    def __init__(self, table_spot, buy_in = 0):
        self.position = table_spot
        self.current_stack = buy_in

class Table:
    little_blind = 0
    big_blind = 1
    pot = 0
    players = []
    current_players = []
    table_cards = []
    used_cards = []
    remaining_cards = []
    cards = deck.Deck()

    num_suits = {}
    num_cards = {}

    def __init__(self, players):
        self.players = players

    def shift_blinds(self):
        if self.little_blind == len(self.players) - 1: 
            self.little_blind = 0
            self.big_blind += 1
        else: 
            self.little_blind += 1
            if self.big_blind == len(self.players) - 1: self.big_blind = 0
            else: self.big_blind += 1

    def deal(self):
        self.pot = 0
        self.used_cards = []
        self.remaining_cards = []
        self.table_cards = []
        self.cards.shuffle_deck()
        self.current_players = self.players
        for suit in deck.suit_names:
            self.num_suits[suit] = 0
        for val in values:
            self.num_cards[val] = 0

        for i in range(len(self.players)):
            card = self.cards.cards[i]
            self.players[(i + self.little_blind) % len(self.players)].pocket_hand = []
            self.players[(i + self.little_blind) % len(self.players)].pocket_hand.append(card)
            self.used_cards.append(card)
            self.num_suits[card.suit] += 1
            self.num_cards[card.val] += 1
        
        for i in range(len(self.players)):
            card = self.cards.cards[i + len(self.players)]
            self.players[(i + self.little_blind) % len(self.players)].pocket_hand.append(card)
            self.used_cards.append(card)
            self.num_suits[card.suit] += 1
            self.num_cards[card.val] += 1

        self.remaining_cards = self.cards.cards[len(self.used_cards):]

        
        for player in self.current_players:
            player.current_hand = player.pocket_hand
            print(f'Player {player.position}')
            deck.print_cards(player.pocket_hand)
            '''
            print(f'Perceived Flush Chance: {self.perceived_flush_chance(player)}')
            print(f'Real Flush Chance: {self.real_flush_chance(player)}')
            
            '''
            print()

    def flop(self):
        self.used_cards.append(self.remaining_cards[0])
        self.used_cards.append(self.remaining_cards[1])
        self.used_cards.append(self.remaining_cards[2])
        self.used_cards.append(self.remaining_cards[3])
        self.table_cards.append(self.remaining_cards[1])
        self.table_cards.append(self.remaining_cards[2])
        self.table_cards.append(self.remaining_cards[3])

        self.num_suits[self.remaining_cards[0].suit] += 1
        self.num_cards[self.remaining_cards[0].val] += 1
        self.num_suits[self.remaining_cards[1].suit] += 1
        self.num_cards[self.remaining_cards[1].val] += 1
        self.num_suits[self.remaining_cards[2].suit] += 1
        self.num_cards[self.remaining_cards[2].val] += 1
        self.num_suits[self.remaining_cards[3].suit] += 1
        self.num_cards[self.remaining_cards[3].val] += 1

        self.remaining_cards = self.remaining_cards[4:]

        print("Flop:")
        deck.print_cards(self.table_cards)
        print()

        for player in self.current_players:
            player.current_hand = deck.find_hand(self.table_cards, player.pocket_hand)
            
            print(f'Player {player.position}')
            #print(f'Perceived Flush Chance: {self.perceived_flush_chance(player)}')
            #print(f'Real Flush Chance: {self.real_flush_chance(player)}')
            print(f'Perceived Straight Chance: {self.perceived_straight_chance(player)}')
            print()
            


    def turn(self):
        self.used_cards.append(self.remaining_cards[0])
        self.used_cards.append(self.remaining_cards[1])
        self.table_cards.append(self.remaining_cards[1])

        self.num_suits[self.remaining_cards[0].suit] += 1
        self.num_cards[self.remaining_cards[0].val] += 1
        self.num_suits[self.remaining_cards[1].suit] += 1
        self.num_cards[self.remaining_cards[1].val] += 1

        self.remaining_cards = self.remaining_cards[2:]

        print("Turn:")
        deck.print_cards(self.table_cards)
        print()

        for player in self.current_players:
            player.current_hand = deck.find_hand(self.table_cards, player.pocket_hand)
            
            print(f'Player {player.position}')
            #print(f'Perceived Flush Chance: {self.perceived_flush_chance(player)}')
            #print(f'Real Flush Chance: {self.real_flush_chance(player)}')
            print(f'Perceived Straight Chance: {self.perceived_straight_chance(player)}')
            print()
            
        
        
        

    def river(self):
        self.used_cards.append(self.remaining_cards[0])
        self.used_cards.append(self.remaining_cards[1])
        self.table_cards.append(self.remaining_cards[1])

        self.num_suits[self.remaining_cards[0].suit] += 1
        self.num_cards[self.remaining_cards[0].val] += 1
        self.num_suits[self.remaining_cards[1].suit] += 1
        self.num_cards[self.remaining_cards[1].val] += 1

        self.remaining_cards = self.remaining_cards[2:]

        print("Board:")
        deck.print_cards(self.table_cards)
        print()

        for player in self.current_players:
            player.current_hand = deck.find_hand(self.table_cards, player.pocket_hand)
            print(f'Player {player.position}')
            deck.print_hand(player.current_hand)

    def find_winning_hand_overall(self):
        best_hand = 0
        competing_players = []
        for player in self.current_players:
            if player.current_hand[0] > best_hand:
                best_hand = player.current_hand[0]
                competing_players = [player]
            elif player.current_hand[0] == best_hand: competing_players.append(player)

        winning_indices = []
        winners = []
        if len(competing_players) > 1:
            for i in range(5):
                max_val = 0
                for j in range(len(competing_players)):
                    current_card = competing_players[j].current_hand[1][i].num_val
                    if current_card > max_val:
                        max_val = current_card
                        winning_indices = [j]
                    elif current_card == max_val:
                        winning_indices.append(j) 

                if len(winning_indices) == 1:
                    break   
        else: winners = competing_players
        
        for num in winning_indices:
            winners.append(competing_players[num])

        for player in winners:
            print("Winning hand:")
            print(f'Player {player.position}')
            deck.print_hand(player.current_hand)

        return winners
    
    

    def real_flush_chance(self, player):
        suit_vals = {suit_names[SPADES_NUM]: 0, suit_names[CLUBS_NUM]: 0, suit_names[HEARTS_NUM]: 0, suit_names[DIAMONDS_NUM]: 0}
        eligible_suits = []
        eligible_cards = player.pocket_hand + self.table_cards
        suit_probabilities = []
        for card in eligible_cards:
            suit_vals[card.suit] += 1

        remaining_cards = 5 - len(self.table_cards)
        
        for suit, num in suit_vals.items():
            if num >= 5: return [suit, 1]
            elif 5 - num <= remaining_cards and 5 - num <= 13 - self.num_suits[suit]: eligible_suits.append(suit)
        
        if len(eligible_suits) == 0: return [0]

        for suit in eligible_suits:
            num_outs = 13 - self.num_suits[suit]
            num_needed = 5 - suit_vals[suit]
            if remaining_cards == 1:
                probability = comb(num_outs, 1) / comb(len(self.remaining_cards), 1)
                suit_probabilities.append([suit, probability])
                continue
            elif remaining_cards == 2:
                probability = comb(num_outs, 2) / comb(len(self.remaining_cards), 2)
                if num_needed == 1:
                    probability += (num_outs * (len(self.remaining_cards) - num_outs)) / comb(len(self.remaining_cards), 2)
                suit_probabilities.append([suit, probability])
                continue
            else:
                probability = comb(num_outs, 5) / comb(len(self.remaining_cards), 5)
                if num_needed == 4:
                    probability += (comb(num_outs, 4) * (len(self.remaining_cards) - num_outs)) / comb(len(self.remaining_cards), 5)
                if num_needed == 3:
                    probability += (comb(num_outs, 3) * comb(len(self.remaining_cards) - num_outs, 2)) / comb(len(self.remaining_cards), 5)
                suit_probabilities.append([suit, probability])
                continue

        return suit_probabilities
    
    def perceived_flush_chance(self, player):
        suit_vals = {suit_names[SPADES_NUM]: 0, suit_names[CLUBS_NUM]: 0, suit_names[HEARTS_NUM]: 0, suit_names[DIAMONDS_NUM]: 0}
        eligible_suits = []
        eligible_cards = player.pocket_hand + self.table_cards
        suit_probabilities = []
        for card in eligible_cards:
            suit_vals[card.suit] += 1

        remaining_cards = 5 - len(self.table_cards)
        
        for suit, num in suit_vals.items():
            if num >= 5: return [suit, 1]
            elif 5 - num <= remaining_cards and 5 - num <= 13 - self.num_suits[suit]: eligible_suits.append(suit)
        
        if len(eligible_suits) == 0: return [0]

        possible_remaining = 52 - len(eligible_cards)

        for suit in eligible_suits:
            num_outs = 13 - suit_vals[suit]
            num_needed = 5 - suit_vals[suit]
            if remaining_cards == 1:
                probability = comb(num_outs, 1) / comb(possible_remaining, 1)
                suit_probabilities.append([suit, probability])
                continue
            elif remaining_cards == 2:
                probability = comb(num_outs, 2) / comb(possible_remaining, 2)
                if num_needed == 1:
                    probability += (num_outs * (possible_remaining - num_outs)) / comb(possible_remaining, 2)
                suit_probabilities.append([suit, probability])
                continue
            else:
                probability = comb(num_outs, 5) / comb(possible_remaining, 5)
                if num_needed == 4:
                    probability += (comb(num_outs, 4) * (possible_remaining - num_outs)) / comb(possible_remaining, 5)
                if num_needed == 3:
                    probability += (comb(num_outs, 3) * comb(possible_remaining - num_outs, 2)) / comb(possible_remaining, 5)
                suit_probabilities.append([suit, probability])
                continue

        return suit_probabilities
    
    def perceived_straight_chance(self, player):
        eligible_cards = player.pocket_hand + self.table_cards
        eligible_cards = deck.sort_cards(eligible_cards)
        remaining_card_values = {'A': 4, '2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 4, '9': 4,
                               'T': 4, 'J': 4, 'Q': 4, 'K': 4}
        out_card_values = []

        if deck.find_straight(eligible_cards)[0]: return 1

        for card in eligible_cards:
            remaining_card_values[card.val] -= 1

        #if eligible_cards[0].val == 'A':
            #eligible_cards.append(deck.Card('A', eligible_cards[0].suit, 1))

        remaining_cards = 5 - len(self.table_cards)
        possible_remaining = 52 - len(eligible_cards)

        if remaining_cards == 1:
            #print("here")
            for value in values:
                if remaining_card_values[value] < 1:
                    continue
                straight_cards = deck.find_straight(eligible_cards + [deck.Card(value, suit_names[CLUBS_NUM])])
                if straight_cards[0]:
                    out_card_values.append(value)

            num_outs = 0
            for value in out_card_values:
                print(f'{value}: {remaining_card_values[value]}')
                num_outs += remaining_card_values[value]

            probability = comb(num_outs, 1) / comb(possible_remaining, 1)
            return probability

        elif remaining_cards == 2:
            one_outs = []
            two_outs = []
            for value1 in values:
                if remaining_card_values[value1] < 1:
                    continue
                straight_cards = deck.find_straight(eligible_cards + [deck.Card(value1, suit_names[CLUBS_NUM])])
                if straight_cards[0]:
                    #print(value1)
                    one_outs.append(value1)
                    continue
                for value2 in values:
                    if remaining_card_values[value2] < 2:
                        continue
                    straight_cards = deck.find_straight(eligible_cards + 
                                                        [deck.Card(value1, suit_names[CLUBS_NUM]), deck.Card(value2, suit_names[CLUBS_NUM])])
                    if straight_cards[0]:
                        two_outs.append([value1, value2])
                
            print(f'one outs: {one_outs}')
            print(f'two outs: {two_outs}')

        return 0

    
