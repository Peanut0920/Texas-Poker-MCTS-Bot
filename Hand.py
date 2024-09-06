import random
from collections import Counter
import math
import itertools
import pygame

class Card:
    def __init__(self):
        self.suits = ['D', 'C', 'H', 'S']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
        self.cards = [(suit, rank) for suit in self.suits for rank in self.ranks]
        self.backup = [(suit, rank) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)
    def Shuffle(self):
        random.shuffle(self.cards)
        print("Shuffle!")

    def Reset(self):
        print("Reset Successfully.")
        self.__init__()

class Player:
    def __init__(self, cards, name):
        self.name = name
        self.cards = []
        self.card_1 = cards.pop(random.randint(0, len(cards) - 1))
        self.card_2 = cards.pop(random.randint(0, len(cards) - 1))
        self.selected_card = [self.card_1, self.card_2]
        self.cards.extend(self.selected_card)
        print(f"{self.name}: {self.cards}")

        self.amount = 50000
        self.bet_amount = 0
        self.current_bet = 0

        self.check = False
        self.fold = False
        self.call = False
        self.raisecall = False
        self.action_seq = []

    def Fold(self):
        self.fold = True
        self.action_seq.append(("fold", 0))
        print(f"{self.name} Fold")

    def Call(self, amount):
        if amount > self.amount:
            print(f"{self.name} cannot call. Not enough funds.")
            return
        self.amount -= amount
        self.bet_amount += amount
        self.call = True
        print(self.call)
        self.action_seq.append(("call", amount))
        print(f"{self.name} Call: Bet: RM {amount}")

    def Raise(self, amount):
        total_bet = self.current_bet + amount
        if total_bet > self.amount:
            print(f"{self.name} cannot raise. Not enough funds.")
            return
        self.amount -= amount
        self.bet_amount += amount
        self.current_bet += amount
        self.raisecall = True
        self.action_seq.append(("raise", amount))
        print(f"{self.name} Raise: Bet: RM {amount}")

    def Check(self):
        self.check = True
        self.action_seq.append(("check", 0))
        print(f"{self.name} Check")

    def reset(self):
        self.check = False
        self.fold = False
        self.call = False
        self.raisecall = False
        self.current_bet = 0
        self.action_seq = []

    def reset_action(self):
        self.check = False
        self.fold = False
        self.call = False
        self.raisecall = False

class Community:
    def __init__(self,cards):
        self.card = []
        self.card_1 = cards.pop(random.randint(0,len(cards)-1))
        self.card_2 = cards.pop(random.randint(0,len(cards)-1))
        self.card_3 = cards.pop(random.randint(0,len(cards)-1))
        self.selected_cards = [self.card_1, self.card_2, self.card_3]
        self.card.extend(self.selected_cards)
    def FourthCard(self,cards):
        self.card_4 = cards.pop(random.randint(0,len(cards)-1))
        self.selected_cards = [self.card_4]
        self.card.extend(self.selected_cards)
    def FirthCard(self,cards):
        self.card_5 = cards.pop(random.randint(0,len(cards)-1))
        self.selected_cards = [self.card_5]
        self.card.extend(self.selected_cards)

