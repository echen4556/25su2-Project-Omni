##################################################
# Page 33: Compare Players Stats
##################################################

import streamlit as st

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
show_maps_weapons = compare['show_maps_weapons']

# -------------------------------
# Page layout
# -------------------------------
st.title(f"Comparing {player1_name} vs {player2_name}")
st.subheader(f"Game: {game_name}")

# -------------------------------
# Mock stats (replace with DB later)
# -------------------------------
mock_stats = {
    player1_name: {"Kills": 20, "Deaths": 5, "Headshots": 8, "Assists": 7},
    player2_name: {"Kills": 15, "Deaths": 7, "Headshots": 5, "Assists": 10},
}

# -------------------------------
# Display side-by-side stats
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {player1_name}")
    for stat, value in mock_stats[player1_name].items():
        st.write(f"**{stat}:** {value}")

with col2:
    st.markdown(f"### {player2_name}")
    for stat, value in mock_stats[player2_name].items():
        st.write(f"**{stat}:** {value}")

# -------------------------------
# Premium feature display
# -------------------------------
st.markdown("---")
if show_maps_weapons:
    st.success("Premium: Maps and weapons stats are visible")
    # Example: extra stats
    st.write("Additional stats could go here: Map win rate, weapon accuracy, etc.")
else:
    st.info("Maps and weapons stats are hidden (premium only)")

# -------------------------------
# Optional: Back button
# -------------------------------
if st.button("Back to Player Selection"):
    st.switch_page("32_Select_Players")  # Switch back to Page 32
