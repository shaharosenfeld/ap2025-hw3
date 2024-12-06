import yaml
from item import Item
from shopping_cart import ShoppingCart
from errors import ItemNotExistError, ItemAlreadyExistsError, TooManyMatchesError

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

    def search_by_name(self, search_phrase: str):
        filtered_items = [item for item in self._items if search_phrase.lower() in item.name.lower()]
        return sorted(filtered_items, key=lambda item: item.name)
            

    def search_by_hashtag(self, hashtag: str):
        filtered_items = [item for item in self._items if hashtag.lower() in item.hashtags]
        return sorted(filtered_items, key=lambda item: item.name)
        

    def add_item(self, item):
        if not item or len(item.name.split()) < 2:
            raise TooManyMatchesError(f"Item name '{item.name}' is too generic.")
        if item in self._items:
            raise ItemAlreadyExistsError(f"Item '{item.name}' already exists.")
        self._items.append(item)
                    
    def remove_item(self, item_name):
        item = next((item for item in self._items if item.name == item_name), None)
        if not item:
            raise ItemNotExistError(f"Item '{item_name}' not found in the store.")
        self._items.remove(item)
        # Also remove the item from the shopping cart if it's there
        self._shopping_cart.remove_item(item_name)
    
    def checkout(self) -> int:
        return self._shopping_cart.get_subtotal()