class PokerGame:
    def __init__(self, player_card, community_card=[]):
        self.list = player_card + community_card
        self.rank_presence, self.suit_positions, self.sorted_cards = self.get_suitrank_presence()
    def get_suitrank_presence(self):
        rank_mapping = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12, '13': 13, '14': 14}
        suit_mapping = {'D': 1, 'C': 2, 'S': 3, 'H': 4}

        rank_presence = [False] * 13  # Initialize 13 positions for ranks 2 to 14
        suit_positions = [None] * 13  # Initialize 13 positions for the suits of ranks 2 to 14
        sorted_cards = []
        for card in self.list:
            rank = rank_mapping[card[1]]
            suit = suit_mapping[card[0]]
            index = rank - 2  # Convert rank to 0-based index
            suit_positions[index] = suit
            rank_presence[index] = True
            sorted_cards.append((rank, suit))
        
        sorted_cards.sort(reverse=True, key=lambda x: x[0])
        return rank_presence, suit_positions, sorted_cards
    def is_flush(self):
        suit_count = [0] * 4  # Initialize counts for each suit
        suits = [[] for _ in range(4)]
        for rank, suit in self.sorted_cards:
            suit_count[suit - 1] += 1
            suits[suit - 1].append(rank)
            if suit_count[suit - 1] >= 5:
                return True, suits[suit - 1][:5]
        return False, []
    def is_straight(self):
        consecutive_count = 0
        last_rank = -1
        straight_cards = []
        for presence, (rank, _) in zip(self.rank_presence, self.sorted_cards):
            if presence:
                if last_rank == -1 or rank == last_rank - 1:
                    consecutive_count += 1
                    straight_cards.append(rank)
                    last_rank = rank
                    if consecutive_count == 5:
                        return True, straight_cards[:5]
                elif rank != last_rank:
                    consecutive_count = 1
                    straight_cards = [rank]
                    last_rank = rank
        # Special case for A-2-3-4-5 straight (wheel straight)
        if consecutive_count == 4 and self.rank_presence[12]:  # Ace
            return True, straight_cards + [14]
        return False, []
    def is_straight_flush(self):
        is_flush, flush_cards = self.is_flush()
        if is_flush:
            flush_cards.sort(reverse=True)
            consecutive_count = 0
            last_rank = -1
            straight_flush_cards = []
            for rank in flush_cards:
                if last_rank == -1 or rank == last_rank - 1:
                    consecutive_count += 1
                    straight_flush_cards.append(rank)
                    last_rank = rank
                    if consecutive_count == 5:
                        return True, straight_flush_cards[:5]
                elif rank != last_rank:
                    consecutive_count = 1
                    straight_flush_cards = [rank]
                    last_rank = rank
            if consecutive_count == 4 and 14 in flush_cards:
                return True, straight_flush_cards + [14]
        return False, []
    def is_four_of_a_kind(self):
        rank_counts = {rank: 0 for rank in range(2, 15)}
        for rank, _ in self.sorted_cards:
            rank_counts[rank] += 1
            if rank_counts[rank] == 4:
                kicker = max([card[0] for card in self.sorted_cards if card[0] != rank])
                return True, [rank] * 4 + [kicker]
        return False, []
    def is_full_house(self):
        rank_counts = {rank: 0 for rank in range(2, 15)}
        for rank, _ in self.sorted_cards:
            rank_counts[rank] += 1
        three_of_a_kind = [rank for rank, count in rank_counts.items() if count >= 3]
        pairs = [rank for rank, count in rank_counts.items() if count >= 2 and rank not in three_of_a_kind]
        if three_of_a_kind and pairs:
            return True, [max(three_of_a_kind)] * 3 + [max(pairs)] * 2
        if len(three_of_a_kind) >= 2:
            return True, [max(three_of_a_kind)] * 3 + [min(three_of_a_kind)] * 2
        return False, []
    def is_three_of_a_kind(self):
        rank_counts = {rank: 0 for rank in range(2, 15)}
        for rank, _ in self.sorted_cards:
            rank_counts[rank] += 1
            if rank_counts[rank] == 3:
                kickers = [card[0] for card in self.sorted_cards if card[0] != rank][:2]
                return True, [rank] * 3 + kickers
        return False, []
    def is_two_pair(self):
        rank_counts = {rank: 0 for rank in range(2, 15)}
        for rank, _ in self.sorted_cards:
            rank_counts[rank] += 1
        pairs = [rank for rank, count in rank_counts.items() if count >= 2]
        if len(pairs) >= 2:
            high_pair = max(pairs)
            low_pair = min(pairs)
            non_pair_cards = [card[0] for card in self.sorted_cards if card[0] not in pairs]
            if non_pair_cards:
                kicker = max(non_pair_cards)
            else:
                kicker = None
            return True, [high_pair] * 2 + [low_pair] * 2 + [kicker] if kicker else [high_pair] * 2 + [low_pair] * 2
        return False, []
    def is_one_pair(self):
        rank_counts = {rank: 0 for rank in range(2, 15)}
        for rank, _ in self.sorted_cards:
            rank_counts[rank] += 1
            if rank_counts[rank] == 2:
                kickers = [card[0] for card in self.sorted_cards if card[0] != rank][:3]
                return True, [rank] * 2 + kickers
        return False, []
    def high_card(self):
        return True, [card[0] for card in self.sorted_cards[:5]]
    def evaluate_hand(self):
        if self.is_straight_flush()[0]:
            return "Straight Flush", self.is_straight_flush()[1]
        if self.is_four_of_a_kind()[0]:
            return "Four of a Kind", self.is_four_of_a_kind()[1]
        if self.is_full_house()[0]:
            return "Full House", self.is_full_house()[1]
        if self.is_flush()[0]:
            return "Flush", self.is_flush()[1]
        if self.is_straight()[0]:
            return "Straight", self.is_straight()[1]
        if self.is_three_of_a_kind()[0]:
            return "Three of a Kind", self.is_three_of_a_kind()[1]
        if self.is_two_pair()[0]:
            return "Two Pair", self.is_two_pair()[1]
        if self.is_one_pair()[0]:
            return "One Pair", self.is_one_pair()[1]
        if self.high_card()[0]:
            return "High Card", self.high_card()[1]
    def compare_hands(player1, player2):
        ranking = ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House",
                   "Four of a Kind", "Straight Flush"]
        player1_rank, player1_values = player1.evaluate_hand()
        player2_rank, player2_values = player2.evaluate_hand()
        if ranking.index(player1_rank) > ranking.index(player2_rank):
            return "Player 1 wins with " + player1_rank
        elif ranking.index(player1_rank) < ranking.index(player2_rank):
            return "Bot wins with " + player2_rank
        else:
            if player1_values > player2_values:
                return "Player 1 wins with " + player1_rank
            elif player1_values < player2_values:
                return "Bot wins with " + player2_rank
            else:
                player1_suits = [card[1] for card in player1.sorted_cards]
                player2_suits = [card[1] for card in player2.sorted_cards]
                for self_suit, other_suit in zip(self_suits, other_suits):
                    if player1_suits > player2_suits:
                        return "Player 1 wins with higher suit"
                    elif player1_suits < player2_suits:
                        return "Bot wins with higher suit"
                return "It's a tie"

    def display_hand_image(hand_type):
        image_files = {
            "Straight Flush": "images/straightflush.png",
            "Four of a Kind": "images/fourofakind.png",
            "Full House": "images/fullhouse.png",
            "Flush": "images/flush.png",
            "Straight": "images/straight.png",
            "Three of a Kind": "images/threeofakind.png",
            "Two Pair": "images/twopair.png",
            "One Pair": "images/onepair.png",
            "High Card": "images/highcards.png"
        }
        if hand_type not in image_files:
            return

        screen = pygame.display.get_surface()
        image = pygame.image.load(image_files[hand_type])
        image = pygame.transform.scale(image, (200, 200))
        screen.blit(image, (480, 380))
        pygame.display.flip()
    def reward(self):
        hand,Card = self.evaluate_hand()
        level = {
            "Straight Flush": 10,
            "Four of a Kind": 9,
            "Full House": 8,
            "Flush": 7,
            "Straight": 5,
            "Three of a Kind": 4,
            "Two Pair": 3,
            "One Pair": 2,
            "High Card": 1,
            "error": 0
        }
        return level.get(hand, 0)
    def compare_hands_multiple_player(self, players):
        ranking = ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House",
                   "Four of a Kind", "Straight Flush"]

        best_player = None
        best_rank = -1
        best_values = []
        best_kickers = []

        for player in players:
            player_rank, player_values = player.evaluate_hand()
            player_kickers = player.get_kickers()
            player_rank_index = ranking.index(player_rank)

            if player_rank_index > best_rank:
                best_player = player
                best_rank = player_rank_index
                best_values = player_values
                best_kickers = player_kickers
            elif player_rank_index == best_rank:
                if player_values > best_values:
                    best_player = player
                    best_values = player_values
                    best_kickers = player_kickers
                elif player_values == best_values:
                    for player_kicker, best_kicker in zip(player_kickers, best_kickers):
                        if player_kicker > best_kicker:
                            best_player = player
                            best_kickers = player_kickers
                            break
                        elif player_kicker < best_kicker:
                            break

        return f"{best_player.name} wins with {ranking[best_rank]}"

class Betting:
    def __init__(self):
        self.pot = 0
        self.current_bet = 0
        self.players = []
        self.current_player_index = -1
        self.round = 1

    def add_player(self, player):
        self.players.append(player)

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return self.players[self.current_player_index]

    def all_players_acted(self):
        return all(player.check or player.fold or player.call or player.raisecall for player in self.players)

    def start_round(self):
        self.current_bet = 0
        for player in self.players:
            player.reset_action()
        print("Betting round started.")

    def end_round(self):
        print(f"Betting round ended. Pot is RM {self.pot}")
        for player in self.players:
            player.reset_action()

    def update_pot(self, amount):
        self.pot += amount





    def reset_round(self):
        print(f"Betting round ended. Pot is RM {self.pot}")
        self.current_bet = 0
        self.current_player_index = 0
        self.pot = 0
        for player in self.players:
            player.reset()
        print("Round reset.")


        
       














