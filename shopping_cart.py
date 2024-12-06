from item import Item
import errors


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
            self.items = []
            self._initialized = True
        
    def add_item(self, item):
        # Check if the item already exists in the cart
        for cart_item in self.items:
            if cart_item.name == item.name:
                raise errors.ItemAlreadyExistsError(f"{item.name} is already in the cart.")
        self.items.append(item)   

    def remove_item(self, item_name):
        # Check if the item exists in the cart
        item_to_remove = None
        for cart_item in self.items:
            if cart_item.name == item_name:
                item_to_remove = cart_item
                break
        if item_to_remove is None:
            raise errors.ItemNotExistError(f"{item_name} is not in the cart.")
        self.items.remove(item_to_remove)

    def get_subtotal(self) -> float:
        total = 0.0
        for item in self.items:  
            total += item.price
        return total
    
    def get_items(self):
        return self.items
