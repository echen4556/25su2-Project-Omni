import streamlit as st
import requests
import pandas as pd

API_BASE_URL = 'http://api:4000' 

# --- Ensure comparison exists ---
if "compare" not in st.session_state:
    st.warning("No players selected to compare. Go back to Page 32.")
    st.stop()

compare = st.session_state['compare']
player1_name = compare['player1_name']
player2_name = compare['player2_name']
game_name = compare['game_name']
show_maps_weapons = compare['show_maps_weapons']

# --- Ensure user is logged in ---
if 'username' not in st.session_state:
    st.error("You must be logged in to view this page.")
    st.stop()

# --- Helper functions ---
def get_profile(username, game_name):
    """Fetch user profile and find the game instance"""
    try:
        response = requests.get(f"{API_BASE_URL}/profiles/{username}")
        response.raise_for_status()
        profile = response.json()
        game_instance = next((g for g in profile['games'] if g['game_name'] == game_name), None)
        if game_instance:
            return {
                "username": profile['username'],
                "isPremium": profile['isPremium'],
                "gameID": game_instance['game_id']
            }
        else:
            return None
    except requests.exceptions.RequestException:
        st.error(f"Failed to fetch profile for {username}")
        return None

def get_player_stats(username, game_id):
    try:
        response = requests.get(f"{API_BASE_URL}/playerstats/{username}/{game_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return {"Kills":0,"Deaths":0,"Assists":0,"Headshots":0}

def get_maps(username, game_id):
    try:
        response = requests.get(f"{API_BASE_URL}/maps/{username}/{game_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []

def get_weapons(username, game_id):
    try:
        response = requests.get(f"{API_BASE_URL}/weapons/{username}/{game_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []

# --- Gather data for both players ---
player_data = {}
for player_name in [player1_name, player2_name]:
    profile = get_profile(player_name, game_name)
    if not profile:
        st.error(f"No profile found for {player_name} in {game_name}")
        st.stop()
    
    stats = get_player_stats(player_name, profile['gameID'])
    
    maps, weapons = ([], [])
    if profile['isPremium']:
        maps = get_maps(player_name, profile['gameID'])
        weapons = get_weapons(player_name, profile['gameID'])
    
    player_data[player_name] = {
        "stats": stats,
        "isPremium": profile['isPremium'],
        "maps": maps,
        "weapons": weapons
    }

# --- Display stats ---
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
        if data['isPremium'] and show_maps_weapons:
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

# --- Back button ---
if st.button("Back to Player Selection"):
    st.switch_page("32_Select_Players")
