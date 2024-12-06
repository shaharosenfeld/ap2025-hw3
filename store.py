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
        matches = [i for i in self._items if item_name.lower() in i.name.lower()]
        matches.sort(key=lambda item: item.name)
        return matches
            

    def search_by_hashtag(self, hashtag: str) -> list:
        matches = [i for i in self._items if hashtag.lower() in i.hashtags]
        matches.sort(key=lambda item: item.name)
        return matches
        

    def add_item(self, item_name: str):
        item = self.search_by_name(item_name)[0]
        self._shopping_cart.add_item(item)
                    
    def remove_item(self, item_name: str):
        matches = self.search_by_name(item_name)
        if len(matches) == 0:
            raise errors.ItemNotExistError(f"Item '{item_name}' not found.")
        if len(matches) > 1:
            raise errors.TooManyMatchesError(f"Too many items found for '{item_name}'")
        if matches[0] not in self._shopping_cart.get_items():
            raise errors.ItemNotExistError(f"Item '{item_name}' not found in your shopping cart.")
        self._shopping_cart.remove_item(matches[0])
    
    def checkout(self) -> int:
        return self._shopping_cart.get_subtotal()
