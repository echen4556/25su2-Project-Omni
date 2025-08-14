import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

# Page layout setup
st.set_page_config(layout='wide')

# Show sidebar links for the current user
SideBarLinks()

# Title and welcome message
st.title(f"Welcome to Omni.gg, {st.session_state['username']}.")
st.write('')
st.write('Your central hub for game analytics, player stats, and strategy tools.')
st.write('')

# Navigation buttons for Omni app features
if st.button('📊 View Player Stats Dashboard',
             type='primary',
             use_container_width=True):
    st.switch_page('player_stats_dashboard')

if st.button('🔫 Weapon Analytics',
             type='primary',
             use_container_width=True):
    st.switch_page('weapon_analytics')

if st.button('🗺️ Map Insights',
             type='primary',
             use_container_width=True):
    st.switch_page('map_insights')

if st.button('🤝 Compare Players',
             type='primary',
             use_container_width=True):
    st.switch_page('View_Statspages/32_Select_Players.py')