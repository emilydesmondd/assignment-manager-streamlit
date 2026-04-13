import streamlit as st


def display_dashboard() -> None:
    inventory = st.session_state.inventory
    search = st.text_input("Search item name", placeholder="e.g., Latte").strip().lower()
    filtered = [
    item
    for item in inventory
    if not search or search in str(item.get("name", "")).lower()
    ]
    total_units = sum(int(item.get("stock", 0)) for item in inventory)
    low_stock = [item for item in inventory if int(item.get("stock", 0)) < 10]
    c1, c2, c3 = st.columns(3)
    c1.metric("Unique Items", len(inventory))
    c2.metric("Total Units In Stock", total_units)
    c3.metric("Low Stock Items (<10)", len(low_stock))
    if low_stock:
        st.warning(
            "Low stock: "
            + ", ".join(f"{item['name']} ({item['stock']})" for item in low_stock)
        )
    st.subheader("Inventory")
    st.dataframe(filtered, use_container_width=True, hide_index=True)