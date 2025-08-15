import streamlit as st
import requests
import pandas as pd

API_BASE_URL = 'http://api:4000'  # adjust if different

# -------------------------------
# Ensure comparison data exists
# -------------------------------
if "compare" not in st.session_state:
    st.warning("No players selected to compare. Please go back to Page 32.")
    st.stop()

compare = st.session_state['compare']
player1_name = compare['player1_name']
player2_name = compare['player2_name']
game_name = compare['game_name']

# -------------------------------
# Helper functions
# -------------------------------
def get_profile(username, game_name):
    try:
        response = requests.get(f"{API_BASE_URL}/profiles/{username}")
        response.raise_for_status()
        profile = response.json()
        # Find the game instance for this game
        game_instance = next((g for g in profile['games'] if g['game_name'] == game_name), None)
        if game_instance:
            return {
                "profileID": profile['profileID'],
                "isPremium": profile['isPremium'],
                "gameID": game_instance['game_id'],
                "gameUsername": game_instance['gameUsername']
            }
        else:
            return None
    except requests.exceptions.RequestException:
        st.error(f"Failed to fetch profile for {username}")
        return None

def get_player_stats(profile_id, game_id):
    try:
        response = requests.get(f"{API_BASE_URL}/playerstats/{profile_id}/{game_id}")
        response.raise_for_status()
        return response.json()  # Expected: {"Kills":.., "Deaths":.., "Assists":.., "Headshots":..}
    except requests.exceptions.RequestException:
        return {"Kills":0, "Deaths":0, "Assists":0, "Headshots":0}

def get_maps(profile_id, game_id):
    try:
        response = requests.get(f"{API_BASE_URL}/maps/{profile_id}/{game_id}")
        response.raise_for_status()
        return response.json()  # List of maps with stats
    except requests.exceptions.RequestException:
        return []

def get_weapons(profile_id, game_id):
    try:
        response = requests.get(f"{API_BASE_URL}/weapons/{profile_id}/{game_id}")
        response.raise_for_status()
        return response.json()  # List of weapons with stats
    except requests.exceptions.RequestException:
        return []

# -------------------------------
# Gather data for both players
# -------------------------------
player_data = {}
for player_name in [player1_name, player2_name]:
    profile = get_profile(player_name, game_name)
    if not profile:
        st.error(f"No profile found for {player_name} in {game_name}")
        st.stop()
    
    stats = get_player_stats(profile['profileID'], profile['gameID'])
    premium = profile['isPremium']
    
    maps, weapons = ([], [])
    if premium:
        maps = get_maps(profile['profileID'], profile['gameID'])
        weapons = get_weapons(profile['profileID'], profile['gameID'])
    
    player_data[player_name] = {
        "stats": stats,
        "isPremium": premium,
        "maps": maps,
        "weapons": weapons
    }

# -------------------------------
# Display stats
# -------------------------------
st.title(f"Comparing {player1_name} vs {player2_name}")
st.subheader(f"Game: {game_name}")

col1, col2 = st.columns(2)
for col, player_name in zip([col1, col2], [player1_name, player2_name]):
    data = player_data[player_name]
    with col:
        st.markdown(f"### {player_name}")
        # Main stats
        for stat, value in data['stats'].items():
            st.write(f"**{stat}:** {value}")
        
        # Premium maps & weapons
        if data['isPremium']:
            st.success("Premium: Maps & Weapons Stats")
            
            # Maps
            st.write("**Maps:**")
            if data['maps']:
                for m in data['maps']:
                    st.write(f"{m['Name']} – {m.get('kills',0)} kills, {m.get('wins',0)} wins")
            else:
                st.write("No map data available.")
            
            # Weapons
            st.write("**Weapons:**")
            if data['weapons']:
                for w in data['weapons']:
                    st.write(f"{w['name']} – {w.get('kills',0)} kills, Accuracy: {w.get('accuracy',0)}")
            else:
                st.write("No weapon data available.")
        else:
            st.info("Maps and weapons stats are hidden (premium only)")

# -------------------------------
# Optional: Back button
# -------------------------------
if st.button("Back to Player Selection"):
    st.switch_page("32_Select_Players")
