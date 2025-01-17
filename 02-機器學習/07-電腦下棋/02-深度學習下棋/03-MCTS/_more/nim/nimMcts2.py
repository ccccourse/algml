import random
from copy import deepcopy
import math

class NimState:
    def __init__(self, piles=None, player=1):
        self.piles = piles if piles is not None else [3, 4, 5]
        self.player = player  # 1 是玩家, -1 是 AI
    
    def calculate_nim_sum(self):
        result = 0
        for pile in self.piles:
            result ^= pile
        return result
    
    def get_possible_moves(self):
        moves = []
        nim_sum = self.calculate_nim_sum()
        
        for i, pile in enumerate(self.piles):
            if pile > 0:  # 只考慮非空的堆
                for remove in range(1, pile + 1):
                    # 計算移動後的 nim-sum
                    new_piles = self.piles.copy()
                    new_piles[i] -= remove
                    new_state = NimState(new_piles, -self.player)
                    if new_state.calculate_nim_sum() == 0:
                        moves.insert(0, (i, remove))
                    else:
                        moves.append((i, remove))
        return moves
    
    def make_move(self, move):
        if move is None or not isinstance(move, tuple):
            raise ValueError("Invalid move")
        pile_idx, remove_count = move
        if pile_idx >= len(self.piles) or remove_count > self.piles[pile_idx]:
            raise ValueError("Invalid move")
        new_piles = self.piles.copy()
        new_piles[pile_idx] -= remove_count
        return NimState(new_piles, -self.player)
    
    def is_terminal(self):
        return sum(self.piles) == 0
    
    def get_winner(self):
        if not self.is_terminal():
            return None
        return -self.player
    
    def evaluate(self):
        if self.is_terminal():
            return float('inf') if self.get_winner() == -1 else float('-inf')
        
        nim_sum = self.calculate_nim_sum()
        total_pieces = sum(self.piles)
        non_empty_piles = sum(1 for p in self.piles if p > 0)
        
        score = 0
        if nim_sum == 0:
            score -= 50  # 不好的狀態
        else:
            score += 50  # 有獲勝機會的狀態
        
        if total_pieces == 1:
            score += 100 if self.player == -1 else -100
            
        score += 10 * non_empty_piles
        return score * self.player

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = {}
        self.untried_moves = state.get_possible_moves()
        self.visits = 0
        self.wins = 0
        self.value = 0
    
    def select_child(self):
        if not self.children:
            return None, None
        
        exploration = math.sqrt(2)
        best_score = float('-inf')
        best_move = None
        best_child = None
        
        for move, child in self.children.items():
            if child.visits == 0:
                continue
                
            exploit = child.value / child.visits
            explore = exploration * math.sqrt(math.log(self.visits) / child.visits)
            state_value = child.state.evaluate() / 100
            
            score = exploit + explore + state_value
            
            if score > best_score:
                best_score = score
                best_move = move
                best_child = child
        
        if best_move is None and self.children:
            # 如果沒有找到最佳移動，隨機選擇一個
            best_move, best_child = random.choice(list(self.children.items()))
            
        return best_move, best_child
    
    def expand(self, move):
        next_state = self.state.make_move(move)
        child = Node(next_state, self)
        self.untried_moves.remove(move)
        self.children[move] = child
        return child

def mcts(root_state, iterations=5000):
    root = Node(root_state)
    
    # 如果只有一個可能的移動，直接返回
    possible_moves = root_state.get_possible_moves()
    if len(possible_moves) == 1:
        return possible_moves[0]
    
    for _ in range(iterations):
        node = root
        state = deepcopy(root_state)
        
        # Selection
        while not node.untried_moves and node.children:
            move, next_node = node.select_child()
            if move is None or next_node is None:
                break
            state = state.make_move(move)
            node = next_node
        
        # Expansion
        if node.untried_moves:
            move = random.choice(node.untried_moves)
            state = state.make_move(move)
            node = node.expand(move)
        
        # Simulation
        depth = 0
        while not state.is_terminal() and depth < 10:
            moves = state.get_possible_moves()
            if not moves:
                break
            if random.random() < 0.7 and moves:
                move = moves[0]
            else:
                move = random.choice(moves)
            state = state.make_move(move)
            depth += 1
        
        # Backpropagation
        value = state.evaluate()
        while node:
            node.visits += 1
            node.value += value
            if state.get_winner() == root_state.player:
                node.wins += 1
            node = node.parent
    
    # 選擇最佳移動
    if not root.children:
        return possible_moves[0]
    
    best_move = None
    best_value = float('-inf')
    
    for move, child in root.children.items():
        if child.visits == 0:
            continue
        value = child.wins / child.visits
        if value > best_value:
            best_value = value
            best_move = move
    
    if best_move is None:
        return random.choice(possible_moves)
    
    return best_move

def print_game_state(state):
    print("\n現在的堆：")
    for i, pile in enumerate(state.piles):
        print(f"堆 {i}: " + "* " * pile)
    print(f"Nim-sum: {state.calculate_nim_sum()}")

def play_game():
    state = NimState()
    print("Nim 遊戲開始！每次可以從一堆中取走任意數量的物品。")
    print("取走最後一個物品的玩家獲勝。")
    
    while not state.is_terminal():
        print_game_state(state)
        
        if state.player == 1:
            valid_move = False
            while not valid_move:
                try:
                    pile = int(input("選擇堆 (0-2): "))
                    count = int(input(f"要取走多少個 (1-{state.piles[pile]}): "))
                    move = (pile, count)
                    if move in state.get_possible_moves():
                        valid_move = True
                    else:
                        print("無效的移動，請重試。")
                except (ValueError, IndexError):
                    print("無效的輸入，請重試。")
        else:
            print("\nAI 思考中...")
            move = mcts(state)
            print(f"AI 從堆 {move[0]} 取走了 {move[1]} 個物品")
        
        state = state.make_move(move)
    
    print_game_state(state)
    winner = "AI" if state.get_winner() == -1 else "玩家"
    print(f"\n遊戲結束！{winner} 獲勝！")

if __name__ == "__main__":
    play_game()