import os
import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')
SideBarLinks()

st.title('Administration Page')
st.write('\n\n')
st.write('Options')

API_BASE = os.getenv("API_BASE", "http://web-api:4000/api")

##Name of game to add
search_name = st.text_input(
    "Name of Player",
    value="",
    placeholder="Enter profile name to search"
)

profile = []

if search_name.strip():
    with st.spinner("Searching..."):
        try:
            resp = requests.get(f"{API_BASE}/profiles", timeout=5)
            resp.raise_for_status()
            all_profiles = resp.json()
            term = search_name.lower()
            profile = [p for p in all_profiles if term in (p.get('username') or '').lower()]
        except requests.RequestException as e:
            st.error(f"Error contacting server: {e}")
        except ValueError:
            st.error("Unexpected response from server (not JSON).")

if profile:
    st.table(profile)
elif search_name.strip():
    st.info("No matching profiles found.")
else:
    st.caption("Type a name to search.")

if st.button("⬅ Back to Admin Home"):
    st.switch_page("pages/17_Jordan_Lee_home.py")
