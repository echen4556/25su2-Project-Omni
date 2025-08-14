import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    This is a demo app for analyzing and consolidating the statistical data of
    video game players of various games.

    The goal of this demo is to provide a model of our app that will allow the user to utilize
    all of our app's planned features such as viewing player data, weapon data, map data, and 
    comparing players to one another via their data. 

    Stay tuned for more information and features to come!
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
