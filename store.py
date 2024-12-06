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

     
    def _get_cart_hashtags(self):
        #Get all hashtags from items in the shopping cart, including duplicates"""
        cart_hashtags = []
        for item in self._shopping_cart.get_items():
            cart_hashtags.extend(item.hashtags)
        return cart_hashtags
    
    def count_common_hashtags(self, item_hashtags, cart_hashtags):
        #Count how many hashtags an item shares with the cart items
        count = 0
        for tag in item_hashtags:
            count += cart_hashtags.count(tag)
        return count
    
    def _sort_items(self, items):
        """Sort items based on common hashtags with cart and lexicographical order"""
        cart_hashtags = self._get_cart_hashtags()
        
        # Create tuples of (item, common_hashtag_count) for sorting
        items_with_counts = [
            (item, self.count_common_hashtags(item.hashtags, cart_hashtags))
            for item in items
        ]
        
        # Sort first by common hashtag count (descending) then by name
        return [
            item for item, _ in sorted(
                items_with_counts,
                key=lambda x: (-x[1], x[0].name)  # Negative count for descending order
            )
        ]
        
    def search_by_name(self, search_phrase: str):
        # Filter out items already in cart
        cart_items = set(self._shopping_cart.get_items())
        filtered_items = [
            item for item in self._items 
            if search_phrase in item.name and item not in cart_items
        ]
        return self._sort_items(filtered_items)

    def search_by_hashtag(self, hashtag: str):
        # Filter out items already in cart
        cart_items = set(self._shopping_cart.get_items())
        matching_items = [
            item for item in self._items 
            if hashtag in item.hashtags and item not in cart_items
        ]
        return self._sort_items(matching_items)

    def add_item(self, item_name: str):
        #Check if the item exists in the store's inventory
        matching_items = [item for item in self._items if item_name in item.name]
        if len(matching_items) == 0:
            # No matching item found
            raise ItemNotExistError(f"Item '{item_name}' not found in the store.")     
        if len(matching_items) > 1:
            # More than one match found
            raise TooManyMatchesError(f"Too many matches for the name '{item_name}'.")
        # Get the matched item
        item_to_add = matching_items[0]

        #Check if the item is already in the shopping cart
        if item_to_add in self._shopping_cart.get_items():
            raise ItemAlreadyExistsError(f"Item '{item_name}' is already in the shopping cart.")

        #Add the item to the shopping cart
        self._shopping_cart.add_item(item_to_add)
                    
    def remove_item(self, item_name: str):
        #Find matching items in the shopping cart using substring matching
        matching_items = [item for item in self._shopping_cart.get_items() if item_name in item.name]
        if len(matching_items) == 0:
            # No matching item found
            raise ItemNotExistError(f"Item '{item_name}' not found in the shopping cart.")
        
        if len(matching_items) > 1:
            #More than one match found, raise TooManyMatchesError
            raise TooManyMatchesError(f"Too many matches for the substring '{item_name}'.")
        #Remove the matched item from the shopping cart
        item_to_remove = matching_items[0]
        self._shopping_cart.remove_item(item_to_remove.name)
    
    def checkout(self) -> int:
        return self._shopping_cart.get_subtotal()
