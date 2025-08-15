import streamlit as st
import requests
import logging
from modules.nav import SideBarLinks

# --- Configuration ---
st.set_page_config(layout='wide')
logger = logging.getLogger(__name__)
API_BASE_URL = "http://host.docker.internal:4000" # Replace with your API URL

# --- Page Setup ---
SideBarLinks()

# Ensure user is logged in
if 'username' not in st.session_state or 'profileID' not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

is_premium = st.session_state.get('isPremium', False)
username = st.session_state['username']
profile_id = st.session_state['profileID']

# --- Data Fetching Function ---
@st.cache_data
def get_user_games(profile_id):
    """Fetches all games associated with a user's profile."""
    try:
        # REPLACE WITH DB CALL
        return [
            {'gameID': 1, 'name': 'Valorant'},
            {'gameID': 2, 'name': 'Counter-Strike 2'}
        ]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching games: {e}")
        return []

# --- UI Display ---

# Title and welcome message
st.title(f"Welcome to Omni.gg, {username}.")
st.write('Your central hub for game analytics, player stats, and strategy tools.')
st.write('')

st.subheader("My Game Dashboards")
games_list = get_user_games(profile_id)

if games_list:
    for game in games_list:
        game_name = game['name']
        game_id = game['gameID']

        # When this button is clicked:
        if st.button(f"📊 View {game_name} Stats", key=f"game_{game_id}", use_container_width=True):
            # 1. Save the game info to the session state
            st.session_state['selected_game_id'] = game_id
            st.session_state['selected_game_name'] = game_name
            st.session_state['viewing_profile_name'] = username

            # 2. Switch to the stats page

            st.switch_page("pages/31_View_Stats.py")
else:
    st.info("You haven't added any games to your profile yet!")


st.divider()

# --- Other Navigation Buttons ---
st.subheader("Tools & Features")

# Premium section
if is_premium:
    if st.button('🔫 Weapon Analytics', use_container_width=True):
        st.switch_page('weapon_analytics')
    if st.button('🗺️ Map Insights', use_container_width=True):
        st.switch_page('map_insights')
else:
    if st.button('💎 Upgrade to Premium to Unlock Weapon & Map Stats', type='secondary', use_container_width=True):
        st.switch_page('premium_upgrade')

if st.button('🤝 Compare Players',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/32_Select_Players.py')



