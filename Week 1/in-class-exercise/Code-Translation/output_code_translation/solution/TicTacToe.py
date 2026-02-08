class TicTacToe:
<<<<<<< Updated upstream
    def __init__(self, N=3):
        self.board = [[' ' for _ in range(N)] for _ in range(3)]
        self.current_player = 'X'

    def make_move(self, row, col):
=======
    def __init__(self, N: int = 3):
        # Initialize a 3xN board filled with spaces
        self.board = [[' ' for _ in range(N)] for _ in range(3)]
        self.current_player = 'X'

    def make_move(self, row: int, col: int) -> bool:
        """Attempt to place the current player's mark at (row, col).
        Returns True if the move was successful, False if the cell is already occupied."""
>>>>>>> Stashed changes
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
<<<<<<< Updated upstream
=======
        """Return 'X' or 'O' if there is a winner, otherwise None."""
        # Check rows
>>>>>>> Stashed changes
        for row in self.board:
            if row[0] != ' ' and row[0] == row[1] and row[1] == row[2]:
                return row[0]

        for col in range(3):
<<<<<<< Updated upstream
            if self.board[0][col] != ' ' and self.board[0][col] == self.board[1][col] and self.board[1][col] == self.board[2][col]:
                return self.board[0][col]

        if self.board[0][0] != ' ' and self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
            return self.board[0][0]

        if self.board[0][2] != ' ' and self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]:
            return self.board[0][2]
        return '\0'

    def is_board_full(self):
=======
            if (
                self.board[0][col] != ' '
                and self.board[0][col] == self.board[1][col] == self.board[2][col]
            ):
                return self.board[0][col]

        # Check main diagonal
        if (
            self.board[0][0] != ' '
            and self.board[0][0] == self.board[1][1] == self.board[2][2]
        ):
            return self.board[0][0]

        # Check anti-diagonal
        if (
            self.board[0][2] != ' '
            and self.board[0][2] == self.board[1][1] == self.board[2][0]
        ):
            return self.board[0][2]

        return None

    def is_board_full(self) -> bool:
        """Return True if the board has no empty spaces."""
>>>>>>> Stashed changes
        for row in self.board:
            if ' ' in row:
                return False
        return True

<<<<<<< Updated upstream
    def get_current_player(self):
=======
    def get_current_player(self) -> str:
        """Return the symbol of the player whose turn it is."""
>>>>>>> Stashed changes
        return self.current_player
