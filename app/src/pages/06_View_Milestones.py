import logging
import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)
API_BASE_URL = "http://host.docker.internal:4000" 

st.set_page_config(layout='wide')
SideBarLinks()

# Ensure user is logged in
if 'username' not in st.session_state or 'profileID' not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

profile_id = st.session_state['profileID']

st.title("📅 Progress Timeline")
st.write("A chronological view of your milestones and goals:")

def fetch_data(endpoint):
    try:
        r = requests.get(f"{API_BASE_URL}/{endpoint}/profile/{profile_id}")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching {endpoint}: {e}")
        return []

# Fetch milestones & goals
milestones = fetch_data("milestones")
goals = fetch_data("goals")

# Build combined timeline list
timeline_entries = []

for m in milestones:
    if m.get('dateAchieved'):
        timeline_entries.append({
            "type": "🏆 Milestone",
            "color": "#FFD700",  # gold
            "description": m.get("description", "No description"),
            "date": m['dateAchieved'],
            "category": m.get("category", ""),
            "notes": m.get("notes", "")
        })

for g in goals:
    if g.get('dateCreated'):
        timeline_entries.append({
            "type": "🎯 Goal Created",
            "color": "#1E90FF",  # blue
            "description": g.get("description", "No description"),
            "date": g['dateCreated'],
            "category": g.get("category", ""),
            "notes": g.get("notes", "")
        })
    if g.get('dateAchieved'):
        timeline_entries.append({
            "type": "✅ Goal Achieved",
            "color": "#4CAF50",  # green
            "description": g.get("description", "No description"),
            "date": g['dateAchieved'],
            "category": g.get("category", ""),
            "notes": g.get("notes", "")
        })

# Convert to DataFrame & sort by date
if timeline_entries:
    df = pd.DataFrame(timeline_entries)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.sort_values(by='date')

    # Timeline CSS
    st.markdown("""
    <style>
    .timeline {
        border-left: 3px solid #bbb;
        margin-left: 20px;
        padding-left: 20px;
    }
    .timeline-item {
        margin-bottom: 20px;
        position: relative;
    }
    .timeline-dot {
        position: absolute;
        left: -14px;
        top: 6px;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        border: 2px solid white;
        box-shadow: 0 0 0 3px #bbb;
    }
    .timeline-date {
        font-size: 0.85em;
        color: gray;
    }
    .timeline-title {
        font-weight: bold;
    }
    .extra-info {
        font-size: 0.85em;
        color: #444;
    }
    </style>
    """, unsafe_allow_html=True)

    # Render timeline
    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for _, row in df.iterrows():
        st.markdown(f"""
        <div class="timeline-item">
            <div class="timeline-dot" style="background-color: {row['color']};"></div>
            <div class="timeline-title">{row['type']}</div>
            <div class="timeline-date">{row['date'].strftime('%b %d, %Y')}</div>
            <div>{row['description']}</div>
            <div class="extra-info"><strong>Category:</strong> {row['category']}</div>
            <div class="extra-info"><strong>Notes:</strong> {row['notes']}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("No milestones or goals to display yet.")

if st.button("⬅ Back to Home"):
    st.switch_page("Home.py")
