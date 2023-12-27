import deck
import tkinter as tk
from PIL import ImageTk
import time
import random

suit_names = ["spades", "clubs", "hearts", "diamonds"]
SPADES_NUM = 0
CLUBS_NUM = 1
HEARTS_NUM = 2
DIAMONDS_NUM = 3

values = ['A', '2', '3', '4', '5', '6', '7', '8', '9',
          'T', 'J', 'Q', 'K']

suit_conv = {'S': "spades", 'C': "clubs", 'H': "hearts", 'D': "diamonds"}

# Player Class
class Player:
    current_hand = []
    pocket_cards = []
    name = ""

    def __init__(self, pocket_cards, name):
        self.pocket_cards = pocket_cards
        self.name = name

# Simulator Class (Singleton)
class Simulator:
    cards = deck.Deck().cards
    remaining_cards = []
    table_cards = []

    def __init__(self):
        self.remaining_cards = self.cards

    # Find the winning hand from an array of players
    def find_winning_hand(self, players):
        best_hand = 0
        competing_players = []
        for player in players:
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


        return winners
    
    # Find the winning hand from among two players
    def find_winning_hand_heads_up(self, player1, player2):
        if player1.current_hand[0] > player2.current_hand[0]:
            return [player1]
        elif player1.current_hand[0] < player2.current_hand[0]:
            return [player2]

        for i in range(5):
            if player1.current_hand[1][i].num_val > player2.current_hand[1][i].num_val:
                return [player1]
            elif player1.current_hand[1][i].num_val < player2.current_hand[1][i].num_val:
                return [player2]
        
        return [player1, player2]
        
    # Find the cards that the player who is currently losing needs in order to win or chop (tie)
    def find_outs(self, player1, player2):
        start_time = time.time()
        remaining_cards = 5 - len(self.table_cards)
        current_cards = player1.pocket_cards + player2.pocket_cards + self.table_cards
        self.remaining_cards = [card for card in self.cards if card not in current_cards]

        # Find who is currently winning
        player1.current_hand = deck.find_hand(self.table_cards, player1.pocket_cards)
        player2.current_hand = deck.find_hand(self.table_cards, player2.pocket_cards)
        current_winner = self.find_winning_hand_heads_up(player1, player2)

        # GUI updates
        grid_frame.pack_forget()

        button_frame.pack_forget()

        current_winner_frame.pack()
        
        player1_hand.config(text=deck.hands[player1.current_hand[0]])
        player1_card1.config(image=player1.current_hand[1][0].image)
        player1_card1.image = player1.current_hand[1][0].image
        player1_card2.config(image=player1.current_hand[1][1].image)
        player1_card2.image = player1.current_hand[1][1].image
        player1_card3.config(image=player1.current_hand[1][2].image)
        player1_card3.image = player1.current_hand[1][2].image
        player1_card4.config(image=player1.current_hand[1][3].image)
        player1_card4.image = player1.current_hand[1][3].image
        player1_card5.config(image=player1.current_hand[1][4].image)
        player1_card5.image = player1.current_hand[1][4].image

        player2_hand.config(text=deck.hands[player2.current_hand[0]])
        player2_card1.config(image=player2.current_hand[1][0].image)
        player2_card1.image = player2.current_hand[1][0].image
        player2_card2.config(image=player2.current_hand[1][1].image)
        player2_card2.image = player2.current_hand[1][1].image
        player2_card3.config(image=player2.current_hand[1][2].image)
        player2_card3.image = player2.current_hand[1][2].image
        player2_card4.config(image=player2.current_hand[1][3].image)
        player2_card4.image = player2.current_hand[1][3].image
        player2_card5.config(image=player2.current_hand[1][4].image)
        player2_card5.image = player2.current_hand[1][4].image

        # There are no more cards to come
        if remaining_cards == 0: 
            if len(current_winner) == 2:
                print("Chop")
                current_winner_label.config(text="Chop")
                
            elif current_winner[0] == player1:
                print(f'{player1.name} Wins')
                current_winner_label.config(text=f'{player1.name} Wins')
                
            else: 
                print(f'{player2.name} Wins')
                current_winner_label.config(text=f'{player2.name} Wins')
            player1_win_chance.config(text="")
            player2_win_chance.config(text="")
            result_frame.pack()
            return []

        chopping_cards = []
        p1_winning_cards = []
        p2_winning_cards = []

        chopping_2_outs = []
        p1_2_outs = []
        p2_2_outs = []

        maybe_p1 = player1
        maybe_p2 = player2

        p1_winning_combos = 0
        p2_winning_combos = 0
        chopping_combos = 0

        count = 0

        # Look through every remaining card and see how each will affect each player's hand
        for card in self.remaining_cards:
            if remaining_cards == 1: count += 1
            maybe_p1.current_hand = deck.find_hand(self.table_cards + [card], maybe_p1.pocket_cards)
            maybe_p2.current_hand = deck.find_hand(self.table_cards + [card], maybe_p2.pocket_cards)
            maybe_winner = self.find_winning_hand_heads_up(maybe_p1, maybe_p2)

            if len(maybe_winner) == 2:
                if len(current_winner) != 2:
                    if remaining_cards == 1: chopping_combos += 1
                    chopping_cards.append(card)
            elif maybe_winner[0] == maybe_p1 and (len(current_winner) == 2 or current_winner[0] == player2):
                if remaining_cards == 1: p1_winning_combos += 1
                p1_winning_cards.append(card)
            elif maybe_winner[0] == maybe_p2 and (len(current_winner) == 2 or current_winner[0] == player1): 
                if remaining_cards == 1: p2_winning_combos += 1
                p2_winning_cards.append(card)

        # If there are two cards yet to come, run every possible remaining combination
            # If there is a combination of two cards needed, add it to '2-outs'
        if remaining_cards == 2:
            outs = []
            if len(current_winner) != 2:
                if current_winner[0] == player1:
                    outs = p2_winning_cards + chopping_cards
                else:
                    outs = p1_winning_cards + chopping_cards
            else: outs = p1_winning_cards + p2_winning_cards
            
            self.remaining_cards = deck.sort_card_indices(self.remaining_cards, reversed=True)
            for card1 in self.remaining_cards:
                for card2 in self.remaining_cards:
                    # Save computations by using sorting
                    if card2.index < card1.index:
                        count += 1
                        maybe_p1.current_hand = deck.find_hand(self.table_cards + [card1, card2], maybe_p1.pocket_cards)
                        maybe_p2.current_hand = deck.find_hand(self.table_cards + [card1, card2], maybe_p2.pocket_cards)
                        maybe_winner = self.find_winning_hand_heads_up(maybe_p1, maybe_p2)
                        
                        if len(maybe_winner) == 2:
                            if len(current_winner) != 2:
                                chopping_combos += 1
                                if card1 not in outs and card2 not in outs:
                                    chopping_2_outs.append(card1)
                                    chopping_2_outs.append(card2)
                                    chopping_2_outs = list(set(chopping_2_outs))
                        elif maybe_winner[0] == maybe_p1 and (len(current_winner) == 2 or current_winner[0] == player2):
                            p1_winning_combos += 1
                            if card1 not in outs and card2 not in outs:
                                    p1_2_outs.append(card1)
                                    p1_2_outs.append(card2)
                                    p1_2_outs = list(set(p1_2_outs))
                        elif maybe_winner[0] == maybe_p2 and (len(current_winner) == 2 or current_winner[0] == player1): 
                            p2_winning_combos += 1
                            if card1 not in outs and card2 not in outs:
                                    p2_2_outs.append(card1)
                                    p2_2_outs.append(card2)
                                    p2_2_outs = list(set(p2_2_outs))

        p1_winning_cards = deck.sort_cards_regular(p1_winning_cards)
        p2_winning_cards = deck.sort_cards_regular(p2_winning_cards)
        chopping_cards = deck.sort_cards_regular(chopping_cards)

        winning_player = ""
        function_outs_1 = []
        function_outs_2 = []

        # GUI updates
        if len(current_winner) == 2: # There is a tie
            p1_win_odds = p1_winning_combos / count
            p2_win_odds = p2_winning_combos / count
            chopping_odds = 1 - p1_win_odds - p2_win_odds
            
            current_winner_label.config(text="Currently Chopping")

            if len(p1_winning_cards) > 0:
                outs1_label = tk.Label(outs_board_1, text="Player 1 Outs: ")
                outs1_label.pack(side=tk.LEFT)
                for card in p1_winning_cards:
                    outs_card = tk.Label(outs_board_1, image=card.image)
                    outs_card.pack(side=tk.LEFT)
                
            if len(p2_winning_cards) > 0:
                outs2_label = tk.Label(outs_board_2, text="Player 2 Outs: ")
                outs2_label.pack(side=tk.LEFT)
                for card in p2_winning_cards:
                    outs_card = tk.Label(outs_board_2, image=card.image)
                    outs_card.pack(side=tk.LEFT)

            if remaining_cards == 2:
                winning_player = "chop"
                if len(p1_2_outs) > 0:
                    function_outs_1 = p1_2_outs
                if len(p2_2_outs) > 0:
                    function_outs_2 = p2_2_outs
        elif current_winner[0] == player1: # Player 1 is currently winning
            p2_win_odds = p2_winning_combos / count
            chopping_odds = chopping_combos / count
            p1_win_odds = 1 - chopping_odds - p2_win_odds
            
            current_winner_label.config(text=f'{player1.name} is Currently Winning')
            
            if len(p2_winning_cards) > 0:
                outs1_label = tk.Label(outs_board_1, text="Player 2 Outs: ")
                outs1_label.pack(side=tk.LEFT)
                for card in p2_winning_cards:
                    outs_card = tk.Label(outs_board_1, image=card.image)
                    outs_card.pack(side=tk.LEFT)
            
            if len(chopping_cards) > 0:
                outs2_label = tk.Label(outs_board_2, text="Chopping Outs:")
                outs2_label.pack(side=tk.LEFT)
                for card in chopping_cards:
                    outs_card = tk.Label(outs_board_2, image=card.image)
                    outs_card.pack(side=tk.LEFT)

            if remaining_cards == 2:
                winning_player = "p1"
                if len(p2_2_outs) > 0:
                    function_outs_1 = p2_2_outs
                if len(chopping_2_outs) > 0:
                    function_outs_2 = chopping_2_outs
        else: # Player 2 is currently winning
            p1_win_odds = p1_winning_combos / count
            chopping_odds = chopping_combos / count
            p2_win_odds = 1 - p1_win_odds - chopping_odds
            
            current_winner_label.config(text=f'{player2.name} is Currently Winning')
            
            if len(p1_winning_cards) > 0:
                outs1_label = tk.Label(outs_board_1, text="Player 1 Outs: ")
                outs1_label.pack(side=tk.LEFT)
                for card in p1_winning_cards:
                    outs_card = tk.Label(outs_board_1, image=card.image)
                    outs_card.pack(side=tk.LEFT)
            
            if len(chopping_cards) > 0:
                outs2_label = tk.Label(outs_board_2, text="Chopping Outs:")
                outs2_label.pack(side=tk.LEFT)
                for card in chopping_cards:
                    outs_card = tk.Label(outs_board_2, image=card.image)
                    outs_card.pack(side=tk.LEFT)

            if remaining_cards == 2:
                winning_player = "p2"
                if len(p1_2_outs) > 0:
                    function_outs_1 = p1_2_outs
                if len(chopping_2_outs) > 0:
                    function_outs_2 = chopping_2_outs
        
        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")

        player1_win_chance.config(text="Win Chance: %.2f" % p1_win_odds)

        player2_win_chance.config(text="Win Chance: %.2f" % p2_win_odds)
        
        result_frame.pack()

        chopping_chance.config(text="Chopping Chance: %.2f" % chopping_odds)
        
        # Create popup window for 2-out combinations
        if remaining_cards == 2 and (len(function_outs_1) > 0 or len(function_outs_2) > 0):
            button_2_outs = tk.Button(chopping_frame, text="View 2-Out Cards", command=lambda: popup_2_outs(winning_player, function_outs_1, function_outs_2))
            button_2_outs.pack(side=tk.RIGHT, padx=15)

        chopping_frame.pack()

        outer_outs_1.pack(padx=10, fill='x', expand=False)
        outer_outs_2.pack(padx=10, fill='x', expand=False)

    # Pre-flop (no cards on the table yet) simulation
    def heads_up(self, p1, p2):
        start_time = time.time()
        current_cards = p1.pocket_cards + p2.pocket_cards
        self.remaining_cards = [card for card in self.cards if card not in current_cards]

        p1_winner_count = 0
        p2_winner_count = 0
        chop_count = 0

        total_count = 500

        # Simulate 500 5-card runouts and determine the winner of each to see which player is favored
        for i in range(total_count):
            random.shuffle(self.remaining_cards)
            p1.current_hand = deck.find_hand(self.remaining_cards[:5], p1.pocket_cards)
            p2.current_hand = deck.find_hand(self.remaining_cards[:5], p2.pocket_cards)
            current_winner = self.find_winning_hand_heads_up(p1, p2)

            if len(current_winner) == 2:
                chop_count += 1
            elif current_winner[0] == p1:
                p1_winner_count += 1
            else:
                p2_winner_count += 1

        p1_winner_odds = p1_winner_count / total_count
        p2_winner_odds = p2_winner_count / total_count
        chop_odds = chop_count / total_count

        player1_win_label.config(text="Win Chance: %.2f" % p1_winner_odds)

        player2_win_label.config(text="Win Chance: %.2f" % p2_winner_odds)

        chop_chance_label.config(text="Chop Chance: %.2f" % chop_odds)

        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")

