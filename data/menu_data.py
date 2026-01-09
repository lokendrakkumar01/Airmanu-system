"""
Menu Data Structure
Contains all restaurant menu items and categories
"""

MENU_DATA = {
    "categories": [
        {
            "id": "starters",
            "name": "Starters",
            "icon": "starters"
        },
        {
            "id": "mains",
            "name": "Main Course",
            "icon": "food"
        },
        {
            "id": "desserts",
            "name": "Desserts",
            "icon": "dessert"
        },
        {
            "id": "beverages",
            "name": "Beverages",
            "icon": "drinks"
        }
    ],
    
    "items": [
        # Starters
        {
            "id": 1,
            "name": "Paneer Tikka",
            "description": "Grilled cottage cheese with spices",
            "price": 180,
            "category": "starters"
        },
        {
            "id": 2,
            "name": "Spring Rolls",
            "description": "Crispy vegetable rolls",
            "price": 120,
            "category": "starters"
        },
        {
            "id": 3,
            "name": "Mushroom Soup",
            "description": "Creamy mushroom soup",
            "price": 100,
            "category": "starters"
        },
        {
            "id": 4,
            "name": "Garlic Bread",
            "description": "Toasted bread with garlic butter",
            "price": 90,
            "category": "starters"
        },
        {
            "id": 5,
            "name": "Chicken Wings",
            "description": "Spicy grilled chicken wings",
            "price": 220,
            "category": "starters"
        },
        
        # Main Course
        {
            "id": 6,
            "name": "Butter Chicken",
            "description": "Rich tomato-based curry with chicken",
            "price": 280,
            "category": "mains"
        },
        {
            "id": 7,
            "name": "Dal Makhani",
            "description": "Black lentils in creamy gravy",
            "price": 200,
            "category": "mains"
        },
        {
            "id": 8,
            "name": "Veg Biryani",
            "description": "Fragrant rice with vegetables",
            "price": 240,
            "category": "mains"
        },
        {
            "id": 9,
            "name": "Paneer Butter Masala",
            "description": "Cottage cheese in rich gravy",
            "price": 260,
            "category": "mains"
        },
        {
            "id": 10,
            "name": "Chicken Biryani",
            "description": "Aromatic rice with chicken",
            "price": 300,
            "category": "mains"
        },
        {
            "id": 11,
            "name": "Pasta Alfredo",
            "description": "Creamy white sauce pasta",
            "price": 250,
            "category": "mains"
        },
        
        # Desserts
        {
            "id": 12,
            "name": "Gulab Jamun",
            "description": "Sweet milk solid balls in syrup",
            "price": 80,
            "category": "desserts"
        },
        {
            "id": 13,
            "name": "Ice Cream Sundae",
            "description": "Vanilla ice cream with toppings",
            "price": 120,
            "category": "desserts"
        },
        {
            "id": 14,
            "name": "Chocolate Brownie",
            "description": "Warm chocolate brownie with ice cream",
            "price": 140,
            "category": "desserts"
        },
        {
            "id": 15,
            "name": "Tiramisu",
            "description": "Italian coffee-flavored dessert",
            "price": 160,
            "category": "desserts"
        },
        
        # Beverages
        {
            "id": 16,
            "name": "Fresh Lime Soda",
            "description": "Refreshing lime drink",
            "price": 60,
            "category": "beverages"
        },
        {
            "id": 17,
            "name": "Mango Shake",
            "description": "Thick mango milkshake",
            "price": 100,
            "category": "beverages"
        },
        {
            "id": 18,
            "name": "Cold Coffee",
            "description": "Iced coffee with milk",
            "price": 90,
            "category": "beverages"
        },
        {
            "id": 19,
            "name": "Masala Chai",
            "description": "Traditional Indian spiced tea",
            "price": 40,
            "category": "beverages"
        },
        {
            "id": 20,
            "name": "Fresh Fruit Juice",
            "description": "Seasonal fruit juice",
            "price": 80,
            "category": "beverages"
        }
    ]
}


def get_categories():
    """Get all menu categories"""
    return MENU_DATA["categories"]


def get_items_by_category(category_id):
    """Get all items for a specific category"""
    return [item for item in MENU_DATA["items"] if item["category"] == category_id]


def get_item_by_id(item_id):
    """Get a specific item by ID"""
    for item in MENU_DATA["items"]:
        if item["id"] == item_id:
            return item
    return None


def get_category_by_id(category_id):
    """Get category info by ID"""
    for cat in MENU_DATA["categories"]:
        if cat["id"] == category_id:
            return cat
    return None
