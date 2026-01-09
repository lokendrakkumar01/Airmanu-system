"""
Billing Engine
Calculates subtotal, GST, and total amount
"""

from datetime import datetime
from config import GST_RATE, RESTAURANT_NAME, CURRENCY_SYMBOL


class BillingEngine:
    @staticmethod
    def calculate_subtotal(cart_items):
        """Calculate subtotal from cart items"""
        subtotal = 0
        for item in cart_items:
            subtotal += item['price'] * item['quantity']
        return subtotal
    
    @staticmethod
    def calculate_gst(subtotal, gst_rate=GST_RATE):
        """Calculate GST amount"""
        return subtotal * gst_rate
    
    @staticmethod
    def calculate_total(subtotal, gst_amount):
        """Calculate total amount"""
        return subtotal + gst_amount
    
    @staticmethod
    def generate_receipt(cart_items):
        """
        Generate receipt data
        Returns dict with all billing information
        """
        subtotal = BillingEngine.calculate_subtotal(cart_items)
        gst = BillingEngine.calculate_gst(subtotal)
        total = BillingEngine.calculate_total(subtotal, gst)
        
        receipt = {
            'restaurant': RESTAURANT_NAME,
            'date': datetime.now().strftime('%d/%m/%Y'),
            'time': datetime.now().strftime('%I:%M %p'),
            'items': cart_items,
            'subtotal': subtotal,
            'gst_rate': GST_RATE * 100,  # Convert to percentage
            'gst_amount': gst,
            'total': total,
            'currency': CURRENCY_SYMBOL
        }
        
        return receipt
    
    @staticmethod
    def format_price(amount, currency=CURRENCY_SYMBOL):
        """Format price with currency symbol"""
        return f"{currency}{amount:.2f}"
