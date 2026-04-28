import streamlit as st
import json
import os
from datetime import datetime
import urllib.parse
import requests as req

# 1. FORCE THE SIDEBAR TO BE OPEN ON START
st.set_page_config(
    page_title="GreenSource",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS (FIXED TO ENSURE SIDEBAR TOGGLE IS VISIBLE) ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

* { font-family: 'Outfit', sans-serif; }
h1,h2,h3 { font-family: 'Syne', sans-serif; color: #1a3d2b !important; }

.stApp {
    background: linear-gradient(160deg, #f0f7f4 0%, #e8f5ee 40%, #d8eedf 100%);
    background-attachment: fixed;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d2b1a 0%, #1a3d2b 60%, #2d6a4f 100%) !important;
}
[data-testid="stSidebar"] * { color: #d8eedf !important; }

/* Dashboard Cards with Dark Green Text */
.gs-card {
    background: rgba(255,255,255,0.9); backdrop-filter: blur(16px);
    border: 1px solid rgba(82,183,136,0.25); border-radius: 1.5rem;
    padding: 1.8rem; margin: 0.8rem 0;
    box-shadow: 0 4px 24px rgba(13,43,26,0.08);
}
.gs-card h3 { color: #1a3d2b !important; }
.gs-card p { color: #1a3d2b !important; font-weight: 600; }

/* Bouncing Arrow Animation */
@keyframes bounceLeft {
    0%, 20%, 50%, 80%, 100% {transform: translateX(0);}
    40% {transform: translateX(-15px);}
    60% {transform: translateX(-8px);}
}
.bouncing-arrow { font-size: 2.5rem; animation: bounceLeft 2s infinite; display: inline-block; }

/* CRITICAL: We removed 'header {visibility:hidden}' so you can see the sidebar button! */
footer { visibility:hidden; }
#MainMenu { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ── DATA HELPERS (STAYING CONSISTENT) ────────────────────────────────────────
DATA_FILE = "users_data.json"
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return {"users": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=2)

def get_or_create_user(email, name, picture):
    data = load_data()
    if email not in data["users"]:
        data["users"][email] = {"name": name, "picture": picture, "credits": 0, "history": []}
        save_data(data)
    return data["users"][email]

# ── AUTH PAGE ─────────────────────────────────────────────────────────────────
def show_auth():
    # [Your Google Sign-In logic here - same as before]
    st.markdown('<div style="text-align:center; padding-top:5rem;"><h1>🌿 GreenSource</h1><p>Please log in to continue</p></div>', unsafe_allow_html=True)
    # Placeholder for your actual auth button
    if st.button("Click to Simulate Login (Test Mode)"):
        st.session_state.logged_in = True
        st.session_state.user_email = "test@user.com"
        st.session_state.user_data = {"name": "Mohd Wamiq", "credits": 150}
        st.rerun()

# ── MAIN APP ──────────────────────────────────────────────────────────────────
def show_app():
    u = st.session_state.user_data
    email = st.session_state.user_email
    
    # NAVIGATION IN SIDEBAR
    with st.sidebar:
        st.markdown('### 🌿 GreenSource')
        page = st.radio("Menu", ["🏠 Dashboard", "🔍 AI Scanner", "🗺️ Navigator", "🏆 Leaderboard"], label_visibility="collapsed")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()

    if "Dashboard" in page:
        # VISUAL GUIDE FOR SIDEBAR
        col_arrow, col_text = st.columns([1, 5])
        with col_arrow:
            st.markdown('<div class="bouncing-arrow">⬅️</div>', unsafe_allow_html=True)
        with col_text:
            st.info("The tools menu is on the left. Use the arrow ( > ) at the top-left if it's hidden.")

        st.markdown(f"## Welcome back, {u['name']}! 🌿")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="gs-card"><h3>🔍 AI Scanner</h3><p>Identify waste and earn credits.</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="gs-card"><h3>🗺️ Navigator</h3><p>Find local recycling hubs.</p></div>', unsafe_allow_html=True)

    elif "🔍" in page:
        st.write("Scanner Page Content")

# ── ENTRY POINT ──────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    show_app()
else:
    show_auth()