# Configure the GUI
def setup_screen(cards):

    back_to_cards_button=tk.Button(current_winner_frame, text="Re-Select Cards", command=switch_to_cards_view)
    back_to_cards_button.pack(pady=10)

    current_winner_label.pack()

    player1_label = tk.Label(player1, text="Player 1")
    player1_label.pack(side=tk.TOP)

    player2_label = tk.Label(player2, text="Player 2")
    player2_label.pack(side=tk.TOP)

    table_label = tk.Label(table, text="Board Cards")
    table_label.pack(side=tk.TOP)

    player1_win_label.pack(side=tk.BOTTOM)

    player2_win_label.pack(side=tk.BOTTOM)

    chop_chance_label.pack(side=tk.BOTTOM)

    calculate = tk.Button(button_frame, text="Calculate", command=calculation)
    calculate.pack(side=tk.LEFT, padx=20, pady=5)

    all_clear = tk.Button(button_frame, text="Clear", command=clear_cards_all)
    all_clear.pack(side=tk.RIGHT, padx=20, pady=5)

    p1_1.pack(side=tk.LEFT, fill='both', expand=True)
    p1_1.bind('<Button-1>', on_top_click)
    
    p1_2.pack(side=tk.LEFT, expand=True)
    p1_2.bind('<Button-1>', on_top_click)
    
    p2_1.pack(side=tk.LEFT)
    p2_1.bind('<Button-1>', on_top_click)

    p2_2.pack(side=tk.LEFT)
    p2_2.bind('<Button-1>', on_top_click)

    table1.pack(side=tk.LEFT)
    table1.bind('<Button-1>', on_top_click)
    
    table2.pack(side=tk.LEFT)
    table2.bind('<Button-1>', on_top_click)
    
    table3.pack(side=tk.LEFT)
    table3.bind('<Button-1>', on_top_click)
    
    table4.pack(side=tk.LEFT)
    table4.bind('<Button-1>', on_top_click)
    
    table5.pack(side=tk.LEFT)
    table5.bind('<Button-1>', on_top_click)

    # Sort the cards
    sorted_cards = deck.sort_card_indices(cards)

    # Display the sorted cards
    for card in sorted_cards:
        card.image = ImageTk.PhotoImage(card.image)
        label = tk.Label(grid_frame, image=card.image)
        label.image = card.image
        label.card = card
        label.grid(row=(card.index - 1) // 13, column=(card.index - 1) % 13)  # 13 cards per row
        label.bind('<Button-1>', lambda event, c = card: on_selection_click(event, c))

# Create the popup window for the 2-out card combinations when needed
def popup_2_outs(player, outs1, outs2):
    popup = tk.Toplevel()

    popup.title("2-Outs")
    popup.geometry("800x400+300+200")

    outer_outs1_frame = tk.Frame(popup)
    popup_canvas_1 = tk.Canvas(outer_outs1_frame, height=125)
    scrollbar_popup_1 = tk.Scrollbar(outer_outs1_frame, orient="horizontal", command=popup_canvas_1.xview)
    scrollbar_popup_1.pack(side=tk.BOTTOM, fill="x")
    popup_canvas_1.pack(fill="x")
    popup_canvas_1.configure(xscrollcommand=scrollbar_popup_1.set)
    outs1_frame = tk.Frame(popup_canvas_1)
    popup_canvas_1.create_window((0, 0), window=outs1_frame, anchor="nw")

    def update_popupregion_c1(event):
        popup_canvas_1.update_idletasks()
        popup_canvas_1.config(scrollregion=popup_canvas_1.bbox("all"))

        # Show scrollbar only if needed
        if popup_canvas_1.bbox("all")[2] > popup_canvas_1.winfo_width():
            scrollbar_popup_1.pack(side="bottom", fill="x")
        else:
            scrollbar_popup_1.forget()

    outs1_frame.bind("<Configure>", update_popupregion_c1)


    outer_outs2_frame = tk.Frame(popup)
    popup_canvas_2 = tk.Canvas(outer_outs2_frame, height=125)
    scrollbar_popup_2 = tk.Scrollbar(outer_outs2_frame, orient="horizontal", command=popup_canvas_2.xview)
    scrollbar_popup_2.pack(side=tk.BOTTOM, fill="x")
    popup_canvas_2.pack(fill="x")
    popup_canvas_2.configure(xscrollcommand=scrollbar_popup_2.set)
    outs2_frame = tk.Frame(popup_canvas_2)
    popup_canvas_2.create_window((0, 0), window=outs2_frame, anchor="nw")

    def update_popupregion_c2(event):
        popup_canvas_2.update_idletasks()
        popup_canvas_2.config(scrollregion=popup_canvas_2.bbox("all"))

        # Show scrollbar only if needed
        if popup_canvas_2.bbox("all")[2] > popup_canvas_2.winfo_width():
            scrollbar_popup_2.pack(side="bottom", fill="x")
        else:
            scrollbar_popup_2.forget()

    outs2_frame.bind("<Configure>", update_popupregion_c2)

    outs1_label = []
    outs2_label = []

    if player == "chop":
        outs1_label = tk.Label(outs1_frame, text="Player 1 2-Outs: ")
        outs2_label = tk.Label(outs2_frame, text="Player 2 2-Outs: ")
    elif player == "p1":
        outs1_label = tk.Label(outs1_frame, text="Player 2 2-Outs: ")
        outs2_label = tk.Label(outs2_frame, text="Chopping 2-Outs: ")
    else:
        outs1_label = tk.Label(outs1_frame, text="Player 1 2-Outs: ")
        outs2_label = tk.Label(outs2_frame, text="Chopping 2-Outs: ")
      
    if len(outs1) > 0:
        outs1 = deck.sort_cards_regular(outs1)
        outs1_label.pack(side=tk.LEFT)
        for card in outs1:
            outs_card = tk.Label(outs1_frame, image=card.image)
            outs_card.pack(side=tk.LEFT)
    if len(outs2) > 0:
        outs2 = deck.sort_cards_regular(outs2)
        outs2_label.pack(side=tk.LEFT)
        for card in outs2:
            outs_card = tk.Label(outs2_frame, image=card.image)
            outs_card.pack(side=tk.LEFT)

    outer_outs1_frame.pack(padx=10, pady=10, fill="x")
    outer_outs2_frame.pack(padx=10, fill="x")

    return

# Transition the GUI from the result back to the card selection
def switch_to_cards_view():
    current_winner_frame.pack_forget()
    result_frame.pack_forget()
    for widget in chopping_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()
    chopping_frame.pack_forget()

    for widget in outs_board_1.winfo_children():
        widget.destroy()

    for widget in outs_board_2.winfo_children():
        widget.destroy()    

    outer_outs_1.pack_forget()
    outer_outs_2.pack_forget()
    
    button_frame.pack(side=tk.TOP)
    grid_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=0)

