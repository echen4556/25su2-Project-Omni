import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

# Page layout setup
st.set_page_config(layout='wide')

# Show sidebar links for the current user
SideBarLinks()

# Get premium status from session (set during login)
is_premium = st.session_state.get('isPremium', False)

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

# Premium section
if is_premium:
    if st.button('🔫 Weapon Analytics',
                 type='primary',
                 use_container_width=True):
        st.switch_page('weapon_analytics')

    if st.button('🗺️ Map Insights',
                 type='primary',
                 use_container_width=True):
        st.switch_page('map_insights')
else:
    if st.button('💎 Upgrade to Premium to Unlock Weapon & Map Stats',
                 type='secondary',
                 use_container_width=True):
        st.switch_page('premium_upgrade')

if st.button('🤝 Compare Players',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/32_Select_Players.py')



