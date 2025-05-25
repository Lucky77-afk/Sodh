"""
Sodh - Solana Blockchain Explorer
"""
import streamlit as st

# Set page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="Sodh - Solana Blockchain Explorer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stButton>button {
        background-color: #14F195;
        color: #000000;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        color: #14F195;
    }
    </style>
""", unsafe_allow_html=True)

# Main app content
st.title("Sodh - Solana Blockchain Explorer 🔍")
st.write("Welcome to Sodh, your gateway to exploring the Solana blockchain!")

# Add a sample component
st.header("Blockchain Explorer")
wallet_address = st.text_input("Enter a Solana wallet address:", "")

if st.button("Search"):
    if wallet_address:
        st.success(f"Searching for wallet: {wallet_address}")
    else:
        st.warning("Please enter a wallet address")

# Navigation
st.sidebar.header("Navigation")
menu = ["Dashboard", "Transactions", "Accounts", "Smart Contracts"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Dashboard":
    st.subheader("Dashboard")
    st.write("Welcome to the dashboard!")
elif choice == "Transactions":
    st.subheader("Transactions")
    st.write("Transaction history will appear here")
elif choice == "Accounts":
    st.subheader("Accounts")
    st.write("Account information will appear here")
elif choice == "Smart Contracts":
    st.subheader("Smart Contracts")
    st.write("Smart contract interactions will appear here")

# Add a simple footer
st.markdown("---")
st.markdown("### Sodh - Solana Blockchain Explorer")
st.markdown("*Built with ❤️ and Streamlit*")
