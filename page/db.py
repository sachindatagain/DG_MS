import mysql.connector
import streamlit as st

# Global connection pool
connection_pool = None  

def init_connection_pool():
    """Initialize the MySQL connection pool."""
    global connection_pool
    if connection_pool is None:
        try:
            pool_size = 10  # Set within the valid range (1-32)

            connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=pool_size,  # Ensuring pool size is within the allowed range
                pool_reset_session=True,
                host="mysql-108.cjgk23oumdif.us-gov-west-1.rds.amazonaws.com",
                user="vendor_portal_usr",
                password="Summer2021",
                database="vendor_portal",
                autocommit=True,
                connect_timeout=30,
                use_pure=True
            )
#            st.success(f"Database connection pool initialized successfully with size {pool_size}.")
        except mysql.connector.Error as err:
            st.error(f"Error initializing connection pool: {err}")

def get_connection():
    """Get a connection from the pool and ensure proper handling."""
    global connection_pool
    if connection_pool is None:
        init_connection_pool()
    
    try:
        conn = connection_pool.get_connection()
        if conn.is_connected():
            return conn
        else:
            st.warning("Database connection not active. Retrying...")
            init_connection_pool()
            return connection_pool.get_connection()
    except mysql.connector.errors.PoolError:
        st.error("Connection pool exhausted. Please try again later.")
        return None
    except mysql.connector.Error as err:
        st.error(f"Database connection lost: {err}. Reconnecting...")
        init_connection_pool()
        return connection_pool.get_connection()  # Retry with a new connection

def test_connection():
    """Test database connection to ensure credentials work."""
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    st.success("Database connection is working fine.")
                else:
                    st.warning("Connected but query failed.")
        except mysql.connector.Error as err:
            st.error(f"Query execution error: {err}")
        finally:
            conn.close()  # Always close the connection to return it to the pool

if __name__ == "__main__":
    test_connection()  # Run connection test


# import mysql.connector
# import streamlit as st

# # Global connection pool
# connection_pool = None  

# def init_connection_pool():
#     """Initialize the MySQL connection pool."""
#     global connection_pool
#     if connection_pool is None:
#         try:
#             connection_pool = mysql.connector.pooling.MySQLConnectionPool(
#                 pool_name="mypool",
#                 pool_size=20,  # Increase pool size to handle more concurrent connections
#                 pool_reset_session=True,  # Ensures fresh sessions for new connections
#                 host="mysql-108.cjgk23oumdif.us-gov-west-1.rds.amazonaws.com",
#                 user="vendor_portal_usr",
#                 password="Summer2021",
#                 database="vendor_portal",
#                 autocommit=True,
#                 connect_timeout=600,
#                 use_pure=True
#             )
#         except mysql.connector.Error as err:
#             st.error(f"Error initializing connection pool: {err}")

# def get_connection():
#     """Get a connection from the pool and ensure proper handling."""
#     global connection_pool
#     if connection_pool is None:
#         init_connection_pool()
    
#     try:
#         conn = connection_pool.get_connection()
#         return conn
#     except mysql.connector.errors.PoolError:
#         st.error("Connection pool exhausted. Try again later.")
#         return None
#     except mysql.connector.Error as err:
#         st.error(f"Database connection lost: {err}. Reconnecting...")
#         init_connection_pool()
#         return connection_pool.get_connection()  # Retry with a new connection


# import streamlit as st 
# import mysql.connector
# import pandas as pd

# def get_connection():
#     try:
#         connection = mysql.connector.connect(
#             host="mysql-108.cjgk23oumdif.us-gov-west-1.rds.amazonaws.com",
#             user="vendor_portal_usr",
#             password="Summer2021",
#             database="vendor_portal"
#         )
#         return connection
#     except mysql.connector.Error as err:
#         st.error(f"Error connecting to the database: {err}")
#         return None
