import streamlit as st

from data.data_manager import load_data, save_data, INVENTORY_PATH, ORDERS_PATH
from services import kiosk_service

st.set_page_config(page_title="Smart Coffee Kiosk", layout="wide")


with st.sidebar:
    st.title("App Information")
    st.info("This is the control panel for the Smart Coffee Kiosk.")

st.title("Smart Coffee Kiosk")

if 'inventory' not in st.session_state:
    st.session_state.inventory = load_data(INVENTORY_PATH)
if 'orders' not in st.session_state:
    st.session_state.orders = load_data(ORDERS_PATH)

tab1, tab2, tab3, tab4 = st.tabs(["Dashboard &amp; Search", "Place Order","Restock Items", "Manage Orders"
])
with tab1:
    st.header("Inventory Dashboard")
    st.write("Dashboard UI will go here.")
    st.write(st.session_state.inventory)

with tab2:
    st.header("Place a New Order")
    st.write("Order form UI will go here.")

with tab3:
    st.header("Restock Inventory")
    st.write("Restock UI will go here.")

with tab4:
    st.header("Manage Existing Orders")
    st.write("Order management UI will go here.")
    st.write(st.session_state.orders)