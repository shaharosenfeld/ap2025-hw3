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
        matches = []
        for i in self._items:
            if i.name == item_name:
                matches.append(i)
        if not matches:
            print(f"Item '{item_name}' not found.")  # Log the error without raising an exception
            return []  # Or you can return None if you prefer
        return matches
        

    def search_by_hashtag(self, hashtag: str) -> list:
        matches = []
        for i in self._items:
            if hashtag in i.hashtags:  # Check if the hashtag exists in the list of hashtags
                matches.append(i)
        if not matches:
            raise errors.ItemNotExistError("Item not found with the given hashtag")
        return matches
        

    def add_item(self, item_name: str):
        matches = self.search_by_name(item_name)
        if matches:
            self._shopping_cart.add_item(matches[0])
        else:
            raise errors.ItemAlreadyExistsError("Item already in shopping cart")

    def remove_item(self, item_name: str):
        matches = self.search_by_name(item_name)
        if matches:
            self._shopping_cart.remove_item(matches[0])
        else:
            raise errors.ItemNotExistError("Item not found in your shopping cart")

    def checkout(self) -> int:
        return self._shopping_cart.get_subtotal()
