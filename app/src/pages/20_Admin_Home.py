import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('System Admin Home Page')

if st.button('Add Games', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_View_and_Add_Games.py')


if st.button("⬅ Back to Home"):
    st.switch_page("Home.py")