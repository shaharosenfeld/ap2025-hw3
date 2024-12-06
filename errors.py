class ItemNotExistError(Exception):
    def __init__(self, message="Item not found"):
        self.message = message
        super().__init__(self.message)


class ItemAlreadyExistsError(Exception):
    pass


class TooManyMatchesError(Exception):
    pass
