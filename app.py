# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
from dotenv import load_dotenv
load_dotenv()

# --------------------------------------------------
# Imports
# --------------------------------------------------
import streamlit as st
from utils.eligibility import get_eligible_schemes
from utils.ai_helper import generate_ai_response

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Government Scheme & Scholarship Chatbot",
    page_icon="🏛️",
    layout="wide"
)

# --------------------------------------------------
# Load CSS
# --------------------------------------------------
def load_css():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# --------------------------------------------------
# Session initialization
# --------------------------------------------------
if "all_chats" not in st.session_state:
    st.session_state.all_chats = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = []

if "active_chat_index" not in st.session_state:
    st.session_state.active_chat_index = None

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "age": None,
        "education": None,
        "gender": None,
        "state": None
    }

if "eligible_schemes" not in st.session_state:
    st.session_state.eligible_schemes = []

if "selected_scheme" not in st.session_state:
    st.session_state.selected_scheme = None

if "awaiting_scheme_selection" not in st.session_state:
    st.session_state.awaiting_scheme_selection = False

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.title("🏛️ Gov Scheme Assistant")

    # New Chat
    if st.button("🆕 New Chat"):
        if st.session_state.current_chat:
            st.session_state.all_chats.append({
                "title": f"Chat {len(st.session_state.all_chats) + 1}",
                "messages": st.session_state.current_chat
            })

        st.session_state.current_chat = []
        st.session_state.active_chat_index = None
        st.session_state.selected_scheme = None
        st.session_state.eligible_schemes = []
        st.session_state.awaiting_scheme_selection = False
        st.rerun()

    st.markdown("### 🕘 Previous Chats")
    if st.session_state.all_chats:
        for idx, chat in enumerate(st.session_state.all_chats):
            if st.button(chat["title"], key=f"chat_{idx}"):
                st.session_state.current_chat = chat["messages"]
                st.session_state.active_chat_index = idx
                st.session_state.selected_scheme = None
                st.session_state.eligible_schemes = []
                st.session_state.awaiting_scheme_selection = False
                st.rerun()
    else:
        st.caption("No previous chats yet")

    st.markdown("---")
    st.markdown("### 👤 User Profile")

    st.session_state.user_profile["age"] = st.number_input("Age", 1, 100)
    st.session_state.user_profile["education"] = st.selectbox(
        "Education",
        ["", "School", "Higher Secondary", "Diploma",
         "Undergraduate", "Postgraduate", "Research"]
    )
    st.session_state.user_profile["gender"] = st.selectbox(
        "Gender", ["", "Male", "Female", "Other"]
    )
    st.session_state.user_profile["state"] = st.text_input("State")

# --------------------------------------------------
# Main Chat UI
# --------------------------------------------------
st.title("💬 Government Scheme & Scholarship Chatbot")

for msg in st.session_state.current_chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

user_input = st.chat_input("Ask about schemes, benefits, deadlines...")

# --------------------------------------------------
# Chat Logic
# --------------------------------------------------
if user_input:
    st.session_state.current_chat.append({
        "role": "user",
        "content": user_input
    })

    text = user_input.lower()
    profile = st.session_state.user_profile

    # --------------------------------------------------
    # Scheme selection state
    # --------------------------------------------------
    if st.session_state.awaiting_scheme_selection:
        selected = None
        for i, s in enumerate(st.session_state.eligible_schemes, start=1):
            if text.strip() == str(i) or s["scheme_name"].lower() in text:
                selected = s
                break

        if selected:
            st.session_state.selected_scheme = selected
            st.session_state.awaiting_scheme_selection = False

            reply = (
                f"✅ You selected **{selected['scheme_name']}**.\n\n"
                "You can now ask about:\n"
                "- documents required\n"
                "- benefits\n"
                "- eligibility\n"
                "- age limits\n"
                "- deadline\n"
                "- how to apply\n"
                "- or ask for an explanation"
            )
        else:
            reply = "Please select a valid scheme number or scheme name."

    # --------------------------------------------------
    # Follow-up state (IMPROVED CONVERSATION LOGIC)
    # --------------------------------------------------
    elif st.session_state.selected_scheme:
        s = st.session_state.selected_scheme

        # 🔹 Overview / explain more intent
        if any(phrase in text for phrase in [
            "tell me about", "explain", "explain more",
            "more detail", "in a better way",
            "describe", "overview", "details"
        ]):
            prompt = (
                "You are a government scheme assistant.\n\n"
                "Explain the following scholarship clearly in simple English.\n"
                "Structure the answer as:\n"
                "1. Purpose of the scheme\n"
                "2. Who it is meant for\n"
                "3. What financial support is provided\n"
                "4. Why this scheme is important\n\n"
                "Use 4–6 sentences. Do not repeat information.\n\n"
                f"Scheme name: {s['scheme_name']}\n"
                f"Description: {s['description']}\n"
                f"Benefits: {s['benefits']}"
            )
            reply = generate_ai_response(prompt)

        elif "document" in text:
            reply = (
                "The following documents are required to apply:\n\n- "
                + "\n- ".join(s["documents_required"])
            )

        elif "benefit" in text:
            reply = (
                f"The main benefit of this scheme is financial assistance of "
                f"{s['benefits']}. This support helps students manage tuition "
                "fees and academic expenses."
            )

        elif "deadline" in text or "last date" in text:
            reply = (
                f"The last date to apply for this scheme is {s['last_date']}. "
                "Applicants are advised to apply well before the deadline."
            )

        elif "age" in text:
            reply = (
                f"The eligible age range for this scheme is "
                f"{s['min_age']} to {s['max_age']} years."
            )

        elif "apply" in text:
            reply = (
                "You can apply using the following process:\n\n"
                f"{s['how_to_apply']}"
            )

        elif "eligibility" in text:
            prompt = (
                "Explain the eligibility criteria clearly in simple English.\n\n"
                + s["description"]
            )
            reply = generate_ai_response(prompt)

        # 🔹 Strong AI fallback
        else:
            prompt = (
                "You are an official government scheme chatbot.\n\n"
                "Answer the user's question clearly and politely.\n"
                "If the question is vague, give a helpful overview.\n"
                "Do not repeat sentences. Do not exaggerate.\n"
                "If there is no guarantee, say so clearly.\n\n"
                f"User question: {text}\n\n"
                f"Scheme name: {s['scheme_name']}\n"
                f"Description: {s['description']}\n"
                f"Benefits: {s['benefits']}\n"
                f"Age eligibility: {s['min_age']} to {s['max_age']}"
            )
            reply = generate_ai_response(prompt)

    # --------------------------------------------------
    # Recommendation state
    # --------------------------------------------------
    else:
        missing = [k for k, v in profile.items() if not v]

        if missing:
            reply = "Please provide the following details first: " + ", ".join(missing)
        else:
            schemes = get_eligible_schemes(profile)
            st.session_state.eligible_schemes = schemes

            if not schemes:
                reply = "No schemes found for your profile."
            else:
                st.session_state.awaiting_scheme_selection = True
                reply = "Here are the schemes you are eligible for:\n\n"

                for i, s in enumerate(schemes, start=1):
                    reply += f"""
<div class="scheme-card">
  <div class="scheme-title">{i}. {s['scheme_name']}</div>
  <div class="scheme-badge">{s['scheme_level']}</div>
</div>
"""

                reply += "<p><strong>Select a scheme by number or name.</strong></p>"

    st.session_state.current_chat.append({
        "role": "assistant",
        "content": reply
    })

    st.rerun()
