import uuid
from typing import List, Dict, Optional

def find_order_by_id(orders: List[Dict], order_id: str):
    for order in orders:
        if order["id"] == order_id:
            return order
    return None

def find_item_by_id(inventory: List[Dict], item_id: str):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None

def place_order(inventory: List[Dict], orders: List[Dict], item_id: str, quantity: int, customer_id: str):
    if not customer_id.strip():
        raise ValueError("Customer ID is required.")
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")
    
    item = find_item_by_id(inventory, item_id)

    if not item:
        raise ValueError("Item not found.")
    if item["stock"] < quantity:
        raise ValueError(f"Insufficient stock for {item['name']}. Only {item['stock']} left.")

    item["stock"] -= quantity

    total_price = item["price"] * quantity
    new_order = {
        "order_id": f"{str(uuid.uuid4())}",
        "customer_id": customer_id,
        "item_id": item_id,
        "item_name": item["name"],
        "quantity": quantity,
        "total_price": round(total_price, 2),
        "status": "Placed"
    }
    orders.append(new_order)

    return new_order

def restock_item(inventory: List[Dict], item_id: str, amount: int):
    if amount <= 0:
        raise ValueError("Restock amount must be positive.")
    item = find_item_by_id(inventory, item_id)
    if not item:
        raise ValueError("Item not found.")
    item["stock"] += amount
    return item

def cancel_order(inventory: List[Dict], orders: List[Dict], order_id: str) -> Dict:
    order_to_cancel = find_order_by_id(orders, order_id)
    if not order_to_cancel:
        raise ValueError("Order not found.")
    if order_to_cancel["status"] == "Cancelled":
        raise ValueError("Order is already cancelled.")

    item = find_item_by_id(inventory, order_to_cancel["item_id"])
    if item:
        item["stock"] += order_to_cancel["quantity"]

    order_to_cancel["status"] = "Cancelled"
    return order_to_cancel