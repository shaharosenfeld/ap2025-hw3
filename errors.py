class ItemNotExistError(Exception):
    def __init__(self, message="Item not found"):
        self.message = message
        super().__init__(self.message)


class ItemAlreadyExistsError(Exception):
    def __init__(self, message="Item already exists in the cart"):
        self.message = message
        super().__init__(self.message)


class TooManyMatchesError(Exception):
    def __init__(self, message="Too many matches found"):
        self.message = message
        super().__init__(self.message)
