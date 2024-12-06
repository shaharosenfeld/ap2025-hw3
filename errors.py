class ItemNotExistError(Exception):
    """Exception raised when an item does not exist in the store or shopping cart."""
    def __init__(self, message="Item not found"):
        self.message = message
        super().__init__(self.message)


class ItemAlreadyExistsError(Exception):
    pass


class TooManyMatchesError(Exception):
    pass
