import streamlit as st
from datetime import datetime

FACTORS = {
    "Paper / Cardboard": {"trees":0.017,"water":20,"co2":0.9,"energy":17,"credits":5,"icon":"📄","oil":0,"ore":0,"sand":0},
    "Plastic":           {"oil":0.72,"water":22,"co2":1.5,"energy":5.8,"credits":4,"icon":"🧴","trees":0,"ore":0,"sand":0},
    "Glass":             {"sand":1.2,"water":1.5,"co2":0.3,"energy":0.67,"credits":3,"icon":"🫙","trees":0,"oil":0,"ore":0},
    "Aluminium / Metal": {"ore":4.0,"water":40,"co2":9.0,"energy":14,"credits":8,"icon":"🔩","trees":0,"oil":0,"sand":0},
}

def show(email, update_user_fn):
    st.markdown("""
    <div class="nav-header">
        <h1>📊 Impact Calculator</h1>
        <p>Discover the real environmental difference your recycling makes.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.markdown('<div class="sec-title">Configure Your Recycling</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Enter material details to calculate impact</div>', unsafe_allow_html=True)
        st.markdown('<div class="gs-card">', unsafe_allow_html=True)

        material = st.selectbox("🗂️ Material Type", list(FACTORS.keys()))
        weight   = st.number_input("⚖️ Weight (kg)", min_value=0.1, max_value=1000.0, value=5.0, step=0.5)
        freq     = st.selectbox("📅 Frequency", ["One-time","Weekly","Monthly","Yearly"])

        mult = {"One-time":1,"Weekly":52,"Monthly":12,"Yearly":1}[freq]
        annual = weight * mult

        st.markdown(f"""
        <div class="gs-info" style="margin-top:1rem;">
            📦 Annual equivalent: <strong>{annual:.1f} kg</strong>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("⚡ Calculate & Log Impact", use_container_width=True):
            st.session_state["calc_done"] = True
            st.session_state["calc_mat"]  = material
            st.session_state["calc_wt"]   = weight
            st.session_state["calc_freq"] = freq

        with st.expander("ℹ️ Data sources"):
            st.markdown("""
            - **Paper:** EPA WARM model
            - **Plastic:** PlasticsEurope Environmental Profiles
            - **Glass:** British Glass sustainability data
            - **Metal:** International Aluminium Institute
            """)

    with col2:
        st.markdown('<div class="sec-title">Your Environmental Impact</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Real numbers from verified research</div>', unsafe_allow_html=True)

        mat  = st.session_state.get("calc_mat", material)
        w    = st.session_state.get("calc_wt", weight)
        freq2= st.session_state.get("calc_freq", freq)
        f    = FACTORS[mat]

        co2    = w * f["co2"]
        energy = w * f["energy"]
        water  = w * f["water"]
        credits= int(w * f["credits"])

        # Specific extras
        if "Paper" in mat:
            trees = w * f["trees"]
            headline = f"Recycling {w:.1f}kg of paper saves {trees:.2f} trees and {water:.0f}L of water."
            extras = [("🌳",f"{trees:.2f} trees preserved"),("🌍",f"{co2:.2f} kg CO₂ avoided"),("⚡",f"{energy:.1f} kWh saved"),("🌊",f"{water:.0f}L water conserved")]
            fact = "It takes 24 trees to make 1 tonne of paper!"
        elif "Plastic" in mat:
            oil = w * f["oil"]
            headline = f"Recycling {w:.1f}kg of plastic saves {oil:.2f}L of crude oil."
            extras = [("🛢️",f"{oil:.2f}L crude oil saved"),("🌍",f"{co2:.2f} kg CO₂ avoided"),("⚡",f"{energy:.1f} kWh saved"),("🌊",f"{water:.0f}L water saved")]
            fact = "Plastic takes 500 years to decompose in landfill!"
        elif "Glass" in mat:
            sand = w * f["sand"]
            headline = f"Recycling {w:.1f}kg of glass conserves {sand:.2f}kg of raw sand."
            extras = [("🏖️",f"{sand:.2f}kg sand preserved"),("🌍",f"{co2:.2f} kg CO₂ avoided"),("⚡",f"{energy:.2f} kWh saved"),("🌊",f"{water:.2f}L water saved")]
            fact = "Glass is 100% recyclable — forever!"
        else:
            ore = w * f["ore"]
            headline = f"Recycling {w:.1f}kg of metal saves {ore:.2f}kg of bauxite ore."
            extras = [("⛏️",f"{ore:.2f}kg ore saved"),("🌍",f"{co2:.2f} kg CO₂ avoided"),("⚡",f"{energy:.1f} kWh saved (95% less!)"),("🌊",f"{water:.0f}L water saved")]
            fact = "Recycling aluminium uses 95% less energy than new production!"

        st.markdown(f"""
        <div class="impact-box">
            <h3>🎯 Impact Summary</h3>
            <p>{headline}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        for icon, text in extras:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:0.8rem; background:rgba(255,255,255,0.8); border:1px solid rgba(82,183,136,0.2); border-radius:0.8rem; padding:0.8rem 1rem; margin-bottom:0.5rem;">
                <span style="font-size:1.4rem;">{icon}</span>
                <span style="color:#1a3d2b; font-size:0.9rem;">{text}</span>
            </div>
            """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="val">+{credits}</div>
                <div class="lbl">Credits to Earn</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="gs-card" style="height:100%;">
                <div style="font-size:0.78rem; text-transform:uppercase; color:#52b788; font-weight:600; margin-bottom:0.5rem;">💡 Did you know?</div>
                <div style="color:#1a3d2b; font-size:0.85rem; line-height:1.5;">{fact}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.get("calc_done"):
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✅ Log This Recycling Action", use_container_width=True):
                history_item = {
                    "action": f"{f['icon']} {mat.split('/')[0].strip()} — {w:.1f}kg",
                    "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                    "credits": credits
                }
                update_user_fn(email, credits_add=credits, waste_add=w, co2_add=co2, history_item=history_item)
                st.success(f"✅ Logged! +{credits} Green Credits added!")
                st.session_state["calc_done"] = False
