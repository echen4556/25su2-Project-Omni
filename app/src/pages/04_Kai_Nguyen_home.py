import logging
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)
st.set_page_config(layout="wide")

ROUTES = {
    "view_stats_page": "pages/31_View_Stats.py",
    "compare_players_page": "pages/33_Compare_Players.py",
    "weapon_analytics_page": "pages/Weapon_Analytics.py",   # <-- adjust if different
    "map_insights_page": "pages/map_insights.py",           # <-- adjust if different
}

if "username" not in st.session_state or "profileID" not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

username = st.session_state["username"]
profile_id = st.session_state["profileID"]
is_premium = st.session_state.get("isPremium", False)


@st.cache_data(ttl=300)
def get_user_games(profile_id: int):
    """
    Return games linked to this profile.
    Replace the mock with a real DB call (or API) later.
    """

    
    return [
        {"gameID": 1, "name": "Valorant"},
        {"gameID": 2, "name": "Counter-Strike 2"},
    ]


SideBarLinks()

st.title(f"Welcome to Omni.gg, {username}.")
st.write("")
st.write("Your central hub for game analytics, player stats, and strategy tools.")
st.write("")

# ---- Dynamic: dashboards per game ----
st.subheader("My Game Dashboards")
games_list = get_user_games(profile_id)

if games_list:
    for game in games_list:
        game_name = game["name"]
        game_id = game["gameID"]

        if st.button(f"📊 View {game_name} Stats", key=f"game_{game_id}", use_container_width=True):
            # Stash context for the stats page
            st.session_state["selected_game_id"] = game_id
            st.session_state["selected_game_name"] = game_name
            st.session_state["viewing_profile_id"] = profile_id
            st.session_state["viewing_profile_name"] = username

            st.switch_page(ROUTES["view_stats_page"])
else:
    st.info("You haven't added any games to your profile yet!")

st.divider()

# ---- Static feature shortcuts ----
col1, col2 = st.columns(2, gap="large")

with col1:
    if st.button("🔫 Weapon Analytics", type="primary", use_container_width=True):
        st.switch_page(ROUTES["weapon_analytics_page"])

with col2:
    if st.button("🗺️ Map Insights", type="primary", use_container_width=True):
        st.switch_page(ROUTES["map_insights_page"])

st.write("")

if st.button("🤝 Compare Players", type="primary", use_container_width=True):
    st.switch_page(ROUTES["compare_players_page"])


if is_premium:
    st.caption("⭐ Premium account active")
