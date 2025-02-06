import streamlit as st
from page.db import get_connection

# Login function to authenticate user and fetch details
def login(email, password):
    connection = get_connection()
    if connection:
        try:
            query = "SELECT employee_name, email, role FROM employees WHERE email = %s AND password = %s;"
            cursor = connection.cursor() # middleman to send the query from streamlit to mysql server
            cursor.execute(query, (email, password)) # execution is done here 
            result = cursor.fetchone()  # Fetch the first row
            cursor.close()
            connection.close() # used to close connectivity made by connection.cursor() from streamlit to mysql server
            if result:
                # Store user details in session state
                st.session_state.username = result[0]  # Store the user's name
                st.session_state.email = result[1]     # Store the user's email
                return result[2]  # Return the user's role (admin/user)
            else:
                return None
        except Exception as e:
            st.error(f"Error during login: {e}")
            return None
    return None

# Initialize session state if not already done
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None
if "email" not in st.session_state:
    st.session_state.email = None
if "page" not in st.session_state:
    st.session_state.page = "Login"  # Default to login page

# Handle page navigation
if st.session_state.page == "Login":
    # Display login page
    st.title("Login Page")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    # Handle login attempt
    if login_button:
        role = login(email, password)
        if role == "admin":
            st.success(f"Logged in as Admin: {st.session_state.username}")
            st.session_state.role = "admin"  # Store role in session state
            st.session_state.logged_in = True  # Mark the user as logged in
            st.session_state.page = "Admin"  # Set page to Admin
        elif role == "user":
            st.success(f"Logged in as User: {st.session_state.username}")
            st.session_state.role = "user"  # Store role in session state
            st.session_state.logged_in = True  # Mark the user as logged in
            st.session_state.page = "User"  # Set page to User
        else:
            st.error("Invalid credentials. Please try again.")

elif st.session_state.page == "Admin" and st.session_state.role == "admin":
    import page.admin  # Import admin page
    page.admin.admin_page()  # Navigate to Admin page

elif st.session_state.page == "User" and st.session_state.role == "user":
    import page.user  # Import user page
    page.user.user_page()  # Navigate to User page

else:
    st.error("Something went wrong. Please try logging in again.")

#----------------------------------------------------------------------------------------------------------
