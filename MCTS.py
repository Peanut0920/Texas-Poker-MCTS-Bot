import itertools
import random
from Hand import PokerGame
from typing import List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor

class Node:
    def __init__(self, state: str, parent: Optional['Node'] = None):
        self.state = state
        self.parent = parent
        self.children: List['Node'] = []
        self.visits = 0
        self.wins = 0

    def add_child(self, child_state: str) -> 'Node':
        child_node = Node(child_state, parent=self)
        self.children.append(child_node)
        return child_node

    def update(self, win: float):
        self.visits += 1
        self.wins += win

class MCTS:
    def __init__(self, player_cards: List[Tuple[str, str]], community_cards: List[Tuple[str, str]], length: int = 7, iterations: int = 100, threshold: int = 5, exploration_weight: float = 1.414):
        self.exploration_weight = exploration_weight
        self.threshold = threshold
        self.iterations = iterations
        self.length = length
        self.cards = player_cards + community_cards
        self.suits = ['D', 'C', 'H', 'S']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']

    def select_node(self, node: Node) -> Node:
        best_score = -float('inf')
        best_child = None
        for child in node.children:
            if child.visits == 0:
                score = float('inf')  # Prioritize unexplored nodes
            else:
                exploit = child.wins / child.visits
                explore = self.exploration_weight * ((2 * (child.visits)) ** 0.5 / child.visits)
                score = exploit + explore
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def expand(self, node: Node):
        legal_moves = self.get_legal_moves(node.state)
        for move in legal_moves:
            if not any(child.state == move for child in node.children):
                node.add_child(move)

    def simulate(self, state: str) -> float:
        all_possible_outcomes = self.generate_all_possible_outcomes()
        win_count = 0
        for outcome in all_possible_outcomes:
            game = PokerGame(self.cards[:2], self.cards[2:] + outcome)
            score = game.reward()
            if score > self.threshold:
                win_count += 1
        return win_count / len(all_possible_outcomes)

    def parallel_simulate(self, state: str) -> float:
        all_possible_outcomes = self.generate_all_possible_outcomes()
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(self.simulate_single_outcome, all_possible_outcomes))
        return sum(results) / len(results)

    def simulate_single_outcome(self, outcome: List[Tuple[str, str]]) -> float:
        game = PokerGame(self.cards[:2], self.cards[2:] + outcome)
        score = game.reward()
        return 1 if score > self.threshold else 0

    def backpropagate(self, node: Node, score: float):
        while node:
            node.update(score)
            node = node.parent

    def run(self, root_state: str) -> Node:
        root_node = Node(root_state)
        for _ in range(self.iterations):
            node = root_node
            while node.children:
                node = self.select_node(node)
            self.expand(node)
            if node.children:
                node = random.choice(node.children)
            win = self.parallel_simulate(node.state)
            self.backpropagate(node, win)
        return root_node

    def get_legal_moves(self, state: str) -> List[str]:
        # Implement the logic to generate all legal moves for Texas Poker
        return ['raise', 'fold', 'check', 'call']

    def generate_all_possible_outcomes(self) -> List[List[Tuple[str, str]]]:
        remaining_cards = [(suit, rank) for suit in self.suits for rank in self.ranks
                           if (suit, rank) not in self.cards]
        possible_outcomes = []
        for additional_cards in itertools.combinations(remaining_cards, self.length - len(self.cards)):
            possible_outcomes.append(list(additional_cards))
        return possible_outcomes

    def make_action(self, root_state: str) -> str:
        root_node = self.run(root_state)
        best_child = max(root_node.children, key=lambda child: child.visits)
        return best_child.state

    def raise_bet(self, current_bet: int, raise_amount: int) -> int:
        return current_bet + raise_amount

    def continue_round(self, current_state: str, current_bet: int, raise_amount: int) -> str:
        if current_state == "initial":
            new_bet = self.raise_bet(current_bet, raise_amount)
            return f"raise to {new_bet}"
        else:
            return self.make_action(current_state)
