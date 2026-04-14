import time
from langchain_core.tools import tool

@tool
def get_all_products() -> str:
    """Use this to fetch a list of all available products, including their names, IDs, and prices."""
    print("Calling mock product listing API...")
    time.sleep(1) 
    products = [
        {"id": "P001", "name": "Wireless Bluetooth Headphones", "price": 79.99, "category": "Electronics"},
        {"id": "P002", "name": "Ergonomic Office Chair", "price": 199.50, "category": "Home Office"},
        {"id": "P003", "name": "Smart LED Desk Lamp", "price": 45.00, "category": "Home Office"},
        {"id": "P004", "name": "Portable SSD 1TB", "price": 120.00, "category": "Electronics"},
        {"id": "P005", "name": "Yoga Mat Deluxe", "price": 29.99, "category": "Fitness"}
    ]
    return str(products)

@tool
def get_product_details(product_id: str) -> str:
    """Use this to fetch specific details about a single product. You must provide the product_id (e.g., P001)."""
    print(f"Calling mock product details API for {product_id}...")
    time.sleep(0.8) 
    products = [
        {"id": "P001", "name": "Wireless Bluetooth Headphones", "price": 79.99, "category": "Electronics"},
        {"id": "P002", "name": "Ergonomic Office Chair", "price": 199.50, "category": "Home Office"},
        {"id": "P003", "name": "Smart LED Desk Lamp", "price": 45.00, "category": "Home Office"},
        {"id": "P004", "name": "Portable SSD 1TB", "price": 120.00, "category": "Electronics"},
        {"id": "P005", "name": "Yoga Mat Deluxe", "price": 29.99, "category": "Fitness"}
    ]
    for product in products:
        if product["id"].lower() == product_id.lower():
            return str(product)
    return "Product not found."

@tool
def track_order_status(order_id: str) -> str:
    """Use this to track the status of a user's order. You must provide the order_id (e.g., ORD001)."""
    print(f"Calling mock order tracking API for {order_id}...")
    time.sleep(1.5) # Simulate network delay
    statuses = {
        "ORD001": {"status": "Shipped", "estimated_delivery": "2024-08-10", "carrier": "FedEx"},
        "ORD002": {"status": "Processing", "estimated_delivery": "2024-08-15", "carrier": "UPS"},
        "ORD003": {"status": "Delivered", "delivery_date": "2024-08-01"},
        "ORD004": {"status": "Out for Delivery", "estimated_delivery": "2024-08-08", "carrier": "DHL"}
    }
    return str(statuses.get(order_id.upper(), {"status": "Order ID not found."}))

@tool
def get_pricing_plans() -> str:
    """Use this to fetch available SaaS or e-commerce pricing and subscription plans."""
    print("Calling mock pricing plans API...")
    time.sleep(0.7) # Simulate network delay
    plans = [
        {"name": "Basic", "price": "$10/month", "features": ["5GB storage", "Email support"]},
        {"name": "Pro", "price": "$25/month", "features": ["50GB storage", "Priority support", "Advanced analytics"]},
        {"name": "Enterprise", "price": "Custom", "features": ["Unlimited storage", "24/7 Phone support", "Dedicated account manager"]}
    ]
    return str(plans)

@tool
def get_active_offers() -> str:
    """Use this to check for any current discounts, promo codes, or special offers on products."""
    print("Calling mock offers API...")
    time.sleep(0.5)
    offers = [
        {"product_id": "P001", "product_name": "Wireless Bluetooth Headphones", "offer": "10% off with code AUDIO10"},
        {"product_id": "P002", "product_name": "Ergonomic Office Chair", "offer": "Free shipping this week"},
        {"product_id": "P005", "product_name": "Yoga Mat Deluxe", "offer": "Buy 1 Get 1 50% off"}
    ]
    return str(offers)