# When a card along the top of the GUI is clicked, return it to its proper spot from among the 
    # grid of cards and turn it back to a gray image
def on_top_click(event):
    if event.widget.image == default_img: return

    modifying_widget = grid_frame.grid_slaves(row=(event.widget.card_index - 1) // 13, column=(event.widget.card_index - 1) % 13)[0]

    modifying_widget.config(image = event.widget.image)
    modifying_widget.image = event.widget.image

    if event.widget == p1_1 or event.widget == p1_2: 
        p1.pocket_cards = [card for card in p1.pocket_cards if card != modifying_widget.card]
    elif event.widget == p2_1 or event.widget == p2_2: 
        p2.pocket_cards = [card for card in p2.pocket_cards if card != modifying_widget.card]
    else:
        s.table_cards = [card for card in s.table_cards if card != modifying_widget.card]

    event.widget.config(image=default_img)
    event.widget.image = default_img
    event.widget.card_index = 0

# Place the card selected from the grid of cards into the first available spot on the top
    # If the card is already in a spot on the top, return it to its proper place on the grid
def on_selection_click(event, card):
    available = True
    
    if p1_1.image == card.image:
        p1_1.config(image=default_img)
        p1_1.image = default_img
        p1_1.card_index = 0
        p1.pocket_cards = [pcard for pcard in p1.pocket_cards if pcard != card]
    elif p1_2.image == card.image:
        p1_2.config(image=default_img)
        p1_2.image = default_img
        p1_2.card_index = 0
        p1.pocket_cards = [pcard for pcard in p1.pocket_cards if pcard != card]
    elif p2_1.image == card.image:
        p2_1.config(image=default_img)
        p2_1.image = default_img
        p2_1.card_index = 0
        p2.pocket_cards = [pcard for pcard in p2.pocket_cards if pcard != card]
    elif p2_2.image == card.image:
        p2_2.config(image=default_img)
        p2_2.image = default_img
        p2_2.card_index = 0
        p2.pocket_cards = [pcard for pcard in p2.pocket_cards if pcard != card]
    elif table1.image == card.image:
        table1.config(image=default_img)
        table1.image = default_img
        table1.card_index = 0
        s.table_cards = [tcard for tcard in s.table_cards if tcard != card]
    elif table2.image == card.image:
        table2.config(image=default_img)
        table2.image = default_img
        table2.card_index = 0
        s.table_cards = [tcard for tcard in s.table_cards if tcard != card]
    elif table3.image == card.image:
        table3.config(image=default_img)
        table3.image = default_img
        table3.card_index = 0
        s.table_cards = [tcard for tcard in s.table_cards if tcard != card]
    elif table4.image == card.image:
        table4.config(image=default_img)
        table4.image = default_img
        table4.card_index = 0
        s.table_cards = [tcard for tcard in s.table_cards if tcard != card]
    elif table5.image == card.image:
        table5.config(image=default_img)
        table5.image = default_img
        table5.card_index = 0
        s.table_cards = [tcard for tcard in s.table_cards if tcard != card]

    elif p1_1.image == default_img:
        p1_1.config(image=card.image)
        p1_1.image = card.image
        p1_1.card_index = card.index
        p1.pocket_cards.append(card)
    elif p1_2.image == default_img:
        p1_2.config(image=card.image)
        p1_2.image = card.image
        p1_2.card_index = card.index
        p1.pocket_cards.append(card)
    elif p2_1.image == default_img:
        p2_1.config(image=card.image)
        p2_1.image = card.image
        p2_1.card_index = card.index
        p2.pocket_cards.append(card)
    elif p2_2.image == default_img:
        p2_2.config(image=card.image)
        p2_2.image = card.image
        p2_2.card_index = card.index
        p2.pocket_cards.append(card)
    elif table1.image == default_img:
        table1.config(image=card.image)
        table1.image = card.image
        table1.card_index = card.index
        s.table_cards.append(card)
    elif table2.image == default_img:
        table2.config(image=card.image)
        table2.image = card.image
        table2.card_index = card.index
        s.table_cards.append(card)
    elif table3.image == default_img:
        table3.config(image=card.image)
        table3.image = card.image
        table3.card_index = card.index
        s.table_cards.append(card)
    elif table4.image == default_img:
        table4.config(image=card.image)
        table4.image = card.image
        table4.card_index = card.index
        s.table_cards.append(card)
    elif table5.image == default_img:
        table5.config(image=card.image)
        table5.image = card.image
        table5.card_index = card.index
        s.table_cards.append(card)
    else:
        available = False

    if event.widget.image == default_img:
        event.widget.config(image=card.image)
        event.widget.image = card.image
    elif available:
        event.widget.config(image=default_img)
        event.widget.image = default_img

# Determine which function needs to be called based on the current cards selected
    # Also error checking to ensure the proper cards have been selected
def calculation():
    player1_win_label.config(text="")
    player2_win_label.config(text="")
    chop_chance_label.config(text="")

    if len(p1.pocket_cards) == 2 and len(p2.pocket_cards) == 2:
        if len(s.table_cards) == 0: s.heads_up(p1, p2)
        elif len(s.table_cards) >= 3: s.find_outs(p1, p2)

# Clear all of the cards from the top of the screen and return them to the grid
def clear_cards_all():
    player1_win_label.config(text="")
    player2_win_label.config(text="")
    chop_chance_label.config(text="")
    clear_cards_p1()
    clear_cards_p2()
    clear_cards_table()

# Clear just the cards from Player 1
def clear_cards_p1():
    if p1_1.image != default_img: 
        modifying_widget = grid_frame.grid_slaves(row=(p1_1.card_index - 1) // 13, column=(p1_1.card_index - 1) % 13)[0]

        modifying_widget.config(image = p1_1.image)
        modifying_widget.image = p1_1.image

        p1_1.config(image=default_img)
        p1_1.image = default_img
        p1_1.card_index = 0

    if p1_2.image != default_img: 
        modifying_widget = grid_frame.grid_slaves(row=(p1_2.card_index - 1) // 13, column=(p1_2.card_index - 1) % 13)[0]

        modifying_widget.config(image = p1_2.image)
        modifying_widget.image = p1_2.image

        p1_2.config(image=default_img)
        p1_2.image = default_img
        p1_2.card_index = 0

    p1.pocket_cards = []

# Clear just the cards from Player 2
def clear_cards_p2():
    if p2_1.image != default_img: 
        modifying_widget = grid_frame.grid_slaves(row=(p2_1.card_index - 1) // 13, column=(p2_1.card_index - 1) % 13)[0]

        modifying_widget.config(image = p2_1.image)
        modifying_widget.image = p2_1.image

        p2_1.config(image=default_img)
        p2_1.image = default_img
        p2_1.card_index = 0

    if p2_2.image != default_img: 
        modifying_widget = grid_frame.grid_slaves(row=(p2_2.card_index - 1) // 13, column=(p2_2.card_index - 1) % 13)[0]

        modifying_widget.config(image = p2_2.image)
        modifying_widget.image = p2_2.image

        p2_2.config(image=default_img)
        p2_2.image = default_img
        p2_2.card_index = 0

    p2.pocket_cards = []

# Clear just the cards from the board
def clear_cards_table():
    if table1.image != default_img: 
        modifying_widget = grid_frame.grid_slaves(row=(table1.card_index - 1) // 13, column=(table1.card_index - 1) % 13)[0]

        modifying_widget.config(image = table1.image)
        modifying_widget.image = table1.image

        table1.config(image=default_img)
        table1.image = default_img
        table1.card_index = 0

    if table2.image != default_img: 
        modifying_widget = grid_frame.grid_slaves(row=(table2.card_index - 1) // 13, column=(table2.card_index - 1) % 13)[0]

        modifying_widget.config(image = table2.image)
        modifying_widget.image = table2.image

        table2.config(image=default_img)
        table2.image = default_img
        table2.card_index = 0
    
    if table3.image != default_img: 
        modifying_widget = grid_frame.grid_slaves(row=(table3.card_index - 1) // 13, column=(table3.card_index - 1) % 13)[0]

        modifying_widget.config(image = table3.image)
        modifying_widget.image = table3.image

        table3.config(image=default_img)
        table3.image = default_img
        table3.card_index = 0

    if table4.image != default_img: 
        modifying_widget = grid_frame.grid_slaves(row=(table4.card_index - 1) // 13, column=(table4.card_index - 1) % 13)[0]

        modifying_widget.config(image = table4.image)
        modifying_widget.image = table4.image

        table4.config(image=default_img)
        table4.image = default_img
        table4.card_index = 0

    if table5.image != default_img: 
        modifying_widget = grid_frame.grid_slaves(row=(table5.card_index - 1) // 13, column=(table5.card_index - 1) % 13)[0]

        modifying_widget.config(image = table5.image)
        modifying_widget.image = table5.image

        table5.config(image=default_img)
        table5.image = default_img
        table5.card_index = 0

    s.table_cards = []

# GUI configuration
root = tk.Tk()
root.title("Heads-Up Calculator")
root.geometry("1170x750+100+0")

s = Simulator()

p1 = Player([], "Player 1")
p2 = Player([], "Player 2")

grid_frame = tk.Frame(root)
grid_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=0)

pack_frame = tk.Frame(root)
pack_frame.pack(side=tk.TOP, fill=tk.X)

button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP)

default_card = deck.Card('A', 'clubs', 0)

default_img = default_card.image

default_img = ImageTk.PhotoImage(default_img)

player1 = tk.Frame(pack_frame)
player1.pack(side=tk.LEFT, padx=10, pady=0)

player2 = tk.Frame(pack_frame)
player2.pack(side=tk.RIGHT, padx=10, pady=0)

table = tk.Frame(pack_frame, pady=0)
table.pack()

player1_win_label = tk.Label(player1)

player2_win_label = tk.Label(player2)

chop_chance_label = tk.Label(table)

p1_1 = tk.Label(player1, image=default_img)
p1_1.image = default_img
p1_1.card_index = 0
p1_2 = tk.Label(player1, image=default_img)
p1_2.image = default_img
p1_2.card_index = 0
p2_1 = tk.Label(player2, image=default_img)
p2_1.image = default_img
p2_1.card_index = 0
p2_2 = tk.Label(player2, image=default_img)
p2_2.image = default_img
p2_2.card_index = 0

table1 = tk.Label(table, image=default_img)
table1.image = default_img
table1.card_index = 0
table2 = tk.Label(table, image=default_img)
table2.image = default_img
table2.card_index = 0
table3 = tk.Label(table, image=default_img)
table3.image = default_img
table3.card_index = 0
table4 = tk.Label(table, image=default_img)
table4.image = default_img
table4.card_index = 0
table5 = tk.Label(table, image=default_img)
table5.image = default_img
table5.card_index = 0

current_winner_frame=tk.Frame(root)

current_winner_label=tk.Label(current_winner_frame, text="Current Winner: ")

result_frame=tk.Frame(root)

player1_frame = tk.Frame(result_frame)
player1_frame.pack(side=tk.LEFT, padx=50, pady=0)

player1_label = tk.Label(player1_frame, text="Player 1 Current Hand")
player1_label.pack(side=tk.TOP)

player1_hand = tk.Label(player1_frame, text="Player 1 Hand")
player1_hand.pack()

player1_card_frame = tk.Frame(player1_frame)
player1_card_frame.pack(side=tk.TOP)

player1_card1 = tk.Label(player1_card_frame, image=default_img)
player1_card1.image = default_img
player1_card1.card_index = 0
player1_card1.pack(side=tk.LEFT)

player1_card2 = tk.Label(player1_card_frame, image=default_img)
player1_card2.image = default_img
player1_card2.card_index = 0
player1_card2.pack(side=tk.LEFT)

player1_card3 = tk.Label(player1_card_frame, image=default_img)
player1_card3.image = default_img
player1_card3.card_index = 0
player1_card3.pack(side=tk.LEFT)

player1_card4 = tk.Label(player1_card_frame, image=default_img)
player1_card4.image = default_img
player1_card4.card_index = 0
player1_card4.pack(side=tk.LEFT)

player1_card5 = tk.Label(player1_card_frame, image=default_img)
player1_card5.image = default_img
player1_card5.card_index = 0
player1_card5.pack(side=tk.LEFT)

player1_win_chance = tk.Label(player1_frame, text='Win Chance: 0.0')
player1_win_chance.pack(side=tk.BOTTOM)


player2_frame = tk.Frame(result_frame)
player2_frame.pack(side=tk.RIGHT, padx=50, pady=0)

player2_label = tk.Label(player2_frame, text="Player 2 Current Hand")
player2_label.pack(side=tk.TOP)

player2_hand = tk.Label(player2_frame, text="Player 2 Hand")
player2_hand.pack()

player2_card_frame = tk.Frame(player2_frame)
player2_card_frame.pack(side=tk.TOP)

player2_card1 = tk.Label(player2_card_frame, image=default_img)
player2_card1.image = default_img
player2_card1.card_index = 0
player2_card1.pack(side=tk.LEFT)

player2_card2 = tk.Label(player2_card_frame, image=default_img)
player2_card2.image = default_img
player2_card2.card_index = 0
player2_card2.pack(side=tk.LEFT)

player2_card3 = tk.Label(player2_card_frame, image=default_img)
player2_card3.image = default_img
player2_card3.card_index = 0
player2_card3.pack(side=tk.LEFT)

player2_card4 = tk.Label(player2_card_frame, image=default_img)
player2_card4.image = default_img
player2_card4.card_index = 0
player2_card4.pack(side=tk.LEFT)

player2_card5 = tk.Label(player2_card_frame, image=default_img)
player2_card5.image = default_img
player2_card5.card_index = 0
player2_card5.pack(side=tk.LEFT)

player2_win_chance = tk.Label(player2_frame, text='Win Chance: 0.0')
player2_win_chance.pack(side=tk.BOTTOM)

chopping_frame = tk.Frame(root)

chopping_chance = tk.Label(chopping_frame, text="Chopping Chance: 0.0")
chopping_chance.pack(side=tk.LEFT)

outer_outs_1 = tk.Frame(root)
outs_canvas_1 = tk.Canvas(outer_outs_1, height = 125)
scrollbar1 = tk.Scrollbar(outer_outs_1, orient="horizontal", command=outs_canvas_1.xview)
scrollbar1.pack(side=tk.TOP, fill="x")
outs_canvas_1.pack(fill="x", expand=False)
outs_canvas_1.configure(xscrollcommand=scrollbar1.set)
outs_board_1 = tk.Frame(outs_canvas_1)
outs_canvas_1.create_window((0, 0), window=outs_board_1, anchor="nw")

def update_scrollregion_c1(event):
    outs_canvas_1.update_idletasks()
    outs_canvas_1.config(scrollregion=outs_canvas_1.bbox("all"))

    # Show scrollbar only if needed
    if outs_canvas_1.bbox("all")[2] > outs_canvas_1.winfo_width():
        scrollbar1.pack(side="bottom", fill="x")
    else:
        scrollbar1.forget()

outs_board_1.bind("<Configure>", update_scrollregion_c1)

outer_outs_2 = tk.Frame(root, height=10)
outs_canvas_2 = tk.Canvas(outer_outs_2, height=125)
scrollbar2 = tk.Scrollbar(outer_outs_2, orient="horizontal", command=outs_canvas_2.xview)
scrollbar2.pack(side=tk.BOTTOM, fill="x")
outs_canvas_2.pack(fill="x")
outs_canvas_2.configure(xscrollcommand=scrollbar2.set)
outs_board_2 = tk.Frame(outs_canvas_2)
outs_canvas_2.create_window((0, 0), window=outs_board_2, anchor="nw")

def update_scrollregion_c2(event):
    outs_canvas_2.update_idletasks()
    outs_canvas_2.config(scrollregion=outs_canvas_2.bbox("all"))

    # Show scrollbar only if needed
    if outs_canvas_2.bbox("all")[2] > outs_canvas_2.winfo_width():
        scrollbar2.pack(side="bottom", fill="x")
    else:
        scrollbar2.forget()

outs_board_2.bind("<Configure>", update_scrollregion_c2)

setup_screen(s.cards)

root.mainloop()



