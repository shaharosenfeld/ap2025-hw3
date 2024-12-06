from item import Item
from errors import ItemNotExistError, ItemAlreadyExistsError


class ShoppingCart:
    
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        # Check if the item is already in the cart
        if item in self.items:
            raise ItemAlreadyExistsError(f"Item '{item.name}' already exists in the cart.")
        self.items.append(item)   

    def remove_item(self, item_name: str):
        # Find the item in the cart
        item_to_remove = next((item for item in self.items if item.name == item_name), None)
        if not item_to_remove:
            raise ItemNotExistError(f"Item '{item_name}' not found.")
        self.items.remove(item_to_remove)

    def get_subtotal(self):
        return sum(item.price for item in self.items)
    
    def get_items(self):
        return self.items
