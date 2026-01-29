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
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Government Scheme Chatbot",
    page_icon="🏛️",
    layout="wide"
)

# --------------------------------------------------
# Load custom CSS
# --------------------------------------------------
def load_css():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# --------------------------------------------------
# Session state initialization
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
        "state": None,
        "occupation": None
    }

if "eligible_schemes" not in st.session_state:
    st.session_state.eligible_schemes = []

if "selected_scheme" not in st.session_state:
    st.session_state.selected_scheme = None

if "awaiting_scheme_selection" not in st.session_state:
    st.session_state.awaiting_scheme_selection = False

if "show_results" not in st.session_state:
    st.session_state.show_results = False

# --------------------------------------------------
# Helper: AI reasoning (WHY scheme fits user)
# --------------------------------------------------
def generate_reasoning(scheme, profile):
    prompt = f"""
You are a helpful government assistant.

Explain WHY this scheme is suitable for the user.
Speak in simple English.
Do NOT list technical fields.
Do NOT repeat the scheme name.

User details:
Age: {profile.get('age')}
Education: {profile.get('education')}
Occupation: {profile.get('occupation')}
State: {profile.get('state')}

Scheme info:
Description: {scheme.get('description')}
Benefits: {scheme.get('benefits')}

Write 2–3 sentences.
"""
    return generate_ai_response(prompt)

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
        st.session_state.selected_scheme = None
        st.session_state.eligible_schemes = []
        st.session_state.awaiting_scheme_selection = False
        st.session_state.show_results = False
        st.rerun()

    st.markdown("### 🕘 Previous Chats")
    for idx, chat in enumerate(st.session_state.all_chats):
        if st.button(chat["title"], key=f"chat_{idx}"):
            st.session_state.current_chat = chat["messages"]
            st.session_state.selected_scheme = None
            st.session_state.show_results = False
            st.rerun()

    st.markdown("---")
    st.markdown("### 👤 User Profile")

    st.session_state.user_profile["age"] = st.number_input("Age", 1, 100)

    st.session_state.user_profile["education"] = st.selectbox(
        "Education",
        [
            "", "No Formal Education", "School", "Higher Secondary",
            "Diploma", "Undergraduate", "Postgraduate",
            "Research", "Skill Training"
        ]
    )

    st.session_state.user_profile["gender"] = st.selectbox(
        "Gender", ["", "Male", "Female", "Other"]
    )

    st.session_state.user_profile["occupation"] = st.selectbox(
        "Occupation",
        [
            "", "Student", "Unemployed", "Employed",
            "Self-Employed", "Farmer", "Apprentice",
            "Senior Citizen", "Homemaker"
        ]
    )

    st.session_state.user_profile["state"] = st.text_input("State")

    # BUTTON: Show eligible schemes
    if st.button("🎯 Show Eligible Schemes"):
        st.session_state.show_results = True

# --------------------------------------------------
# Main Chat UI
# --------------------------------------------------
st.title("💬 Government Scheme & Scholarship Chatbot")

for msg in st.session_state.current_chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

user_input = st.chat_input(
    "Ask about schemes, benefits, eligibility, deadlines, or applications..."
)

# --------------------------------------------------
# Recommendation Trigger (BUTTON-BASED)
# --------------------------------------------------
if st.session_state.show_results and not st.session_state.awaiting_scheme_selection:
    profile = st.session_state.user_profile
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
                reason = generate_reasoning(s, profile)

                reply += f"""
<div class="scheme-card">
  <div class="scheme-title">{i}. {s['scheme_name']}</div>
  <div class="scheme-badge">{s['scheme_level']}</div>
  <p><em>Why this scheme fits you:</em> {reason}</p>
</div>
"""

            reply += "<p><strong>Select a scheme by number or name.</strong></p>"

    st.session_state.current_chat.append({
        "role": "assistant",
        "content": reply
    })

    st.session_state.show_results = False
    st.rerun()

# --------------------------------------------------
# Chat Input Logic
# --------------------------------------------------
if user_input:
    st.session_state.current_chat.append({
        "role": "user",
        "content": user_input
    })

    text = user_input.lower()

    # Scheme selection
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
                "- benefits\n"
                "- eligibility\n"
                "- documents\n"
                "- age limits\n"
                "- deadline\n"
                "- how to apply\n"
                "- application portal\n"
                "- explanation"
            )
        else:
            reply = "Please select a valid scheme number or scheme name."

    # Follow-up on selected scheme
    elif st.session_state.selected_scheme:
        s = st.session_state.selected_scheme

        if any(k in text for k in ["purpose", "why", "explain", "about", "details"]):
            prompt = f"""
Explain the purpose of this government scheme in very simple English.
Assume the user has no prior knowledge.
Use 3–4 sentences.

Scheme description:
{s['description']}
"""
            reply = generate_ai_response(prompt)

        elif "benefit" in text:
            reply = f"The benefits of this scheme include: {s['benefits']}."

        elif "document" in text:
            reply = "Documents required:\n- " + "\n- ".join(s["documents_required"])

        elif "deadline" in text or "last date" in text:
            reply = (
                "This scheme has a rolling application process. "
                "You can apply anytime."
                if s["last_date"].lower() == "rolling"
                else f"The last date to apply is {s['last_date']}."
            )

        elif "age" in text:
            reply = f"Eligible age range: {s['min_age']} to {s['max_age']} years."

        elif "apply" in text or "portal" in text:
            reply = (
                f"{s['how_to_apply']}\n\n"
                f"🔗 Official portal: {s.get('application_url', 'Please check official government website')}"
            )
        else:
            prompt = f"""
Answer the user's question clearly and politely.
If there is no guarantee, say so honestly.

User question: {text}

Scheme details:
{s['description']}
Benefits: {s['benefits']}
"""
            reply = generate_ai_response(prompt)

    else:
        reply = (
            "Please click **Show Eligible Schemes** after filling your profile "
            "to see schemes relevant to you."
        )

    st.session_state.current_chat.append({
        "role": "assistant",
        "content": reply
    })

    st.rerun()
