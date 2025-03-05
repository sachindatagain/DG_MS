import mysql.connector
import streamlit as st
import time

# Global connection pool
connection_pool = None
connection_timestamps = {}
MAX_IDLE_TIME = 30  # Increased idle timeout to 30 seconds for stability

def init_connection_pool():
    """Initialize the MySQL connection pool."""
    global connection_pool
    if connection_pool is None:
        try:
            st.info("🔄 Initializing MySQL connection pool...")
            connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=5,
                pool_reset_session=True,
                host="mysql-108.cjgk23oumdif.us-gov-west-1.rds.amazonaws.com",
                user="vendor_portal_usr",
                password="Summer2021",
                database="vendor_portal",
                autocommit=True,
                connect_timeout=30,
                use_pure=True
            )
        except mysql.connector.Error as err:
            st.error(f"❌ Error initializing connection pool: {err}")
            connection_pool = None  # Ensure it's explicitly None if failure occurs

def close_idle_connections():
    """Close idle connections safely."""
    global connection_timestamps
    current_time = time.time()
    to_remove = []

    for conn, last_used in list(connection_timestamps.items()):
        if conn and (current_time - last_used > MAX_IDLE_TIME):
            try:
                if hasattr(conn, 'is_connected') and conn.is_connected():
                    conn.close()
                to_remove.append(conn)
            except mysql.connector.Error as err:
                st.warning(f"⚠️ Error closing idle connection: {err}")

    for conn in to_remove:
        connection_timestamps.pop(conn, None)

def get_connection():
    """Get a database connection safely."""
    global connection_pool

    if connection_pool is None:
        st.warning("⚠️ Connection pool is not initialized. Initializing now...")
        init_connection_pool()
        if connection_pool is None:
            st.error("❌ Connection pool is unavailable. Check database settings.")
            return None

    close_idle_connections()

    try:
        conn = connection_pool.get_connection()
        if conn is None:
            st.error("❌ Failed to retrieve a connection from the pool.")
            return None

        if not hasattr(conn, 'is_connected') or not conn.is_connected():
            st.error("❌ Connection retrieved but is not active.")
            return None

        connection_timestamps[conn] = time.time()
        return conn
    except mysql.connector.errors.PoolError as err:
        st.error(f"❌ Connection pool exhausted: {err}")
        return None
    except mysql.connector.Error as err:
        st.error(f"❌ Unexpected error when getting connection: {err}")
        return None

def execute_query(query, params=None):
    """Execute a SQL query safely."""
    conn = get_connection()
    if not conn:
        st.error("❌ No database connection available.")
        return None  

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"❌ Query execution error: {err}")
        return None
    finally:
        if conn:
            conn.close()
            connection_timestamps.pop(conn, None)

def test_connection():
    """Test database connection."""
    conn = get_connection()
    if not conn:
        st.error("❌ Failed to establish a database connection.")
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                st.success("✅ Database connection is working fine.")
            else:
                st.warning("⚠️ Connected but query failed.")
    except mysql.connector.Error as err:
        st.error(f"❌ Query execution error: {err}")
    finally:
        if conn:
            conn.close()
            connection_timestamps.pop(conn, None)

if __name__ == "__main__":
    test_connection()




###################################################################

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
#                 pool_size=20,  # Increase based on workload
#                 pool_reset_session=True,
#                 host="mysql-108.cjgk23oumdif.us-gov-west-1.rds.amazonaws.com",
#                 user="vendor_portal_usr",
#                 password="Summer2021",
#                 database="vendor_portal",
#                 autocommit=True,
#                 connect_timeout=30,
#                 use_pure=True
#             )
#         except mysql.connector.Error as err:
#             st.error(f"Error initializing connection pool: {err}")

# def get_connection():
#     """Get a connection from the pool safely."""
#     global connection_pool
#     if connection_pool is None:
#         init_connection_pool()
    
#     try:
#         conn = connection_pool.get_connection()
#         if conn.is_connected():
#             return conn
#     except mysql.connector.errors.PoolError:
#         st.error("Connection pool exhausted. Please try again later.")
#     except mysql.connector.Error as err:
#         st.error(f"Database connection lost: {err}. Reconnecting...")
#         init_connection_pool()
#         return connection_pool.get_connection()  
#     return None

# def execute_query(query, params=None):
#     """Execute a query safely and ensure connection is closed."""
#     conn = get_connection()
#     if not conn:
#         return None

#     try:
#         with conn.cursor() as cursor:
#             cursor.execute(query, params or ())
#             return cursor.fetchall()
#     except mysql.connector.Error as err:
#         st.error(f"Query execution error: {err}")
#         return None
#     finally:
#         conn.close()  # 🔥 Always return connection to the pool

# # Test function
# def test_connection():
#     conn = get_connection()
#     if conn:
#         try:
#             with conn.cursor() as cursor:
#                 cursor.execute("SELECT 1")
#                 result = cursor.fetchone()
#                 if result:
#                     st.success("Database connection is working fine.")
#                 else:
#                     st.warning("Connected but query failed.")
#         except mysql.connector.Error as err:
#             st.error(f"Query execution error: {err}")
#         finally:
#             conn.close()  # 🔥 Return connection to the pool

# if __name__ == "__main__":
#     test_connection()  # Run connection test


####################################################################################

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

###################################################################################################
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
