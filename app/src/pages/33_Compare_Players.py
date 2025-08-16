import logging
import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(layout='wide')
SideBarLinks()

# Use the correct service name for Docker networking
API_BASE_URL = "http://api:4000"

# -------------------------------
# Ensure user is logged in and has data
# -------------------------------
if 'username' not in st.session_state:
    st.error("You must be logged in to view this page.")
    st.stop()

if "compare" not in st.session_state:
    st.warning("No players selected to compare. Go back to selection page.")
    st.stop()

compare = st.session_state['compare']
player1_name = compare['player1_name']
player2_name = compare['player2_name']
game_id = compare['game_id']
game_name = compare['game_name']
show_maps_weapons = compare['show_maps_weapons']

# -------------------------------
# Cached API helpers
# -------------------------------
@st.cache_data
def get_profile_id(username: str):
    """Fetches the profileID for a given username."""
    try:
        resp = requests.get(f"{API_BASE_URL}/profiles")
        resp.raise_for_status()
        profiles = resp.json()
        profile = next((p for p in profiles if p['username'] == username), None)
        return profile['profileID'] if profile else None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching profile for {username}: {e}")
        return None

@st.cache_data
def get_player_stats(profile_id: int, game_id: int):
    """Fetches summary stats for a player in a game."""
    try:
        resp = requests.get(f"{API_BASE_URL}/playerstats/summary/{profile_id}/{game_id}")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        return {}

@st.cache_data
def get_maps_stats(profile_id: int, game_id: int):
    """Fetches map stats for a player in a game."""
    try:
        resp = requests.get(f"{API_BASE_URL}/playerstats/map/{profile_id}/{game_id}")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        return []

@st.cache_data
def get_weapons_stats(profile_id: int, game_id: int):
    """Fetches weapon stats for a player in a game."""
    try:
        resp = requests.get(f"{API_BASE_URL}/playerstats/weapon/{profile_id}/{game_id}")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        return []

# -------------------------------
# Fetch data for both players
# -------------------------------
player1_id = get_profile_id(player1_name)
player2_id = get_profile_id(player2_name)

if not player1_id or not player2_id:
    st.error("Could not find a profile for one or both players.")
    st.stop()

player1_stats = get_player_stats(player1_id, game_id)
player2_stats = get_player_stats(player2_id, game_id)

# -------------------------------
# Display comparison
# -------------------------------
st.title(f"📊 Comparing {player1_name} vs {player2_name}")
st.subheader(f"Game: {game_name}")

# --- Combined Core Stats Table ---
if player1_stats and player2_stats:
    # Remove unwanted IDs before processing
    player1_stats.pop('statTableID', None)
    player1_stats.pop('gameInstanceID', None)
    player2_stats.pop('statTableID', None)
    player2_stats.pop('gameInstanceID', None)

    # Define which stats are better when higher
    higher_is_better = ['kills', 'assists', 'totalDamage', 'totalHeadshots', 'totalShotsHit', 'totalWins']

    # Convert stats to pandas Series for easier comparison
    p1_series = pd.Series(player1_stats, name=player1_name)
    p2_series = pd.Series(player2_stats, name=player2_name)

    # Combine into a single DataFrame
    stats_df = pd.concat([p1_series, p2_series], axis=1)

    # Calculate the comparison arrow
    comparison = []
    for stat, values in stats_df.iterrows():
        p1_val = values[player1_name]
        p2_val = values[player2_name]

        if p1_val == p2_val:
            comparison.append("➖")
            continue

        # Check if higher is better for this stat
        if stat in higher_is_better:
            if p1_val > p2_val:
                comparison.append("⬅️")
            else:
                comparison.append("➡️")
        # For stats where lower is better (like 'deaths')
        else:
            if p1_val < p2_val:
                comparison.append("⬅️")
            else:
                comparison.append("➡️")

    stats_df.insert(1, '🆚', comparison)

    st.subheader("Overall Performance")

    # Create headers with custom widths for a balanced look
    header_cols = st.columns([2, 3, 1, 3])
    header_cols[0].markdown("**Stat**")
    header_cols[1].markdown(f"<div style='text-align: center;'><b>{player1_name}</b></div>", unsafe_allow_html=True)
    header_cols[3].markdown(f"<div style='text-align: center;'><b>{player2_name}</b></div>", unsafe_allow_html=True)
    st.divider()

    # Iterate over the DataFrame to display rows with custom widths
    for index, row in stats_df.iterrows():
        row_cols = st.columns([2, 3, 1, 3])
        # Use index for the stat name, which is more robust
        row_cols[0].write(str(index).replace('_', ' ').title())
        row_cols[1].markdown(f"<div style='text-align: center;'>{str(row[player1_name])}</div>", unsafe_allow_html=True)
        row_cols[2].markdown(f"<div style='text-align: center;'>{row['🆚']}</div>", unsafe_allow_html=True)
        row_cols[3].markdown(f"<div style='text-align: center;'>{str(row[player2_name])}</div>", unsafe_allow_html=True)

else:
    st.info("No summary stats available for one or both players to compare.")

st.divider()

# --- Premium Maps & Weapons (in separate columns) ---
if show_maps_weapons:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {player1_name}'s Maps & Weapons")
        maps1_df = pd.DataFrame(get_maps_stats(player1_id, game_id))
        weapons1_df = pd.DataFrame(get_weapons_stats(player1_id, game_id))

        # Drop unwanted columns if they exist
        if not maps1_df.empty:
            maps1_df = maps1_df.drop(columns=['statTableID'], errors='ignore')
        if not weapons1_df.empty:
            weapons1_df = weapons1_df.drop(columns=['statTableID'], errors='ignore')

        st.write("**Maps:**")
        st.table(maps1_df)
        st.write("**Weapons:**")
        st.table(weapons1_df)

    with col2:
        st.markdown(f"### {player2_name}'s Maps & Weapons")
        maps2_df = pd.DataFrame(get_maps_stats(player2_id, game_id))
        weapons2_df = pd.DataFrame(get_weapons_stats(player2_id, game_id))

        # Drop unwanted columns if they exist
        if not maps2_df.empty:
            maps2_df = maps2_df.drop(columns=['statTableID'], errors='ignore')
        if not weapons2_df.empty:
            weapons2_df = weapons2_df.drop(columns=['statTableID'], errors='ignore')

        st.write("**Maps:**")
        st.table(maps2_df)
        st.write("**Weapons:**")
        st.table(weapons2_df)
else:
    st.info("Maps and weapons stats are hidden (premium only).")

# -------------------------------
# Back button
# -------------------------------
if st.button("⬅ Back to Player Selection", use_container_width=True):
    st.switch_page("pages/32_Select_Players.py")
