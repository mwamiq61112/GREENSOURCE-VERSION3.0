import streamlit as st

DISCOUNT_CODES = [
    {"brand":"EcoWear 🧥","code":"GREEN20","desc":"20% off sustainable clothing","expiry":"31 May 2026","min_credits":50},
    {"brand":"SolarBox 🌞","code":"SOLAR15","desc":"₹150 off solar accessories","expiry":"30 Jun 2026","min_credits":80},
    {"brand":"BambooHome 🏠","code":"BAMB10","desc":"10% off bamboo furniture","expiry":"15 Jul 2026","min_credits":100},
    {"brand":"PureEats 🥗","code":"ORGANIC25","desc":"25% off organic food basket","expiry":"31 May 2026","min_credits":60},
    {"brand":"CycloGear 🚲","code":"CYCLE30","desc":"₹300 off cycling gear","expiry":"30 Jun 2026","min_credits":120},
]

def show(email, load_data_fn):
    data = load_data_fn()
    u = data["users"].get(email, {})
    name = u.get("name","User")
    credits = u.get("credits", 0)
    waste   = u.get("waste_kg", 0.0)
    co2     = u.get("co2_saved", 0.0)
    scans   = u.get("scans", 0)
    history = u.get("history", [])
    joined  = u.get("joined", "2025")

    # Rank logic
    if credits >= 200: rank, rank_icon = "Eco Champion", "🏆"
    elif credits >= 100: rank, rank_icon = "Eco Warrior", "🌿"
    elif credits >= 50:  rank, rank_icon = "Green Starter", "🌱"
    else:                rank, rank_icon = "Newcomer", "🌾"

    st.markdown("""
    <div class="nav-header">
        <h1>💚 Green Wallet</h1>
        <p>Your personal environmental impact dashboard.</p>
    </div>
    """, unsafe_allow_html=True)

    # Profile
    st.markdown(f"""
    <div class="gs-card" style="display:flex; align-items:center; gap:1.5rem; flex-wrap:wrap;">
        <div style="
            width:75px; height:75px; border-radius:50%;
            background:linear-gradient(135deg,#95d5b2,#52b788);
            display:flex; align-items:center; justify-content:center;
            font-size:2.2rem; flex-shrink:0; box-shadow:0 4px 16px rgba(82,183,136,0.4);
        ">🌱</div>
        <div style="flex:1;">
            <div style="font-family:'Syne',sans-serif; font-size:1.6rem; font-weight:800; color:#1a3d2b;">{name}</div>
            <div style="color:#52b788; font-size:0.88rem; margin-top:0.1rem;">Member since {joined} · Delhi, India</div>
            <div style="margin-top:0.6rem; display:flex; gap:0.5rem; flex-wrap:wrap;">
                <span class="gs-badge badge-green">{rank_icon} {rank}</span>
                <span class="gs-badge badge-blue">🔬 {scans} Scans</span>
            </div>
        </div>
        <div style="text-align:center; background:linear-gradient(135deg,#1a3d2b,#2d6a4f); padding:1rem 1.5rem; border-radius:1rem;">
            <div style="font-family:'Syne',sans-serif; font-size:2.2rem; font-weight:800; color:#95d5b2;">{credits}</div>
            <div style="color:#b7e4c7; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.5px;">Green Credits</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Metrics
    st.markdown('<div class="sec-title">📊 Impact Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Your real-time environmental contribution</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("♻️ Waste Recycled", f"{waste:.1f} kg")
    with m2: st.metric("🌿 CO₂ Saved", f"{co2:.1f} kg")
    with m3: st.metric("🪙 Green Credits", f"{credits} GC")
    with m4: st.metric("🔬 Total Scans", f"{scans}")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.1, 1], gap="large")

    with col1:
        st.markdown('<div class="sec-title">📋 Activity History</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Your recent recycling actions</div>', unsafe_allow_html=True)
        st.markdown('<div class="gs-card">', unsafe_allow_html=True)
        if history:
            for act in history[:10]:
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:1rem; padding:0.7rem 0; border-bottom:1px solid #e8f5ee;">
                    <div style="flex:1;">
                        <div style="font-weight:600; color:#1a3d2b; font-size:0.9rem;">{act.get('action','Action')}</div>
                        <div style="color:#52b788; font-size:0.78rem;">{act.get('date','')}</div>
                    </div>
                    <div style="font-family:'Syne',sans-serif; font-weight:700; color:#2d6a4f;">+{act.get('credits',0)} GC</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#52b788; text-align:center; padding:2rem; font-size:0.9rem;">No activity yet. Start by scanning waste! 🔬</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sec-title">🎁 Redeem Rewards</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Use your credits for eco-friendly discounts</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#95d5b2,#52b788); border-radius:1.2rem; padding:1.2rem 1.5rem; margin-bottom:1rem; display:flex; align-items:center; justify-content:space-between;">
            <div>
                <div style="font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800; color:#1a3d2b;">{credits} GC</div>
                <div style="color:#1a5c33; font-size:0.85rem;">Available to redeem</div>
            </div>
            <div style="font-size:3rem;">🪙</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎟️ Reveal My Discount Codes", use_container_width=True):
            st.session_state["show_codes"] = True

        if st.session_state.get("show_codes"):
            for d in DISCOUNT_CODES:
                unlocked = credits >= d["min_credits"]
                if unlocked:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#1a3d2b,#2d6a4f); border-radius:0.8rem; padding:1rem 1.2rem; margin-bottom:0.5rem; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="color:#e8f5ee; font-weight:600; font-size:0.88rem;">{d['brand']}</div>
                            <div style="color:#b7e4c7; font-size:0.75rem;">{d['desc']}</div>
                            <div style="color:#52b788; font-size:0.72rem;">Expires {d['expiry']}</div>
                        </div>
                        <div style="font-family:'Syne',monospace; font-weight:800; color:#95d5b2; font-size:0.95rem; background:rgba(149,213,178,0.1); padding:0.3rem 0.7rem; border-radius:0.4rem; border:1px solid rgba(149,213,178,0.3);">{d['code']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    needed = d["min_credits"] - credits
                    st.markdown(f"""
                    <div style="background:rgba(200,200,200,0.2); border-radius:0.8rem; padding:1rem 1.2rem; margin-bottom:0.5rem; display:flex; justify-content:space-between; align-items:center; opacity:0.7;">
                        <div>
                            <div style="color:#555; font-weight:600; font-size:0.88rem;">{d['brand']}</div>
                            <div style="color:#888; font-size:0.75rem;">{d['desc']}</div>
                        </div>
                        <div style="color:#888; font-size:0.8rem;">🔒 Need {needed} more GC</div>
                    </div>
                    """, unsafe_allow_html=True)
