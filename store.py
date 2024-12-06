import yaml
from item import Item
from shopping_cart import ShoppingCart
import errors

class Store:
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items

    def search_by_name(self, item_name: str) -> list:
        matches = [i for i in self._items if i.name == item_name]
        if not matches:
            print(f"Item '{item_name}' not found.")
            return []  # Return an empty list instead of raising an error
        return matches
        

    def search_by_hashtag(self, hashtag: str) -> list:
        matches = [i for i in self._items if hashtag in i.hashtags]
        if not matches:
            print(f"Item not found with the given hashtag: {hashtag}")
            return []  # Return an empty list instead of raising an error
        return matches
        

    def add_item(self, item_name: str):
        if not item_name.strip():
            raise errors.ItemNotExistError(f"Item '{item_name}' not found.")
        
        matches = self.search_by_name(item_name)
        if matches:
            if matches[0] in self._shopping_cart.get_items():
                raise errors.ItemAlreadyExistsError(f"Item '{item_name}' already exists in the cart.")
            self._shopping_cart.add_item(matches[0])
        else:
            raise errors.ItemNotExistError(f"Item '{item_name}' not found.")
                    
    def remove_item(self, item_name: str):
        matches = self.search_by_name(item_name)
        if matches:
            if matches[0] not in self._shopping_cart.get_items():
                raise errors.ItemNotExistError(f"Item '{item_name}' not found in your shopping cart.")
            self._shopping_cart.remove_item(matches[0])
        else:
            raise errors.ItemNotExistError(f"Item '{item_name}' not found in the store.")
    
    def checkout(self) -> int:
        return self._shopping_cart.get_subtotal()
