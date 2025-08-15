import streamlit as st

st.set_page_config(layout="wide")
st.title("💎 Premium Upgrade")

# Check if already premium
is_premium = st.session_state.get('is_premium', False)

# Premium info section
if not is_premium:
    st.write("Unlock exclusive features: Weapon Analytics, Map Insights, and more!")

    # Example pricing/info
    st.markdown("""
    **Premium Pricing:**
    - $4.99/month  
    - $49.99/year
    """)

    if st.button("💳 Upgrade to Premium"):
        st.session_state['is_premium'] = True
        st.success("🎉 Upgrade successful! You now have Premium access.")

# Back button goes to Emma's home page
if st.button("🔙 Back to Dashboard"):
    st.switch_page("pages/03_Emma_Smith_home.py")

# Optional: Only show "already premium" if they haven't clicked back
elif is_premium:
    st.success("You already have Premium! 🎉")
