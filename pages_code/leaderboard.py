import streamlit as st

MEDALS = {1:"🥇",2:"🥈",3:"🥉"}

def show(email, get_leaderboard_fn):
    st.markdown("""
    <div class="nav-header">
        <h1>🏆 Leaderboard</h1>
        <p>See how you rank among GreenSource recyclers!</p>
    </div>
    """, unsafe_allow_html=True)

    board = get_leaderboard_fn()

    col1, col2 = st.columns([1.4, 1], gap="large")

    with col1:
        st.markdown('<div class="sec-title">Top Recyclers</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Ranked by Green Credits earned</div>', unsafe_allow_html=True)

        if not board:
            st.info("No users yet. Be the first to earn credits!")
        else:
            for i, user in enumerate(board[:20], 1):
                medal = MEDALS.get(i, f"#{i}")
                is_me = False  # Can't easily check without passing email deeper
                bg = "rgba(149,213,178,0.15)" if i <= 3 else "rgba(255,255,255,0.7)"
                border = "1px solid rgba(149,213,178,0.4)" if i <= 3 else "1px solid rgba(82,183,136,0.15)"

                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:1rem; padding:0.9rem 1.2rem; border-radius:1rem; margin-bottom:0.5rem; background:{bg}; border:{border}; transition:all 0.2s;">
                    <div style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:800; color:#2d6a4f; width:2.5rem; text-align:center;">{medal}</div>
                    <div style="flex:1;">
                        <div style="font-weight:600; color:#1a3d2b; font-size:0.95rem;">{user['name']}</div>
                        <div style="color:#52b788; font-size:0.78rem;">{user['waste_kg']:.1f} kg recycled</div>
                    </div>
                    <div style="font-family:'Syne',sans-serif; font-weight:800; color:#2d6a4f; font-size:1.1rem;">{user['credits']} GC</div>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sec-title">Your Ranking</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Your position on the board</div>', unsafe_allow_html=True)

        # Find current user rank
        my_rank = None
        my_data = None
        for i, u in enumerate(board, 1):
            # Match by checking session state name
            if u["name"] == st.session_state.get("user_data", {}).get("name",""):
                my_rank = i
                my_data = u
                break

        if my_rank:
            medal = MEDALS.get(my_rank, f"#{my_rank}")
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:1rem;">
                <div class="val">{medal}</div>
                <div class="lbl">Your Current Rank</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="gs-card">
                <div style="display:flex; justify-content:space-between; padding:0.5rem 0; border-bottom:1px solid #e8f5ee; color:#2d6a4f; font-size:0.9rem;">
                    <span>Green Credits</span><strong>{my_data['credits']} GC</strong>
                </div>
                <div style="display:flex; justify-content:space-between; padding:0.5rem 0; color:#2d6a4f; font-size:0.9rem;">
                    <span>Waste Recycled</span><strong>{my_data['waste_kg']:.1f} kg</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if my_rank > 1:
                gap = board[my_rank-2]["credits"] - my_data["credits"]
                st.markdown(f"""
                <div class="gs-info" style="margin-top:1rem;">
                    🎯 Only <strong>{gap} more credits</strong> to reach rank #{my_rank-1}!
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="gs-card" style="text-align:center; padding:2rem;">
                <div style="font-size:3rem;">🌱</div>
                <div style="font-family:'Syne',sans-serif; color:#1a3d2b; font-weight:700; margin-top:1rem;">Start Recycling!</div>
                <div style="color:#52b788; font-size:0.88rem; margin-top:0.5rem;">Scan waste or use the calculator to earn your first credits and appear on the leaderboard.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-card">
            <div class="val">{len(board)}</div>
            <div class="lbl">Total Recyclers</div>
        </div>
        """, unsafe_allow_html=True)
