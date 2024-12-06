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
            self._initialized = True
            self.items = {}
        
    def add_item(self, item: Item):
        if item.name in self.items:
            raise errors.ItemAlreadyExistsError
        else:
            self.items[item.name] = item  #syntax reminder: items[key] = value  --> {key,value}
        

    def remove_item(self, item_name: str):
        if item_name in self.items:
            del self.items[item_name]
        else:
            raise errors.ItemNotExistError

    def get_subtotal(self) -> int:
        sum = 0.00
        for i in self.items.values():  #we itarate over the values(items) and not over key(item name)
            sum += i.price
        return sum
    
    def get_items(self):
        return self.items
