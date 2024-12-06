from item import Item
from errors import ItemNotExistError, ItemAlreadyExistsError, TooManyMatchesError


class ShoppingCart:
    
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        if item in self.items:
            raise ItemAlreadyExistsError(f"Item '{item.name}' already exists in the shopping cart.")
        self.items.append(item)

    def remove_item(self, item_name):
        # Search for an item by name
        matching_items = [item for item in self.items if item_name.lower() in item.name.lower()]
        if len(matching_items) == 0:
            raise ItemNotExistError(f"Item '{item_name}' not found in the shopping cart.")       
        if len(matching_items) > 1:
            raise TooManyMatchesError(f"Too many matches for the substring '{item_name}'.")
        item_to_remove = matching_items[0]
        self.items.remove(item_to_remove)


    def get_subtotal(self):
        return sum(item.price for item in self.items)
    
    def get_items(self):
        return self.items
