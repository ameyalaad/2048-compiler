from Move import Move
import random
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Storage:
    """
    This class stores all necessary information for one Game.
    """

    def __init__(self):
        self._score = 0
        self._state = [[-1 for _ in range(4)] for _ in range(4)]
        self._vars = [[[] for i in range(4)] for j in range(4)]

    def get_state(self):
        return self._state

    def set_state(self, new_state):
        self._state = new_state

    def get_value(self, row, col):
        """Row and column should be legal values"""
        return self._state[row][col] if self._state[row][col]!=-1 else 0

    def set_value(self, row, col, newval):
        """Row and column should be legal values"""
        newval = newval if newval!=0 else -1
        self._state[row][col] = newval


    def get_score(self):
        return self._score

    def set_score(self, new_score):
        self._score = new_score

    def logstate(self):
        pstate = [[0 if e == -1 else e for e in l] for l in self._state]
        states = " ".join([" ".join(map(str, l)) for l in pstate])
        states+=" "
        for i in range(4):
            for j in range(4):
                if self._vars[i][j] != []:
                    states += " ".join([str(i+1)+","+str(j+1)+varname for varname in self._vars[i][j]]) + " "
        eprint(states)

    def generate_update(self):
        """
        Generates a tile in a random location, with a number 2 or 4. Directly updates the state.
        """

        # Get -1 elements as indices
        empty_indices = []
        for i in range(4):
            for j in range(4):
                if self._state[i][j] == -1:
                    empty_indices.append(i*4+j)

        try:
            location = random.choice(empty_indices)
        except IndexError as error:
            print("No empty tiles available. Game should now end")
            # Implement move, will check the previous state comparision then

            return

        self._state[location//4][location % 4] = 2
        # print(self._state)

    def get_max_tiles(self):
        return max([max(x) for x in self._state])

    def move(self, direction, operation):
        """
        Do the move with the operation
        """
        score = 0
        current_state = self.get_state()
        if direction=='UP':
            score, new_state, self._vars = Move.up(current_state, operation, self._vars)
            self.set_state(new_state)
        elif direction=='LEFT':
            score, new_state, self._vars = Move.left(current_state, operation, self._vars)
            self.set_state(new_state)
        elif direction=='DOWN':
            score, new_state, self._vars = Move.down(current_state, operation, self._vars)
            self.set_state(new_state)
        elif direction=='RIGHT':
            score, new_state, self._vars = Move.right(current_state, operation, self._vars)
            self.set_state(new_state)
        self.set_score(score)
        return score

    def show_current_state(self):
        """Helper function to pretty-print the current states"""
        print("2048> The current state is: ")
        print("-"*33)
        for i in self._state:
            for j in i:
                if j == -1:
                    print("| \t", end="")
                else:
                    print(f"| {j}\t", end="")
            print("|")
            print("-"*33)

    def check_game_over(self):
        """
        Checks and returns: 
            0 - Game Not Over
            1 - Game Won
            2 - Game Lost
        """

        # Always return zero. There is no game end condition.
        return 0
        # if self.get_max_tiles() == 2048:
        #     return 1

        # num_empty_tiles = 0
        # for i in range(4):
        #     for j in range(4):
        #         if self._state[i][j] == -1:
        #             num_empty_tiles += 1

        # if num_empty_tiles == 0:
        #     # checking for merging tiles
        #     for i in range(3):
        #         for j in range(3):
        #             if(self._state[i][j] == self._state[i + 1][j] or self._state[i][j] == self._state[i][j + 1]):
        #                 return 0

        #     for j in range(3):
        #         if(self._state[3][j] == self._state[3][j + 1]):
        #             return 0

        #     for i in range(3):
        #         if(self._state[i][3] == self._state[i + 1][3]):
        #             return 0
        #     return 2
        # return 0

    def lookup(self, varname):
        for i in range(4):
            for j in range(4):
                if varname in self._vars[i][j]:
                    return ('location', i+1, ',', j+1)
        return None
    
    def newvar(self, varname, row, col):
        if self.lookup(varname):
            return self.lookup(varname)
        else:
            self._vars[row][col].append(varname)
