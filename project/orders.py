import json, os
from config import ORDERS_FILE

def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return {}
    try:
        with open(ORDERS_FILE, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
    except json.JSONDecodeError:
        print("[warning] orders.json corrupted, resetting.")
        return {}

def save_orders(orders):
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)

def store_order(order):
    orders = load_orders()
    orders[order["txn_id"]] = order
    save_orders(orders)

def update_order(txn_id, updates):
    orders = load_orders()
    if txn_id in orders:
        orders[txn_id].update(updates)
        save_orders(orders)

def get_order(txn_id):
    orders = load_orders()
    return orders.get(txn_id)

def find_pending_by_amount_and_payer(amount, payer):
    orders = load_orders()
    result = []
    for txid, o in orders.items():
        if o["status"] == "PENDING" and abs(o["full_amount"] - amount) < 0.01 and o["expected_payer"].lower() == payer.lower():
            result.append((txid, o["fraction"]))
    return result

def count_pending():
    orders = load_orders()
    return sum(1 for o in orders.values() if o["status"] == "PENDING")
