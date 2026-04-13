import streamlit as st
from data.data_manager import INVENTORY_PATH, ORDERS_PATH, save_data
from services import kiosk_service


def display_order_form() -> None:
    inventory = st.session_state.inventory
    orders = st.session_state.orders
    item_ids = []
    label_by_id = {}
    for item in inventory:
        item_id = item.get("id")
        if not isinstance(item_id, str):
            continue
        name = str(item.get("name", ""))
        price = float(item.get("price", 0.0))
        stock = int(item.get("stock", 0))
        label_by_id[item_id] = f"{name} — ${price:.2f} (stock: {stock})"
        item_ids.append(item_id)
    if not item_ids:
        st.info("No items available.")
        return
    customer_id = st.text_input("Customer ID", key="order_customer_id")
    selected_item_id = st.selectbox(
        "Select Item",
        item_ids,
        format_func=lambda item_id: label_by_id.get(item_id, item_id),
        key="order_item_id",
    )
    quantity = st.number_input("Quantity", min_value=1, step=1,
        key="order_quantity")
    
    if st.button("Place Order", type="primary"):
        try:
            new_order = kiosk_service.place_order(
                inventory=inventory,
                orders=orders,
                item_id=selected_item_id,
                quantity=int(quantity),
                customer_id=customer_id,
            )
            save_data(inventory, INVENTORY_PATH)
            save_data(orders, ORDERS_PATH)
        except ValueError as exc:
            st.error(str(exc))
        else:
            st.success("Order placed successfully!")
            with st.expander("View Receipt"):
                st.json(new_order)
            st.rerun()