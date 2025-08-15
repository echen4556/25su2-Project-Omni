import os
import logging
import requests
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

# ---------- Page setup ----------
st.set_page_config(layout="wide")
SideBarLinks()

st.title("Administration Page")
st.write("\n\n")
st.write("Options")

# ---------- API location ----------
API_ROOT = os.getenv("API_ROOT", "http://web-api:4000").rstrip("/")

# The blueprint is mounted at /profiles, and the routes also begin with /profiles,
# so the final paths are /profiles/profiles[...]
PROFILES_BASE = f"{API_ROOT}/profiles"
PROFILES_URL  = f"{PROFILES_BASE}/profiles"   # list/search endpoint

# ---------- Helpers ----------
def normalize_profiles(raw):
    """
    Convert backend rows to dicts.
    Backend returns either:
      - list of dicts with keys: profileID, username, isAdmin, isPublic, isPremium
      - OR list of tuples in that order
    We normalize to: {"ID", "Username", "Admin", "Public", "Premium"}
    """
    if not raw:
        return []
    first = raw[0]
    if isinstance(first, dict):
        return [{
            "ID":        p.get("profileID"),
            "Username":  p.get("username"),
            "Admin":     p.get("isAdmin"),
            "Public":    p.get("isPublic"),
            "Premium":   p.get("isPremium"),
        } for p in raw]

    # assume tuple/list order: (profileID, username, isAdmin, isPublic, isPremium)
    out = []
    for p in raw:
        pid    = p[0] if len(p) > 0 else None
        uname  = p[1] if len(p) > 1 else None
        admin  = p[2] if len(p) > 2 else None
        public = p[3] if len(p) > 3 else None
        prem   = p[4] if len(p) > 4 else None
        out.append({
            "ID": pid, "Username": uname, "Admin": admin, "Public": public, "Premium": prem
        })
    return out

@st.cache_data(ttl=30)
def fetch_all_profiles():
    r = requests.get(PROFILES_URL, timeout=8)
    r.raise_for_status()
    try:
        data = r.json()
    except ValueError:
        raise ValueError("Profiles endpoint did not return JSON")
    return normalize_profiles(data)

# ---------- UI: search ----------
search_name = st.text_input(
    "Name of Player",
    value="",
    placeholder="Enter profile name to search"
).strip()

results = []
if search_name:
    with st.spinner("Searching..."):
        try:
            all_profiles = fetch_all_profiles()
            term = search_name.lower()
            results = [p for p in all_profiles if term in (p["Username"] or "").lower()]
        except requests.RequestException as e:
            st.error(f"Error contacting server: {e}")
        except ValueError as e:
            st.error(str(e))

# ---------- Display ----------
if results:
    df = pd.DataFrame(results).set_index("ID")  # puts ID on the left (no extra index column)
    st.table(df)
elif search_name:
    st.info("No matching profiles found.")
else:
    st.caption("Type a name to search.")

# ---------- Back button ----------
if st.button("⬅ Back to Admin Home"):
    st.switch_page("pages/17_Jordan_Lee_home.py")