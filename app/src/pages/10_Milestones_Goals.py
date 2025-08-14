import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

# Page layout setup
st.set_page_config(layout='wide')

# Show sidebar links for the current user
SideBarLinks()

# Title
st.title(f"Welcome to Omni, {st.session_state['first_name']}.")
st.write('')
st.write('Track your progress with milestones and set actionable goals to stay on top of your performance.')
st.write('')

# Milestones Section
st.subheader("🏆 Milestones")
st.write("View and manage your key achievements and completed objectives.")

if st.button('📅 View All Milestones',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/06_View_Milestones.py')

if st.button('➕ Add New Milestone',
             type='secondary',
             use_container_width=True):
    st.switch_page('pages/07_Add_Milestone.py')

st.write('---')  # Separator line

# Goals Section
st.subheader("🎯 Goals")
st.write("Plan your next objectives and track progress toward achieving them.")

if st.button('📋 View Current Goals',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/08_View_Goals.py')

if st.button('➕ Set New Goal',
             type='secondary',
             use_container_width=True):
    st.switch_page('pages/09_Add_Goals.py')
