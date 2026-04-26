import streamlit as st
import random
import time
from datetime import datetime

MATERIALS = {
    "Cardboard": {
        "score": 87, "credits": 12, "badge": "badge-green", "icon": "📦",
        "tip": "Flatten boxes, remove tape and staples before recycling.",
        "co2": 0.9, "waste": 0.5,
        "keywords": ["card", "box", "paper", "board", "carton"]
    },
    "Plastic": {
        "score": 72, "credits": 8, "badge": "badge-blue", "icon": "🧴",
        "tip": "Rinse containers. Check resin code (1-7) on the bottom.",
        "co2": 1.5, "waste": 0.3,
        "keywords": ["plastic", "bottle", "bag", "pet", "container"]
    },
    "E-Waste": {
        "score": 94, "credits": 25, "badge": "badge-orange", "icon": "💻",
        "tip": "Never landfill electronics. Take to certified e-waste centers.",
        "co2": 3.2, "waste": 0.8,
        "keywords": ["phone", "laptop", "elec", "wire", "battery", "circuit"]
    },
    "Glass": {
        "score": 91, "credits": 10, "badge": "badge-green", "icon": "🫙",
        "tip": "Glass is 100% recyclable. Rinse before dropping off.",
        "co2": 0.3, "waste": 0.5,
        "keywords": ["glass", "bottle", "jar", "window"]
    },
    "Metal": {
        "score": 96, "credits": 18, "badge": "badge-gold", "icon": "🥫",
        "tip": "Aluminium recycling saves 95% energy vs new production!",
        "co2": 9.0, "waste": 0.4,
        "keywords": ["metal", "alumin", "can", "steel", "iron", "copper"]
    },
}

def classify(filename):
    fn = filename.lower()
    for mat, info in MATERIALS.items():
        if any(k in fn for k in info["keywords"]):
            return mat, info
    return random.choice(list(MATERIALS.items()))

def show(email, update_user_fn):
    st.markdown("""
    <div class="nav-header">
        <h1>🔬 AI Waste Scanner</h1>
        <p>Upload an image — our AI identifies your waste and guides recycling.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1], gap="large")

    with col1:
        st.markdown('<div class="sec-title">Upload Waste Image</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">JPG or PNG · Best results with clear, single-item photos</div>', unsafe_allow_html=True)

        uploaded = st.file_uploader("", type=["jpg","jpeg","png"], label_visibility="collapsed")

        if uploaded is None:
            st.markdown("""
            <div style="border:2px dashed #52b788; border-radius:1.5rem; padding:3rem; text-align:center; background:rgba(82,183,136,0.06);">
                <div style="font-size:3.5rem;">📸</div>
                <div style="font-size:1.1rem; font-weight:600; color:#2d6a4f; margin-top:0.5rem;">Drop your image here</div>
                <div style="color:#52b788; font-size:0.85rem; margin-top:0.3rem;">Supports JPG and PNG formats</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="gs-card" style="margin-top:1rem;">
                <div style="font-weight:700; color:#1a3d2b; margin-bottom:0.8rem; font-family:'Syne',sans-serif;">💡 Tips for best results</div>
                <div style="color:#2d6a4f; font-size:0.9rem; line-height:1.8;">
                    ✅ Use natural lighting<br>
                    ✅ Place item on a clean surface<br>
                    ✅ Capture the full item<br>
                    ✅ Avoid blurry photos
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.image(uploaded, use_container_width=True)
            prog = st.progress(0)
            status = st.empty()
            steps = ["🔍 Detecting edges...", "🎨 Analyzing texture...", "🧠 Classifying material...", "✅ Done!"]
            for i, s in enumerate(steps):
                status.markdown(f'<div class="gs-info">{s}</div>', unsafe_allow_html=True)
                prog.progress((i+1)*25)
                time.sleep(0.4)
            prog.empty(); status.empty()

            mat, info = classify(uploaded.name)

            st.markdown(f"""
            <div class="gs-success">
                ✅ <strong>Analysis Complete:</strong> Material identified as
                <strong>{info['icon']} {mat}</strong> based on texture and shape.
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="gs-card" style="margin-top:1rem;">', unsafe_allow_html=True)
            st.markdown(f'**{info["icon"]} Material: {mat}** &nbsp; <span class="gs-badge {info["badge"]}">{mat}</span>', unsafe_allow_html=True)
            st.markdown(f"<br>💡 **Tip:** {info['tip']}", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("✅ Confirm & Earn Credits", use_container_width=True):
                history_item = {
                    "action": f"{info['icon']} {mat} scanned",
                    "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                    "credits": info["credits"]
                }
                update_user_fn(email,
                    credits_add=info["credits"],
                    waste_add=info["waste"],
                    co2_add=info["co2"],
                    history_item=history_item
                )
                st.success(f"🎉 +{info['credits']} Green Credits added to your wallet!")
                st.balloons()

    with col2:
        if uploaded:
            mat, info = classify(uploaded.name)
            score = info["score"]

            st.markdown('<div class="sec-title">Scan Results</div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-sub">Environmental assessment</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="gs-card" style="text-align:center;">
                <div style="font-size:0.8rem; color:#52b788; text-transform:uppercase; letter-spacing:1px; font-weight:600; margin-bottom:1rem;">
                    Recyclability Score
                </div>
                <div style="
                    width:150px; height:150px; border-radius:50%;
                    background: conic-gradient(#52b788 {score*3.6}deg, #e8f5ee 0deg);
                    display:flex; align-items:center; justify-content:center;
                    margin: 0 auto; position:relative;
                    box-shadow: 0 4px 24px rgba(82,183,136,0.4);
                ">
                    <div style="width:112px; height:112px; border-radius:50%; background:white; position:absolute;"></div>
                    <div style="position:relative; z-index:1; font-family:'Syne',sans-serif; font-size:2.4rem; font-weight:800; color:#1a3d2b;">{score}</div>
                </div>
                <div style="color:#52b788; font-size:0.85rem; margin-top:0.8rem;">out of 100</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="metric-card" style="margin-top:1rem;">
                <div class="val">+{info['credits']}</div>
                <div class="lbl">🪙 Green Credits to Earn</div>
                <div style="color:#b7e4c7; font-size:0.8rem; margin-top:0.4rem;">Click confirm below to claim</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="gs-card" style="margin-top:1rem;">
                <div style="font-weight:700; color:#1a3d2b; margin-bottom:0.8rem;">🌍 If recycled correctly:</div>
                <div style="display:flex; flex-direction:column; gap:0.5rem;">
                    <div style="display:flex; justify-content:space-between; color:#2d6a4f; font-size:0.9rem; padding:0.4rem 0; border-bottom:1px solid #e8f5ee;">
                        <span>CO₂ saved</span><strong>{info['co2']} kg</strong>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#2d6a4f; font-size:0.9rem; padding:0.4rem 0;">
                        <span>Waste diverted</span><strong>{info['waste']} kg</strong>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="gs-card" style="text-align:center; padding:3rem 2rem;">
                <div style="font-size:4rem;">🌿</div>
                <div style="font-family:'Syne',sans-serif; font-size:1.2rem; font-weight:700; color:#1a3d2b; margin:1rem 0 0.5rem;">
                    Ready to Scan
                </div>
                <div style="color:#52b788; font-size:0.88rem; line-height:1.6;">
                    Upload a waste image to get<br>your recyclability score.
                </div>
            </div>
            """, unsafe_allow_html=True)
