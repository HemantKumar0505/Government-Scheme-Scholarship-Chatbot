import streamlit as st

def initialize_session():
    """
    Initializes session state variables.
    This ensures each chat has its own memory.
    """
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {
            "age": None,
            "education": None,
            "gender": None,
            "state": None
        }

    if "selected_scheme" not in st.session_state:
        st.session_state.selected_scheme = None


def reset_session():
    """
    Clears session data for a new chat.
    """
    st.session_state.chat_history = []
    st.session_state.user_profile = {
        "age": None,
        "education": None,
        "gender": None,
        "state": None
    }
    st.session_state.selected_scheme = None
