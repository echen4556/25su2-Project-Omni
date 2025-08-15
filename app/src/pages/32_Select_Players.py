import streamlit as st
import requests

API_BASE_URL = 'http://api:4000' 

# -------------------------------
# Helper functions
# -------------------------------
def get_user_games(profile_id):
    try:
        response = requests.get(f"{API_BASE_URL}/profiles/{profile_id}/games")
        response.raise_for_status()
        return response.json()  # List of games
    except requests.exceptions.RequestException:
        st.error("Failed to fetch games from backend API.")
        return []

def get_all_players():
    try:
        response = requests.get(f"{API_BASE_URL}/profiles")
        response.raise_for_status()
        return response.json()  # List of players with profileID, username, isPremium
    except requests.exceptions.RequestException:
        st.error("Failed to fetch players from backend API.")
        return []

# -------------------------------
# Page layout
# -------------------------------
st.title("Select Players and Game to Compare")
st.write("Choose two players and a game to compare stats.")

# -------------------------------
# Fetch data from API
# -------------------------------
# Assuming a logged-in user with profile_id in session_state
if 'profile_id' not in st.session_state:
    st.error("You must be logged in to view this page.")
    st.stop()

profile_id = st.session_state['profile_id']

games = get_user_games(profile_id)
players = get_all_players()

if not games or not players:
    st.stop()

game_options = {game['game_name']: game['game_id'] for game in games}
player_options = {player['username']: (player['profileID'], player['isPremium']) for player in players}

# -------------------------------
# User selections
# -------------------------------
selected_game_name = st.selectbox("Select Game", list(game_options.keys()))
selected_game_id = game_options[selected_game_name]

player1_name = st.selectbox("Select Player 1", list(player_options.keys()))
player2_name = st.selectbox("Select Player 2", list(player_options.keys()))

player1_id, player1_premium = player_options[player1_name]
player2_id, player2_premium = player_options[player2_name]

# -------------------------------
# Compare button
# -------------------------------
if st.button("Compare Players"):
    if player1_name == player2_name:
        st.warning("Please select two different players.")
    else:
        # Save selections in session state
        st.session_state['compare'] = {
            'player1_id': player1_id,
            'player2_id': player2_id,
            'player1_name': player1_name,
            'player2_name': player2_name,
            'game_id': selected_game_id,
            'game_name': selected_game_name,
            'show_maps_weapons': player1_premium and player2_premium
        }
        # Switch to Page 33
        st.switch_page("33_Compare_Players")
