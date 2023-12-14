class Board:
    def __init__(self):
        self.matrix = [
            [0, -1, 0, -1, 0, -1, 0, -1],
            [-1, 0, -1, 0, -1, 0, -1, 0],
            [0, -1, 0, -1, 0, -1, 0, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
        ]
        self.player1_pawns = self.__player_pawns_cords(1)
        self.player2_pawns = self.__player_pawns_cords(-1)

    def __player_pawns_cords(self, player):
        pawns_cords = []
        for row in range(8):
            for column in range(8):
                if self.matrix[row][column] == player:
                    pawns_cords.append([row, column])

        return pawns_cords
