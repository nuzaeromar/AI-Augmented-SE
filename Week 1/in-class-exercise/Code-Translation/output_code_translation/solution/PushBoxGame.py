class PushBoxGame:
    def __init__(self, map=None):
<<<<<<< Updated upstream
        if map is None:
            map = []
        self.map = map
        self.player_row = 0
        self.player_col = 0
        self.targets = []
        self.boxes = []
=======
        """
        Initialize the game.
        :param map: Optional list of strings representing the game board.
        """
        if map is None:
            map = []
        self.map = list(map)  # ensure we have a mutable copy
        self.player_row = 0
        self.player_col = 0
        self.targets = []          # list of (row, col) tuples
        self.boxes = []            # list of (row, col) tuples
>>>>>>> Stashed changes
        self.target_count = 0
        self._is_game_over = False
        self.init_game()

<<<<<<< Updated upstream
    def gat_map(self):
        return self.map

    def is_game_over(self):
        return self._is_game_over

    def get_player_col(self):
        return self.player_col

    def get_player_row(self):
        return self.player_row

    def get_targets(self):
        return self.targets

    def get_boxes(self):
        return self.boxes

    def get_target_count(self):
        return self.target_count

    def init_game(self):
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                if self.map[row][col] == 'O':
                    self.player_row = row
                    self.player_col = col
                elif self.map[row][col] == 'G':
                    self.targets.append((row, col))
                    self.target_count += 1
                elif self.map[row][col] == 'X':
                    self.boxes.append((row, col))

    def check_win(self):
        box_on_target_count = 0
        for box in self.boxes:
            if box in self.targets:
=======
    def gat_map(self) -> list:
        """
        Return the current map representation.
        """
        return self.map

    def is_game_over(self) -> bool:
        """
        Return whether the game has been won.
        """
        return self._is_game_over

    def get_player_col(self) -> int:
        """
        Return the column index of the player.
        """
        return self.player_col

    def get_player_row(self) -> int:
        """
        Return the row index of the player.
        """
        return self.player_row

    def get_targets(self) -> list:
        """
        Return a list of target positions as (row, col) tuples.
        """
        return self.targets

    def get_boxes(self) -> list:
        """
        Return a list of box positions as (row, col) tuples.
        """
        return self.boxes

    def get_target_count(self) -> int:
        """
        Return the total number of targets on the map.
        """
        return self.target_count

    def init_game(self):
        """
        Scan the map to locate the player, targets and boxes.
        """
        self.targets.clear()
        self.boxes.clear()
        self.target_count = 0
        for row_idx, row_str in enumerate(self.map):
            for col_idx, ch in enumerate(row_str):
                if ch == 'O':                     # player start
                    self.player_row = row_idx
                    self.player_col = col_idx
                elif ch == 'G':                   # target
                    self.targets.append((row_idx, col_idx))
                    self.target_count += 1
                elif ch == 'X':                   # box
                    self.boxes.append((row_idx, col_idx))

    def check_win(self) -> bool:
        """
        Determine if all boxes are on targets.
        """
        box_on_target_count = 0
        target_set = set(self.targets)
        for box in self.boxes:
            if box in target_set:
>>>>>>> Stashed changes
                box_on_target_count += 1
        if box_on_target_count == self.target_count:
            self._is_game_over = True
        return self._is_game_over

<<<<<<< Updated upstream
    def move(self, direction):
=======
    def move(self, direction: str) -> bool:
        """
        Attempt to move the player in the given direction.
        Direction is one of 'w' (up), 's' (down), 'a' (left), 'd' (right).
        Returns True if the move results in a win, otherwise False.
        """
>>>>>>> Stashed changes
        new_player_row = self.player_row
        new_player_col = self.player_col

        if direction == 'w':
            new_player_row -= 1
        elif direction == 's':
            new_player_row += 1
        elif direction == 'a':
            new_player_col -= 1
        elif direction == 'd':
            new_player_col += 1
        else:
            # Invalid direction; no movement.
            return self._is_game_over

        # Ensure the new position is within map bounds
        if not (0 <= new_player_row < len(self.map) and
                0 <= new_player_col < len(self.map[new_player_row])):
            return self._is_game_over

        if self.map[new_player_row][new_player_col] != '#':
<<<<<<< Updated upstream
            if (new_player_row, new_player_col) in self.boxes:
                new_box_row = new_player_row + (new_player_row - self.player_row)
                new_box_col = new_player_col + (new_player_col - self.player_col)

                if self.map[new_box_row][new_box_col] != '#':
                    self.boxes.remove((new_player_row, new_player_col))
=======
            next_pos = (new_player_row, new_player_col)
            if next_pos in self.boxes:
                # Compute where the box would be pushed
                new_box_row = new_player_row + (new_player_row - self.player_row)
                new_box_col = new_player_col + (new_player_col - self.player_col)

                # Verify new box cell is inside map and not a wall
                if (0 <= new_box_row < len(self.map) and
                        0 <= new_box_col < len(self.map[new_box_row]) and
                        self.map[new_box_row][new_box_col] != '#'):
                    # Move the box
                    self.boxes.remove(next_pos)
>>>>>>> Stashed changes
                    self.boxes.append((new_box_row, new_box_col))
                    # Move the player
                    self.player_row = new_player_row
                    self.player_col = new_player_col
            else:
                # No box, just move the player
                self.player_row = new_player_row
                self.player_col = new_player_col

        return self.check_win()
