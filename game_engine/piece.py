class Piece:
    def __init__(self, value: int) -> None:
        self.value = value
        self.is_king = False

    def make_king(self) -> None:
        self.is_king = True

    def __eq__(self, other):
        return isinstance(other, Piece) and self.value == other.value
