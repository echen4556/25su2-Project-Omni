import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)
st.set_page_config(layout="wide")

if "profileID" not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

API_BASE_URL = "http://web-api:4000"

is_premium = st.session_state.get('isPremium', True)
username = st.session_state['username']
profile_id = st.session_state['profileID']

# --- Data Fetching Functions ---
@st.cache_data
def get_user_games(profile_id):
    """Fetches all games associated with a user's profile."""
    try:
        response_linked = requests.get(f"{API_BASE_URL}/games/profile/{profile_id}")
        response_linked.raise_for_status()
        linked_games = response_linked.json()
        return linked_games
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching games: {e}")
        return []

def unlink_game(profile_id, game_id):
    """Sends a DELETE request to unlink a game from the user's profile."""
    try:
        response = requests.delete(f"{API_BASE_URL}/games/profile/{profile_id}/{game_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error unlinking game: {e}")
        return None

# Show sidebar links for the current user
SideBarLinks()

# Title and welcome message
st.title(f"Welcome to Omni.gg, {st.session_state['username']}.")
st.write('')
st.write('Your central hub for game analytics, player stats, and strategy tools.')
st.write('')

st.subheader("My Game Dashboards")
games_list = get_user_games(profile_id)

if games_list:
    for game in games_list:
        game_name = game['name']
        game_id = game['gameID']

    
        if st.button(f"📊 View {game_name} Stats", key=f"game_{game_id}", use_container_width=True):
            # Store info for stats page
            st.session_state['selected_game_id'] = game_id
            st.session_state['selected_game_name'] = game_name
            st.session_state['viewing_profile_name'] = username
            st.switch_page("pages/31_View_Stats.py")
else:
    st.info("You haven't added any games to your profile yet!")

if st.button('🤝 Compare Players',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/32_Select_Players.py')

# --- Match History Navigation ---
if st.button("📜 View Match History", use_container_width=True, type="primary"):
    st.switch_page('pages/match_history.py')
