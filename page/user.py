import streamlit as st
import page.export_data as export_data  # Import the export_data.py page

def user_page():
    # Ensure username and email are fetched from session state
    username = st.session_state.get("username", "Not Available")
    email = st.session_state.get("email", "Not Available")

    # Sidebar profile section
    st.sidebar.title("User Profile")
    st.sidebar.info(f"""
    **Name:** {username}  
    **Email:** {email}
    """)

    # Sidebar options for "Export Data" and "Logout"
    option = st.sidebar.radio("Select Option", ["Export Data", "Logout"], key="user_options")

    # Handle "Export Data" selection
    if option == "Export Data":
        # Navigate to export data page
        export_data.export_data_page()
    
    # Handle "Logout" selection
    elif option == "Logout":
        # Log out logic: Reset session state and redirect to login
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.email = None
        st.success("Logged out successfully!")


if __name__ == "__main__":
    user_page()  # Call the user page function once
