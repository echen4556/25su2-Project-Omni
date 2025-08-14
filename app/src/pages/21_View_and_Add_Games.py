import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Game Administration Page')

st.write('\n\n')
st.write('Options')

##Name of game to add
st.text_input("Name of Game to Add", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")


##List of added Games
games = []

st.table(games)

if st.button("⬅ Back to Admin Home"):
    st.switch_page("pages/17_Jordan_Lee_home.py")
