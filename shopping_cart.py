from item import Item


class ShoppingCart:
    _instance = None
    
    def __new__(cls):
        # Only create the instance once (singltone)
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Initialize the shopping cart with an empty list of items
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.items = []
        
    def add_item(self, item: Item):
        # TODO: Complete
        pass

    def remove_item(self, item_name: str):
        # TODO: Complete
        pass

    def get_subtotal(self) -> int:
        # TODO: Complete
        pass
