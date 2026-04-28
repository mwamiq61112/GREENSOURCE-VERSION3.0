import streamlit as st
import json
import os
from datetime import datetime
import urllib.parse
import requests as req

st.set_page_config(
    page_title="GreenSource",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS (PRESERVING ALL ORIGINAL STYLES + UPDATING TEXT COLOR) ────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

* { font-family: 'Outfit', sans-serif; }
h1,h2,h3 { font-family: 'Syne', sans-serif; color: #1a3d2b !important; }

.stApp {
    background: linear-gradient(160deg, #f0f7f4 0%, #e8f5ee 40%, #d8eedf 100%);
    background-attachment: fixed;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d2b1a 0%, #1a3d2b 60%, #2d6a4f 100%) !important;
}
[data-testid="stSidebar"] * { color: #d8eedf !important; }
[data-testid="stSidebar"] .stRadio > label { color: #95d5b2 !important; font-weight:600; }

.gs-card {
    background: rgba(255,255,255,0.9); backdrop-filter: blur(16px);
    border: 1px solid rgba(82,183,136,0.25); border-radius: 1.5rem;
    padding: 1.8rem; margin: 0.8rem 0;
    box-shadow: 0 4px 24px rgba(13,43,26,0.08);
}
.gs-card h3 { color: #1a3d2b !important; margin-bottom: 0.5rem; }
.gs-card p { color: #1a3d2b !important; font-weight: 500; } /* Dark Green/Black Text */

.google-btn {
    display: flex; align-items: center; justify-content: center; gap: 0.8rem;
    background: white; border: 2px solid #e0e0e0; border-radius: 0.8rem;
    padding: 0.8rem 2rem; cursor: pointer; font-size: 1rem; font-weight: 600;
    color: #3c4043; transition: all 0.2s; width: 100%;
}

@keyframes bounceLeft {
    0%, 20%, 50%, 80%, 100% {transform: translateX(0);}
    40% {transform: translateX(-15px);}
    60% {transform: translateX(-8px);}
}
.arrow-icon { font-size: 2rem; animation: bounceLeft 2s infinite; display: inline-block; }

#MainMenu,footer,header { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ── DATA HELPERS (YOUR ORIGINAL LOGIC) ────────────────────────────────────────
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
        data["users"][email] = {
            "name": name, "picture": picture,
            "joined": datetime.now().strftime("%B %Y"),
            "credits": 0, "waste_kg": 0.0, "co2_saved": 0.0, "scans": 0, "history": []
        }
        save_data(data)
    return data["users"][email]

def update_user(email, credits_add=0, waste_add=0, co2_add=0, history_item=None):
    data = load_data()
    if email in data["users"]:
        data["users"][email]["credits"] += credits_add
        if history_item:
            data["users"][email]["history"].insert(0, history_item)
        save_data(data)
        return data["users"][email]

def get_leaderboard():
    data = load_data()
    board = [{"name": u["name"], "credits": u["credits"], "picture": u.get("picture","")} for u in data["users"].values()]
    return sorted(board, key=lambda x: x["credits"], reverse=True)

# ── GOOGLE AUTH ──────────────────────────────────────────────────────────────
CLIENT_ID     = "218402500740-j807phgipdmvk8nirps5lsc60ohtjaf3.apps.googleusercontent.com"
CLIENT_SECRET = "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"

def get_redirect_uri():
    return st.secrets.get("redirect_uri", "https://greensource-v3-wamiq.streamlit.app/")

def get_google_auth_url():
    params = {"client_id": CLIENT_ID, "redirect_uri": get_redirect_uri(), "response_type": "code", "scope": "openid email profile"}
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)

def exchange_code_for_token(code):
    r = req.post("https://oauth2.googleapis.com/token", data={"code": code, "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "redirect_uri": get_redirect_uri(), "grant_type": "authorization_code"})
    return r.json()

def get_user_info(access_token):
    r = req.get("https://www.googleapis.com/oauth2/v3/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    return r.json()

# ── AUTH PAGE (FULL ORIGINAL UI) ──────────────────────────────────────────────
def show_auth():
    params = st.query_params
    if "code" in params:
        token_data = exchange_code_for_token(params["code"])
        if token_data and "access_token" in token_data:
            user_info = get_user_info(token_data["access_token"])
            if user_info and "email" in user_info:
                u = get_or_create_user(user_info["email"], user_info.get("name", ""), user_info.get("picture", ""))
                st.session_state.logged_in = True
                st.session_state.user_email = user_info["email"]
                st.session_state.user_data = u
                st.query_params.clear()
                st.rerun()

    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown('<div style="text-align:center; padding:3rem 0;"><h1>🌿 GreenSource</h1></div>', unsafe_allow_html=True)
        st.markdown('<div class="gs-card" style="text-align:center;"><h3>Welcome Back 👋</h3><p>Sign in with Google to continue</p>', unsafe_allow_html=True)
        st.markdown(f'<a href="{get_google_auth_url()}" target="_self"><div class="google-btn">Sign in with Google</div></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── MAIN APP (WITH DASHBOARD & SIDEBAR TOGGLE) ───────────────────────────────
def show_app():
    u = st.session_state.user_data
    email = st.session_state.user_email
    data = load_data()
    u = data["users"].get(email, u)

    with st.sidebar:
        st.markdown('### 🌿 GreenSource')
        page = st.radio("", ["🏠 Dashboard", "🔍 AI Waste Scanner", "🗺️ Eco-Navigator", "💚 Green Wallet", "📊 Impact Calculator", "🏆 Leaderboard"], label_visibility="collapsed")
        st.markdown("---")
        st.markdown(f"**{u['credits']} GC**")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    if "Dashboard" in page:
        # Toggle Button for Sidebar
        col_btn, col_txt = st.columns([1, 4])
        with col_btn:
            if st.button("⬅️ Open Menu"):
                st.info("Click the '>' arrow in the top-left to see all tools!")
        
        st.markdown(f"## Welcome back, {u['name']}! 🌿")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="gs-card"><h3>🔍 AI Scanner</h3><p>Scan waste items to earn rewards.</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="gs-card"><h3>🗺️ Navigator</h3><p>Find nearby collection points.</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="gs-card"><h3>💚 Green Wallet</h3><p>Redeem points for marketplace items.</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="gs-card"><h3>📊 Impact</h3><p>Check your total CO2 reduction stats.</p></div>', unsafe_allow_html=True)

    elif "🔍" in page:
        from pages_code import scanner
        scanner.show(email, update_user)
    elif "🗺️" in page:
        from pages_code import navigator
        navigator.show()
    elif "💚" in page:
        from pages_code import wallet
        wallet.show(email, load_data)
    elif "📊" in page:
        from pages_code import calculator
        calculator.show(email, update_user)
    elif "🏆" in page:
        from pages_code import leaderboard
        leaderboard.show(email, get_leaderboard)

# ── ENTRY POINT ──────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    show_app()
else:
    show_auth()
