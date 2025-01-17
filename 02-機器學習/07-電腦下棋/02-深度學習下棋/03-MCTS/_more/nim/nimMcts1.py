import random
from copy import deepcopy
import math

class NimState:
    def __init__(self, piles=None, player=1):
        # 預設三堆：3, 4, 5 個物品
        self.piles = piles if piles is not None else [3, 4, 5]
        self.player = player  # 1 是玩家, -1 是 AI
        
    def get_possible_moves(self):
        # 回傳所有可能的移動 [(pile_index, remove_count), ...]
        moves = []
        for i, pile in enumerate(self.piles):
            for remove in range(1, pile + 1):
                moves.append((i, remove))
        return moves
    
    def make_move(self, move):
        pile_idx, remove_count = move
        new_piles = self.piles.copy()
        new_piles[pile_idx] -= remove_count
        return NimState(new_piles, -self.player)
    
    def is_terminal(self):
        # 當所有堆都為空時遊戲結束
        return sum(self.piles) == 0
    
    def get_winner(self):
        if not self.is_terminal():
            return None
        return -self.player  # 最後移動的玩家獲勝

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = {}  # {move: Node}
        self.untried_moves = state.get_possible_moves()
        self.visits = 0
        self.wins = 0
    
    def select_child(self):
        # UCB1 選擇
        exploration = math.sqrt(2)
        best_score = float('-inf')
        best_move = None
        best_child = None
        
        for move, child in self.children.items():
            # UCB1 公式
            exploit = child.wins / child.visits
            explore = exploration * math.sqrt(math.log(self.visits) / child.visits)
            score = exploit + explore
            
            if score > best_score:
                best_score = score
                best_move = move
                best_child = child
                
        return best_move, best_child
    
    def expand(self, move):
        next_state = self.state.make_move(move)
        child = Node(next_state, self)
        self.untried_moves.remove(move)
        self.children[move] = child
        return child

def mcts(root_state, iterations=1000):
    root = Node(root_state)
    
    for _ in range(iterations):
        node = root
        state = deepcopy(root_state)
        
        # Selection
        while not node.untried_moves and node.children:
            move, node = node.select_child()
            state = state.make_move(move)
        
        # Expansion
        if node.untried_moves:
            move = random.choice(node.untried_moves)
            state = state.make_move(move)
            node = node.expand(move)
        
        # Simulation
        while not state.is_terminal():
            moves = state.get_possible_moves()
            move = random.choice(moves)
            state = state.make_move(move)
        
        # Backpropagation
        winner = state.get_winner()
        while node:
            node.visits += 1
            if winner == root_state.player:
                node.wins += 1
            node = node.parent
    
    # 選擇最佳移動
    if not root.children:
        return random.choice(root.untried_moves)
    
    return max(root.children.items(),
              key=lambda x: x[1].visits)[0]

def print_game_state(state):
    print("\n現在的堆：")
    for i, pile in enumerate(state.piles):
        print(f"堆 {i}: " + "* " * pile)

def play_game():
    state = NimState()
    print("Nim 遊戲開始！每次可以從一堆中取走任意數量的物品。")
    print("取走最後一個物品的玩家獲勝。")
    
    while not state.is_terminal():
        print_game_state(state)
        
        if state.player == 1:  # 人類玩家
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
        else:  # AI 玩家
            print("\nAI 思考中...")
            move = mcts(state)
            print(f"AI 從堆 {move[0]} 取走了 {move[1]} 個物品")
        
        state = state.make_move(move)
    
    print_game_state(state)
    winner = "AI" if state.get_winner() == -1 else "玩家"
    print(f"\n遊戲結束！{winner} 獲勝！")

if __name__ == "__main__":
    play_game()