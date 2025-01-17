class C4State:
    """ A state of the game, i.e. the game board. These are the only functions which are
        absolutely necessary to implement UCT in any 2-player complete information deterministic 
        zero-sum game, although they can be enhanced and made quicker, for example by using a 
        GetRandomMove() function to generate a random move during rollout.
        By convention the players are numbered 1 and 2.
    """
    def __init__(self):
        self.playerJustMoved = 2 # At the root pretend the player just moved is p2 - p1 has the first move
        self.width = 7
        self.board = [[] for x in range(7)] # 0 = empty, 1 = player 1, 2 = player 2

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = C4State()
        st.playerJustMoved = self.playerJustMoved
        st.board = [self.board[i][:] for i in range(self.width)]
        st.width = self.width
        return st

    def getPosition(self, x, y):
        if(0 < x < 7 and 0 < y < len(self.board[x])):
            return self.board[x][y]
        else:
            return None

    def checkArray(self, row):
        check = [None, 0]
        for x in row:
            if(x == check[0] and x != None):
                check[1] += 1
                if(check[1] == 4):
                    return check[0]
            else:
                check = [x, 1]

    def checkWin(self):
        horizontal = [None, 0]

        # Horizontal check
        for y in range(6):            
            row = [self.board[x][y] if y < len(self.board[x]) else None for x in range(7)]
            res = self.checkArray(row)
            if(res != None):                
                return 0 if 1 else 1
            
        #Vertical check
        for col in self.board:
            if(len(col) > 3):
                res = self.checkArray(col + [None]*(7-len(col)))
                if(res != None):
                    return 0 if 1 else 1

        for coord in [(0,2),(0,1), (0,0), (1,0), (2,0),(3,0)]:
            diag1 = [self.getPosition(x + coord[0], x + coord[1]) for x in range(6) if x + coord[0] < 7 and x + coord[1] < 6]
            res = self.checkArray(diag1)
            if(res != None):
                return 0 if 1 else 1
            diag2 = [self.getPosition(x + coord[0], 6 -x - coord[1]) for x in range(6) if x + coord[0] >= 0 and 6 -x - coord[1] >= 0 ]
            res = self.checkArray(diag2)
            if(res != None):
                return 0 if 1 else 1

        return 0.5


        #Diag check
        #for x in range(4):
        #    for y in range(4):
        #        diag_up = [self.getPosition(x, ) for y in range(4)]                    
                        


    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerJustMoved.
        """
        assert move == int(move) and 0 <= move <= 6 and len(self.board[move]) < 7
        self.board[move].append(self.playerJustMoved)
        self.playerJustMoved = 3 - self.playerJustMoved
        
    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        moves = [x for x in range(len(self.board)) if len(self.board[x]) < 6 ]
        res = self.checkWin()
        if(res == 0 or res == 1):
            return []
        return moves
    
    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm. 
        """
        a = self.checkWin()        
        return a


    def __repr__(self):
        """ Don't need this - but good style.
        """
        #st = ""
        #for i in range(7,-1,-1):
        #    st += str([self.getPosition(i, y) if self.getPosition(i, y) != None else " " for y in range(6)])
        #    st += "\n"
        return "\n".join([str(x) for x in self.board])
#state = C4State()
#b = [[1,0,0,0,0],[1],[0],[1],[0],[1],[1]]
#state.board = b
#print(state.board)
#print(state.checkWin())