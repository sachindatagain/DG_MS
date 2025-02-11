import streamlit as st 
import mysql.connector
import pandas as pd

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="mysql-108.cjgk23oumdif.us-gov-west-1.rds.amazonaws.com",
            user="vendor_portal_usr",
            password="Summer2021",
            database="vendor_portal"
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error connecting to the database: {err}")
        return None
