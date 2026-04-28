import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="GreenSource",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS (COMPLETELY UNTOUCHED) ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

* { font-family: 'Outfit', sans-serif; }
h1,h2,h3 { font-family: 'Syne', sans-serif; }

.stApp {
    background: linear-gradient(160deg, #f0f7f4 0%, #e8f5ee 40%, #d8eedf 100%);
    background-attachment: fixed;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d2b1a 0%, #1a3d2b 60%, #2d6a4f 100%) !important;
}
[data-testid="stSidebar"] * { color: #d8eedf !important; }
[data-testid="stSidebar"] .stRadio > label { color: #95d5b2 !important; font-weight:600; }

.nav-header {
    background: linear-gradient(135deg, #0d2b1a, #1a3d2b, #2d6a4f);
    padding: 2rem 2.5rem 1.8rem; border-radius: 0 0 2.5rem 2.5rem;
    margin: -1rem -1rem 2rem -1rem;
    box-shadow: 0 8px 40px rgba(13,43,26,0.25);
}
.nav-header h1 { font-size:2.6rem; font-weight:800; color:#95d5b2; margin:0; letter-spacing:-1px; }
.nav-header p  { color:#b7e4c7; margin:0.3rem 0 0; font-size:1rem; }

.gs-card {
    background: rgba(255,255,255,0.9); backdrop-filter: blur(16px);
    border: 1px solid rgba(82,183,136,0.25); border-radius: 1.5rem;
    padding: 1.8rem; margin: 0.8rem 0;
    box-shadow: 0 4px 24px rgba(13,43,26,0.08);
    transition: all 0.25s ease;
}
.gs-card:hover { transform: translateY(-3px); box-shadow: 0 10px 40px rgba(13,43,26,0.14); }

.metric-card {
    background: linear-gradient(135deg, #1a3d2b, #2d6a4f);
    border-radius: 1.5rem; padding: 1.5rem; text-align: center;
    box-shadow: 0 6px 24px rgba(13,43,26,0.3);
}
.metric-card .val { font-family:'Syne',sans-serif; font-size:2.4rem; font-weight:800; color:#95d5b2; line-height:1; }
.metric-card .lbl { font-size:0.8rem; color:#b7e4c7; margin-top:0.4rem; text-transform:uppercase; letter-spacing:1px; }

.gs-badge { display:inline-block; padding:0.25rem 0.8rem; border-radius:999px; font-size:0.78rem; font-weight:600; }
.badge-green  { background:#d8eedf; color:#1a5c33; border:1px solid #95d5b2; }
.badge-blue   { background:#d0e8f7; color:#1a4a6e; border:1px solid #7ec8f0; }
.badge-orange { background:#fde8d0; color:#7a3a00; border:1px solid #f0b07e; }
.badge-gold   { background:#fff3cd; color:#856404; border:1px solid #ffc107; }

.stButton > button {
    background: linear-gradient(135deg, #2d6a4f, #52b788) !important;
    color: white !important; border: none !important;
    border-radius: 0.8rem !important; padding: 0.65rem 2rem !important;
    font-family: 'Outfit', sans-serif !important; font-weight: 600 !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 15px rgba(45,106,79,0.35) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1a3d2b, #2d6a4f) !important;
    transform: translateY(-2px) !important;
}

.google-btn {
    display: flex; align-items: center; justify-content: center; gap: 0.8rem;
    background: white; border: 2px solid #e0e0e0; border-radius: 0.8rem;
    padding: 0.8rem 2rem; cursor: pointer; font-size: 1rem; font-weight: 600;
    color: #3c4043; transition: all 0.2s; width: 100%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.google-btn:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.15); border-color: #4285F4; }

/* NEW ARROW ANIMATION */
@keyframes bounceLeft {
    0%, 20%, 50%, 80%, 100% {transform: translateX(0);}
    40% {transform: translateX(-15px);}
    60% {transform: translateX(-8px);}
}
.arrow-box { font-size: 2rem; animation: bounceLeft 2s infinite; }

#MainMenu,footer,header { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ── Data helpers (UNTOUCHED) ──────────────────────────────────────────────────
DATA_FILE = "users_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"users": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_or_create_user(email, name, picture):
    data = load_data()
    if email not in data["users"]:
        data["users"][email] = {
            "name": name, "picture": picture,
            "joined": datetime.now().strftime("%B %Y"),
            "credits": 0, "waste_kg": 0.0,
            "co2_saved": 0.0, "scans": 0, "history": []
        }
        save_data(data)
    else:
        data["users"][email]["name"] = name
        data["users"][email]["picture"] = picture
        save_data(data)
    return data["users"][email]

def update_user(email, credits_add=0, waste_add=0, co2_add=0, history_item=None):
    data = load_data()
    if email in data["users"]:
        data["users"][email]["credits"]  += credits_add
        data["users"][email]["waste_kg"] += waste_add
        data["users"][email]["co2_saved"]+= co2_add
        if history_item:
            data["users"][email]["scans"] += 1
            data["users"][email]["history"].insert(0, history_item)
            data["users"][email]["history"] = data["users"][email]["history"][:20]
        save_data(data)
        return data["users"][email]

def get_leaderboard():
    data = load_data()
    board = [{"name": u["name"], "credits": u["credits"],
              "waste_kg": u["waste_kg"], "picture": u.get("picture","")}
             for u in data["users"].values()]
    return sorted(board, key=lambda x: x["credits"], reverse=True)

# ── Google OAuth (UNTOUCHED) ──────────────────────────────────────────────────
import urllib.parse
import requests as req

CLIENT_ID     = "218402500740-j807phgipdmvk8nirps5lsc60ohtjaf3.apps.googleusercontent.com"
CLIENT_SECRET = "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"

def get_redirect_uri():
    try:
        base = st.secrets.get("redirect_uri", "http://localhost:8501")
        return base
    except:
        return "http://localhost:8501"

def get_google_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": get_redirect_uri(),
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account"
    }
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)

def exchange_code_for_token(code):
    try:
        r = req.post("https://oauth2.googleapis.com/token", data={
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": get_redirect_uri(),
            "grant_type": "authorization_code"
        })
        return r.json()
    except:
        return None

def get_user_info(access_token):
    try:
        r = req.get("https://www.googleapis.com/oauth2/v3/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"})
        return r.json()
    except:
        return None

# ── Auth page (UNTOUCHED) ─────────────────────────────────────────────────────
def show_auth():
    params = st.query_params
    if "code" in params:
        with st.spinner("🔐 Signing you in with Google..."):
            token_data = exchange_code_for_token(params["code"])
            if token_data and "access_token" in token_data:
                user_info = get_user_info(token_data["access_token"])
                if user_info and "email" in user_info:
                    email   = user_info["email"]
                    name    = user_info.get("name", email)
                    picture = user_info.get("picture", "")
                    u = get_or_create_user(email, name, picture)
                    st.session_state.logged_in  = True
                    st.session_state.user_email = email
                    st.session_state.user_data  = u
                    st.query_params.clear()
                    st.rerun()

    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:3rem 0 2rem;">
            <div style="font-family:'Syne',sans-serif; font-size:4rem; font-weight:800; color:#1a3d2b; line-height:1;">🌿</div>
            <div style="font-family:'Syne',sans-serif; font-size:2.8rem; font-weight:800; color:#1a3d2b; margin-top:0.5rem;">GreenSource</div>
            <div style="color:#52b788; font-size:1.1rem; margin-top:0.3rem; font-weight:500;">Recycle. Earn. Impact.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="gs-card" style="text-align:center; padding:2.5rem;">', unsafe_allow_html=True)
        auth_url = get_google_auth_url()
        st.markdown(f"""
        <a href="{auth_url}" style="text-decoration:none;">
            <div class="google-btn">
                <svg width="20" height="20" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                <span style="font-size:1rem; font-weight:600; color:#3c4043;">Sign in with Google</span>
            </div>
        </a>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ── Main app (INTEGRATED DASHBOARD) ──────────────────────────────────────────
def show_app():
    u     = st.session_state.user_data
    email = st.session_state.user_email
    data   = load_data()
    u      = data["users"].get(email, u)
    name    = u.get("name","User")
    picture = u.get("picture","")
    credits = u.get("credits", 0)

    with st.sidebar:
        st.markdown('<div style="font-family:Syne,sans-serif; font-size:1.8rem; font-weight:800; color:#95d5b2; padding:1rem 0 0.3rem;">🌿 GreenSource</div>', unsafe_allow_html=True)
        if picture:
            st.markdown(f'<img src="{picture}" style="width:48px; height:48px; border-radius:50%; border:2px solid #52b788; margin-bottom:0.3rem;">', unsafe_allow_html=True)
        
        # NAVIGATION LIST
        page = st.radio("", [
            "🏠 Dashboard", 
            "🏠 AI Waste Scanner",
            "🗺️ Eco-Navigator",
            "💚 Green Wallet",
            "📊 Impact Calculator",
            "🏆 Leaderboard"
        ], label_visibility="collapsed")

        st.markdown("---")
        st.markdown(f'<div style="font-family:Syne,sans-serif; font-size:2rem; color:#b7e4c7; font-weight:800;">{credits} GC</div>', unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in  = False
            st.rerun()

    # --- ROUTING ---
    if "Dashboard" in page:
        # Guidance Arrow
        st.markdown(f'''
            <div style="display:flex; align-items:center; gap:20px; margin-bottom:2rem; background:rgba(45,106,79,0.1); padding:1rem; border-radius:1rem; border-left:5px solid #2d6a4f;">
                <div class="arrow-box">⬅️</div>
                <div style="font-weight:600; color:#1a3d2b;">Welcome! Click the sidebar menu to start using your tools.</div>
            </div>
            <h2>Welcome back, {name}! 🌿</h2>
        ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="gs-card"><h3>🔍 Scanner</h3><p>Identify waste and earn credits.</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="gs-card"><h3>🗺️ Navigator</h3><p>Find nearby recycling centers.</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="gs-card"><h3>💚 Wallet</h3><p>Redeem your Green Credits.</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="gs-card"><h3>🏆 Leaderboard</h3><p>See the top recyclers.</p></div>', unsafe_allow_html=True)

    elif "🏠" in page:
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

# ── Entry point ───────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in  = False

if st.session_state.logged_in:
    show_app()
else:
    show_auth()
