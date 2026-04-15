import streamlit as st
import uuid
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
from database import init_db, create_user, login_user, save_history, get_history

# ── INIT ─────────────────────────
init_db()

st.set_page_config(
    page_title="Creatix Lab · AI Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── SESSION STATE ─────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None

if "chats" not in st.session_state:
    st.session_state.chats = {}   # chat_id -> {title, messages, results}

if "active_chat" not in st.session_state:
    st.session_state.active_chat = None

if "running" not in st.session_state:
    st.session_state.running = False


# ── LOGIN PAGE ─────────────────────────
if not st.session_state.user:

    st.markdown("<h1 style='text-align:center;'>🔐 Creatix Lab</h1>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        u = st.text_input("Username", key="login_user")
        p = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = login_user(u, p)
            if user:
                st.session_state.user = u
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

    with tab2:
        u2 = st.text_input("New Username", key="reg_user")
        p2 = st.text_input("New Password", type="password", key="reg_pass")

        if st.button("Register"):
            if create_user(u2, p2):
                st.session_state.user = u2
                st.rerun()
            else:
                st.error("❌ Username exists")

    st.stop()

st.markdown("""
<style>

/* ── BACKGROUND ── */
.stApp {
    background: #050507;
    color: #ffffff;
}

/* ── HERO TITLE ── */
h1 {
    font-weight: 800;
    color: white !important;
}

h1 span {
    color: #ff8c32 !important;
}

/* ── CHAT BUBBLES ── */
.chat-user {
    background: linear-gradient(135deg, #ff8c32, #ff3d00);
    padding: 10px 14px;
    border-radius: 12px;
    margin: 8px 0;
    color: white;
    max-width: 80%;
}

.chat-bot {
    background: rgba(255,255,255,0.06);
    padding: 10px 14px;
    border-radius: 12px;
    margin: 8px 0;
    color: #f1f1f1;
    border: 1px solid rgba(255,255,255,0.08);
    max-width: 80%;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.7);
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32, #ff3d00);
    color: white;
    border-radius: 10px;
    border: none;
}

/* ── INPUT BOX ── */
.stTextInput input {
    background: #ffffff !important;
    color: #000000 !important;
}

/* ── INFO TEXT ── */
.stInfo {
    background-color: rgba(255,255,255,0.05);
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ─────────────────────────
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user}")

    # NEW CHAT
    if st.button("➕ New Chat"):
        chat_id = str(uuid.uuid4())[:8]

        st.session_state.chats[chat_id] = {
            "title": "New Chat",
            "messages": [],
            "results": {}
        }

        st.session_state.active_chat = chat_id
        st.rerun()

    # CLEAR ALL HISTORY
    if st.button("🧹 Clear All Chats"):
        st.session_state.chats = {}
        st.session_state.active_chat = None
        st.rerun()

    st.markdown("## 💬 Chats")

    for cid, chat in st.session_state.chats.items():
        if st.button(chat["title"], key=cid):
            st.session_state.active_chat = cid

    st.markdown("---")

    if st.button("🚪 Logout"):
        st.session_state.user = None
        st.session_state.chats = {}
        st.session_state.active_chat = None
        st.rerun()


# ── HERO ─────────────────────────
st.markdown("""
<h1 style='text-align:center;'>Creatix <span style="color:#ff8c32;">Research</span></h1>
<p style='text-align:center;color:#bbb;'>Multi-agent AI research system</p>
<hr>
""", unsafe_allow_html=True)


# ── GET ACTIVE CHAT ─────────────────────────
chat_id = st.session_state.active_chat

if chat_id and chat_id in st.session_state.chats:
    chat = st.session_state.chats[chat_id]
else:
    chat = None


# ── INPUT ─────────────────────────
topic = st.text_input("Research Topic")
run = st.button("⚡ Run Research")


# ── RUN PIPELINE ─────────────────────────
if run and topic:

    st.session_state.running = True

    # CREATE CHAT IF NOT EXISTS
    if chat_id is None:
        chat_id = str(uuid.uuid4())[:8]
        st.session_state.active_chat = chat_id

        st.session_state.chats[chat_id] = {
            "title": topic[:30],
            "messages": [],
            "results": {}
        }

    chat = st.session_state.chats[chat_id]

    chat["messages"].append({"role": "user", "content": topic})

    # PIPELINE
    s = build_search_agent().invoke(f"Find detailed information about: {topic}")
    search = s.content

    r = build_reader_agent().invoke(search[:1000])
    reader = r.content

    writer = writer_chain.invoke({
        "topic": topic,
        "research": search + "\n\n" + reader
    })

    critic = critic_chain.invoke({
        "report": writer
    })

    # SAVE RESULTS
    chat["results"] = {
        "writer": writer,
        "critic": critic
    }

    chat["messages"].append({"role": "assistant", "content": writer})
    chat["messages"].append({"role": "assistant", "content": critic})

    chat["title"] = topic[:30]

    st.session_state.running = False

    # SAVE TO DB (optional)
    save_history(st.session_state.user, topic, writer, critic)


# ── DISPLAY CHAT ─────────────────────────
if chat:
    for msg in chat["messages"]:
        if msg["role"] == "user":
            st.markdown(f"🧑 {msg['content']}")
        else:
            st.markdown(f"🤖 {msg['content']}")

else:
    st.info("👉 Create a new chat or select one from sidebar")