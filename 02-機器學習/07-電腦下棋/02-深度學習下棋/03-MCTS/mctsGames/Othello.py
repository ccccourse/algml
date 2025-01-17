class OthelloState:
    """ A state of the game of Othello, i.e. the game board.
        The board is a 2D array where 0 = empty (.), 1 = player 1 (X), 2 = player 2 (O).
        In Othello players alternately place pieces on a square board - each piece played
        has to sandwich opponent pieces between the piece played and pieces already on the 
        board. Sandwiched pieces are flipped.
        This implementation modifies the rules to allow variable sized square boards and
        terminates the game as soon as the player about to move cannot make a move (whereas
        the standard game allows for a pass move). 
    """
    def __init__(self,sz = 8):
        self.playerJustMoved = 2 # At the root pretend the player just moved is p2 - p1 has the first move
        self.board = [] # 0 = empty, 1 = player 1, 2 = player 2
        self.size = sz
        assert sz == int(sz) and sz % 2 == 0 # size must be integral and even
        for y in range(sz):
            self.board.append([0]*sz)
        self.board[sz//2][sz//2] = self.board[sz//2-1][sz//2-1] = 1
        self.board[sz//2][sz//2-1] = self.board[sz//2-1][sz//2] = 2

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = OthelloState()
        st.playerJustMoved = self.playerJustMoved
        st.board = [self.board[i][:] for i in range(self.size)]
        st.size = self.size
        return st

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerToMove.
        """
        (x,y)=(move[0],move[1])
        assert x == int(x) and y == int(y) and self.IsOnBoard(x,y) and self.board[x][y] == 0
        m = self.GetAllSandwichedCounters(x,y)
        self.playerJustMoved = 3 - self.playerJustMoved
        self.board[x][y] = self.playerJustMoved
        for (a,b) in m:
            self.board[a][b] = self.playerJustMoved
    
    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        return [(x,y) for x in range(self.size) for y in range(self.size) if self.board[x][y] == 0 and self.ExistsSandwichedCounter(x,y)]

    def AdjacentToEnemy(self,x,y):
        """ Speeds up GetMoves by only considering squares which are adjacent to an enemy-occupied square.
        """
        for (dx,dy) in [(0,+1),(+1,+1),(+1,0),(+1,-1),(0,-1),(-1,-1),(-1,0),(-1,+1)]:
            if self.IsOnBoard(x+dx,y+dy) and self.board[x+dx][y+dy] == self.playerJustMoved:
                return True
        return False
    
    def AdjacentEnemyDirections(self,x,y):
        """ Speeds up GetMoves by only considering squares which are adjacent to an enemy-occupied square.
        """
        es = []
        for (dx,dy) in [(0,+1),(+1,+1),(+1,0),(+1,-1),(0,-1),(-1,-1),(-1,0),(-1,+1)]:
            if self.IsOnBoard(x+dx,y+dy) and self.board[x+dx][y+dy] == self.playerJustMoved:
                es.append((dx,dy))
        return es
    
    def ExistsSandwichedCounter(self,x,y):
        """ Does there exist at least one counter which would be flipped if my counter was placed at (x,y)?
        """
        for (dx,dy) in self.AdjacentEnemyDirections(x,y):
            if len(self.SandwichedCounters(x,y,dx,dy)) > 0:
                return True
        return False
    
    def GetAllSandwichedCounters(self, x, y):
        """ Is (x,y) a possible move (i.e. opponent counters are sandwiched between (x,y) and my counter in some direction)?
        """
        sandwiched = []
        for (dx,dy) in self.AdjacentEnemyDirections(x,y):
            sandwiched.extend(self.SandwichedCounters(x,y,dx,dy))
        return sandwiched

    def SandwichedCounters(self, x, y, dx, dy):
        """ Return the coordinates of all opponent counters sandwiched between (x,y) and my counter.
        """
        x += dx
        y += dy
        sandwiched = []
        while self.IsOnBoard(x,y) and self.board[x][y] == self.playerJustMoved:
            sandwiched.append((x,y))
            x += dx
            y += dy
        if self.IsOnBoard(x,y) and self.board[x][y] == 3 - self.playerJustMoved:
            return sandwiched
        else:
            return [] # nothing sandwiched

    def IsOnBoard(self, x, y):
        return x >= 0 and x < self.size and y >= 0 and y < self.size
    
    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm. 
        """
        jmcount = len([(x,y) for x in range(self.size) for y in range(self.size) if self.board[x][y] == playerjm])
        notjmcount = len([(x,y) for x in range(self.size) for y in range(self.size) if self.board[x][y] == 3 - playerjm])
        if jmcount > notjmcount: return 1.0
        elif notjmcount > jmcount: return 0.0
        else: return 0.5 # draw

    def __repr__(self):
        s= ""
        for y in range(self.size-1,-1,-1):
            for x in range(self.size):
                s += ".XO"[self.board[x][y]]
            s += "\n"
        return s