import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
def custom_css():
    st.markdown(
        """
        <style>
        /* ===== MAIN APP BACKGROUND ===== */
        .stApp {
            background-color: var(--background-color);
        }

        /* ===== SIDEBAR BACKGROUND (BLUE) ===== */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0d47a1, #1565c0);
        }

        /* SIDEBAR TEXT WHITE */
        section[data-testid="stSidebar"] * {
            color: white !important;
        }

        /* ===== CHAT BUBBLES ===== */
        .stChatMessage.user {
            background: linear-gradient(135deg, #ff4d8d, #ff9acb);
            color: white;
            border-radius: 18px 18px 4px 18px;
            padding: 12px 16px;
            margin: 8px 0;
            max-width: 75%;
            margin-left: auto;
        }

        .stChatMessage.assistant {
            background: linear-gradient(135deg, #6a00ff, #b983ff);
            color: white;
            border-radius: 18px 18px 18px 4px;
            padding: 12px 16px;
            margin: 8px 0;
            max-width: 75%;
            margin-right: auto;
        }

        /* ===== INPUT BOX ===== */
        textarea {
            border-radius: 12px !important;
        }

        /* ===== AUTO TEXT COLOR (LIGHT / DARK MODE) ===== */
        @media (prefers-color-scheme: light) {
            h1, h2, h3, p, span, label {
                color: black !important;
            }
        }

        @media (prefers-color-scheme: dark) {
            h1, h2, h3, p, span, label {
                color: white !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

custom_css()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🔐 Gemini Settings")
    st.markdown("Enter your **Gemini API Key** below:")

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza..."
    )

    if api_key:
        st.session_state["GEMINI_API_KEY"] = api_key
        st.success("✅ API Key saved")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# ---------------- TITLE ----------------
st.title("🤖 AI Chatbot using Gemini")
st.write("Built with **Streamlit + Gemini API**")

# ---------------- API KEY CHECK ----------------
if "GEMINI_API_KEY" not in st.session_state:
    st.info("👈 Please add your Gemini API Key from the sidebar")
    st.stop()

# ---------------- GEMINI CONFIG ----------------
genai.configure(api_key=st.session_state["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- CHAT HISTORY ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Type your message here...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    try:
        response = model.generate_content(user_input)
        ai_response = response.text
    except Exception as e:
        ai_response = f"❌ Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(ai_response)

    st.session_state.chat_history.append(("assistant", ai_response))