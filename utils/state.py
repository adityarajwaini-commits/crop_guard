import streamlit as st

def init_session_state():
    defaults = {
        "page": "Home",
        "dark_mode": True,
        "prediction_history": [],
        "last_prediction": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
