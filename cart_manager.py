"""
Shopping Cart Manager
Handles cart operations and state
"""

from data.menu_data import get_item_by_id


class CartManager:
    def __init__(self):
        self.items = {}  # item_id -> quantity
    
    def add_item(self, item_id, quantity=1):
        """Add item to cart"""
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity
    
    def remove_item(self, item_id):
        """Remove item from cart completely"""
        if item_id in self.items:
            del self.items[item_id]
    
    def update_quantity(self, item_id, quantity):
        """Update item quantity"""
        if quantity <= 0:
            self.remove_item(item_id)
        else:
            self.items[item_id] = quantity
    
    def get_quantity(self, item_id):
        """Get quantity of an item in cart"""
        return self.items.get(item_id, 0)
    
    def get_items(self):
        """Get all cart items with details"""
        cart_items = []
        for item_id, quantity in self.items.items():
            item_data = get_item_by_id(item_id)
            if item_data:
                cart_items.append({
                    **item_data,
                    'quantity': quantity
                })
        return cart_items
    
    def get_item_count(self):
        """Get total number of items in cart"""
        return sum(self.items.values())
    
    def is_empty(self):
        """Check if cart is empty"""
        return len(self.items) == 0
    
    def clear(self):
        """Clear all items from cart"""
        self.items = {}
    
    def get_subtotal(self):
        """Calculate subtotal (before GST)"""
        total = 0
        for item_id, quantity in self.items.items():
            item_data = get_item_by_id(item_id)
            if item_data:
                total += item_data['price'] * quantity
        return total
