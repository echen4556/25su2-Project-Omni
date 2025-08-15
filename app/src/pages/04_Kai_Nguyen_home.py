import logging
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)
st.set_page_config(layout="wide")

if "profileID" not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

is_premium = st.session_state.get('isPremium', True)
username = st.session_state['username']
profile_id = st.session_state['profileID']

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

if st.button('🤝 Compare Players',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/32_Select_Players.py')