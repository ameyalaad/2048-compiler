from copy import deepcopy


class Move:
    """
    This class deals with the movement of pieces around the board. The Game class passes inputs from the Storage class to this class 
    """
    @staticmethod
    def left(state, operation, vars):
        """
        Make a left move
        left_move
        """
        current_state = deepcopy(state)
        valid_move, new_score, new_state, new_vars = Move._move_left(current_state, operation, vars)
        return (new_score if valid_move else -1), new_state, new_vars

    @staticmethod
    def right(state, operation, vars):
        """
        Make a right move
        mirror -> left move 
        """
        current_state = deepcopy(state)
        current_state = Move._mirror(current_state)
        current_vars = deepcopy(vars)
        current_vars = Move._mirror(current_vars)
        valid_move, new_score, new_state, new_vars = Move._move_left(current_state, operation, current_vars)
        new_state = Move._mirror(new_state)
        new_vars = Move._mirror(new_vars)
        return (new_score if valid_move else -1), new_state, new_vars

    @staticmethod
    def up(state, operation, vars):
        """
        Make the up move
        transpose -> left move 
        """
        current_state = deepcopy(state)
        current_state = Move._transpose(current_state)
        current_vars = deepcopy(vars)
        current_vars = Move._transpose(current_vars)
        valid_move, new_score, new_state, new_vars = Move._move_left(current_state, operation, current_vars)
        new_state = Move._transpose(new_state)
        new_vars = Move._transpose(new_vars)
        return (new_score if valid_move else -1), new_state, new_vars

    @staticmethod
    def down(state, operation, vars):
        """ 
        Make the down move
        transpose -> mirror -> left move 
        """
        current_state = deepcopy(state)
        current_state = Move._transpose(current_state)
        current_state = Move._mirror(current_state)
        current_vars = deepcopy(vars)
        current_vars = Move._transpose(current_vars)
        current_vars = Move._mirror(current_vars)
        valid_move, new_score, new_state, new_vars = Move._move_left(current_state, operation, current_vars)
        new_state = Move._mirror(new_state)
        new_state = Move._transpose(new_state)
        new_vars = Move._mirror(new_vars)
        new_vars = Move._transpose(new_vars)
        return (new_score if valid_move else -1), new_state, new_vars

    @staticmethod
    def _move_left(current_state, operation, vars):
        """
        The actual code that merges the blocks in a "left move"
        This function will never be called from outside the Move class
        """
        # print(vars)
        new_state = [[-1]*4 for _ in range(4)]
        score = 0  # change in score
        valid_move = False  # valid if atleast 1 shift operation takes place

        for i in range(0, 4):
            nullIndex = 0  # first null index from left
            for j in range(0, 4):
                if current_state[i][j] != -1:
                    if nullIndex >= 1:
                        # Merge Condition
                        if current_state[i][j] == new_state[i][nullIndex-1]:
                            if operation=='ADD':
                                new_state[i][nullIndex-1] *= 2
                            elif operation=='MULTIPLY':
                                new_state[i][nullIndex-1] = new_state[i][nullIndex-1]**2
                            elif operation=='SUBTRACT':
                                new_state[i][nullIndex-1] = -1
                            elif operation=='DIVIDE':
                                new_state[i][nullIndex-1] = 1
                            else:
                                print("Move: error: operation unspecified")
                            score += new_state[i][nullIndex-1]
                            # print("Merge: ", vars[i][nullIndex-1], vars[i][j])
                            vars[i][nullIndex-1].extend(vars[i][j])
                            vars[i][j]=[]
                        else:
                            # print("Do nothing? ")
                            new_state[i][nullIndex] = current_state[i][j]
                            nullIndex += 1
                    else:
                        # print("Move? ")
                        new_state[i][nullIndex] = current_state[i][j]
                        vars[i][nullIndex].extend(vars[i][j])
                        vars[i][j]=[]
                        nullIndex += 1

                    # Condition for tile shifting
                    if j != nullIndex-1:
                        valid_move = True

        return valid_move, score, new_state, vars

    @staticmethod
    def _mirror(state):
        """
        Returns the mirror of the passed state
        This function will never be called from outside the Move class
        """
        for i in range(4):
            for j in range(2):
                state[i][j], state[i][3-j] = state[i][3-j], state[i][j]
        return state

    @staticmethod
    def _transpose(state):
        """
        Returns the transpose of the passed state
        This function will never be called from outside the Move class
        """
        for i in range(4):
            for j in range(i, 4):
                state[i][j], state[j][i] = state[j][i], state[i][j]
        return state
