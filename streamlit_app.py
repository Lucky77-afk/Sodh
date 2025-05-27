"""
Sodh - Solana Blockchain Explorer (Minimal Example)
"""
import streamlit as st

# Set page config (must be the first Streamlit command)
st.set_page_config(
    page_title="Sodh - Solana Explorer",
    page_icon="🔍",
    layout="wide"
)

# Add a title
st.title("🔍 Sodh - Solana Blockchain Explorer")
st.write("Welcome to Sodh! This is a minimal working example.")

# Add a simple input
user_input = st.text_input("Enter something:")
if user_input:
    st.write(f"You entered: {user_input}")

# Add a button
if st.button("Click me!"):
    st.balloons()
    st.success("Success! The app is working!")

# Add a footer
st.markdown("---")
st.markdown("### About Sodh")
st.markdown("A minimal working example for Streamlit Cloud deployment")
