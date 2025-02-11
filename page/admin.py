import streamlit as st

def admin_page():
    """
    Welcome to Admin page 
    """
    # Sidebar title
    st.sidebar.title("Admin Profile")
    
    # Check if username and email exist in session state
    if st.session_state.get("username") and st.session_state.get("email"):
         st.sidebar.info(f"""     
            **Name:** {st.session_state.username}  
            **Email:** {st.session_state.email} 
    """) # it will highlight the Admin/User information
    else:
        st.sidebar.error("Error: Admin details not found!")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Go to:", ["Dashboard", "User Details", "Import CSV","Add User","Admin Export","Forecast","Logout"])

    # Navigation logic
    if section == "Dashboard":
        try:
            from page.dashboard import admin_dashboard
            admin_dashboard()  # Call the admin_dashboard function
        except ImportError as e:
            st.error(f"Error loading Dashboard: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    elif section == "User Details":
        try:
            from page.user_detail import user_details
            user_details()  # Call the user_details function
        except ImportError as e:  # basically runs when the user_details.py is not founded or else the function is not running
            st.error(f"Error loading User Details: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    elif section == "Import CSV":
        try:
            from page.import_csv import import_csv_page
            import_csv_page()  # Call the import_csv_page function
        except ImportError as e:
            st.error(f"Error loading Import CSV: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    
    elif section == "Add User":
        try:
            from page.add_user import add_user
            add_user()
        except ImportError as e:
            st.error(f"Error loading ADD USER: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    elif section == "Admin Export":
        try:
            from page.admin_export import admin_export_page
            admin_export_page()
        except ImportError as e:
            st.error(f"Error loading ADD USER: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    elif section == "Forecast":
        try:
            from page.forecast_pg import forecast_page
            forecast_page()
        except ImportError as e:
            st.error(f"Error loading Forecast: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    elif section == "Logout":
        # Log out logic: Reset session state
        st.session_state.logged_in = False
        st.session_state.role = None

        # Redirect back to login using an empty placeholder
        st.success("Logged out successfully!")
        placeholder = st.empty()  # Create a placeholder widget
        with placeholder:
            st.write("Redirecting to login...")
            st.session_state.page = "Login"

        # Terminate execution to force page rerun
        st.stop()

    else:
        st.write("Select a section from the sidebar to get started.")
