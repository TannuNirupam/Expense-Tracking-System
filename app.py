import streamlit as st
from add_update_tab import add_update_tab
from analytics_ui import analytics_tab

st.title("Expense Tracking system")

tab1, tab2 = st.tabs(["Add/Update","Analytics"])


with tab1:
    add_update_tab()
with tab2:
    analytics_tab()
          
            # You can send `expenses` to your backend here
