import streamlit as st
import requests

API_BASE_URL = 'http://api:4000'  

# --- Ensure user is logged in ---
if 'username' not in st.session_state:
    st.error("You must be logged in to view this page.")
    st.stop()

username = st.session_state['username']
is_premium = st.session_state.get('isPremium', False)

# --- Helper functions ---
def get_all_players():
    try:
        response = requests.get(f"{API_BASE_URL}/profiles")
        response.raise_for_status()
        return response.json()  # List of players: username, isPremium
    except requests.exceptions.RequestException:
        st.error("Failed to fetch players from API.")
        return []

def get_user_games(username):
    try:
        response = requests.get(f"{API_BASE_URL}/profiles/{username}/games")
        response.raise_for_status()
        return response.json()  # List of games: game_name, game_id
    except requests.exceptions.RequestException:
        st.error("Failed to fetch games from API.")
        return []

# --- Fetch data ---
players = get_all_players()
games = get_user_games(username)

if not players or not games:
    st.stop()

player_options = {player['username']: player['isPremium'] for player in players}
game_options = {game['game_name']: game['game_id'] for game in games}

# --- Page layout ---
st.title("Select Players and Game to Compare")
st.write("Choose two players and a game to compare stats.")

selected_game_name = st.selectbox("Select Game", list(game_options.keys()))
selected_game_id = game_options[selected_game_name]

player1_name = st.selectbox("Select Player 1", list(player_options.keys()))
player2_name = st.selectbox("Select Player 2", list(player_options.keys()))

player1_premium = player_options[player1_name]
player2_premium = player_options[player2_name]

# --- Compare button ---
if st.button("Compare Players"):
    if player1_name == player2_name:
        st.warning("Please select two different players.")
    else:
        st.session_state['compare'] = {
            'player1_name': player1_name,
            'player2_name': player2_name,
            'game_id': selected_game_id,
            'game_name': selected_game_name,
            'show_maps_weapons': player1_premium and player2_premium
        }
        st.switch_page("33_Compare_Players")
