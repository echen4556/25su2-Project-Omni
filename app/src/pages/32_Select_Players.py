import streamlit as st

# -------------------------------
# Mock data (replace with DB later)
# -------------------------------
games = [
    {"gameID": 1, "name": "Valorant"},
    {"gameID": 2, "name": "Counter-Strike 2"},
    {"gameID": 3, "name": "Heretic"},
]

players = [
    {"profileID": 1, "username": "Emma", "isPremium": True},
    {"profileID": 2, "username": "Matthew", "isPremium": False},
    {"profileID": 3, "username": "Alice", "isPremium": True},
    {"profileID": 4, "username": "Bob", "isPremium": False},
]

game_options = {game['name']: game['gameID'] for game in games}
player_options = {player['username']: (player['profileID'], player['isPremium']) for player in players}

# -------------------------------
# Page layout
# -------------------------------
st.title("Select Players and Game to Compare")
st.write("Choose two players and a game to compare stats.")

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
        st.switch_page("pages/33_Compare_Players.py")

