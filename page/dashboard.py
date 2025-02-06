import streamlit as st
import pandas as pd
import plotly.express as px
from page.db import get_connection

def fetch_processing_tool_usage(): 
    connection = get_connection()
    if not connection:
        return None, "Failed to connect to the database."
    try:
        query = """
            SELECT ocr, COUNT(*) AS user_count
            FROM admin_database
            WHERE ocr IS NOT NULL
            GROUP BY ocr
            ORDER BY user_count DESC;
        """
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return pd.DataFrame(result), None
    except Exception as e:
        return None, str(e)

def fetch_top_payers(): 
    connection = get_connection()
    if not connection:
        return None, "Failed to connect to the database."
    try:
        query = """
            SELECT payer, COUNT(*) AS payer_count
            FROM admin_database
            WHERE payer IS NOT NULL
            GROUP BY payer
            ORDER BY payer_count DESC
            LIMIT 20;
        """
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return pd.DataFrame(result), None
    except Exception as e:
        return None, str(e)
    
def fetch_emea_distribution():
    connection = get_connection()
    if not connection:
        return None, "Failed to connect to the database."
    try:
        query = """
            SELECT EMEA, COUNT(*) AS count
            FROM admin_database
            WHERE EMEA IS NOT NULL
            GROUP BY EMEA
            ORDER BY count DESC;
        """
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return pd.DataFrame(result), None
    except Exception as e:
        return None, str(e)

def fetch_priority_distribution():
    connection = get_connection()
    if not connection:
        return None, "Failed to connect to the database."
    try:
        query = """
            SELECT priority, COUNT(*) AS count
            FROM admin_database
            WHERE priority IS NOT NULL
            GROUP BY priority
            ORDER BY count DESC;
        """
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return pd.DataFrame(result), None
    except Exception as e:
        return None, str(e)

def fetch_top_languages():
    connection = get_connection()
    if not connection:
        return None, "Failed to connect to the database."
    try:
        query = """
            SELECT foreign_language AS language, COUNT(*) AS count
            FROM admin_database
            WHERE foreign_language IS NOT NULL
            GROUP BY foreign_language
            ORDER BY count DESC
            LIMIT 5;
        """
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return pd.DataFrame(result), None
    except Exception as e:
        return None, str(e)

def admin_dashboard():
    st.title("Admin Dashboard")

    # Processing Tool Usage
    usage_df, error = fetch_processing_tool_usage()
    if error:
        st.error(f"Error fetching usage data: {error}")
        return
    if not usage_df.empty:
        st.subheader("OCR wise volume")
        fig_usage = px.bar(usage_df, x="ocr", y="user_count", title="Volume Count of OCR Tool", labels={"ocr": "OCR Tool", "user_count": "User Count"}, text="user_count")
        fig_usage.update_traces(textposition="outside")
        st.plotly_chart(fig_usage)
    
    # Top 20 Payers Scatter Bar Chart
    payers_df, error = fetch_top_payers()
    if error:
        st.error(f"Error fetching payers data: {error}")
        return
    if not payers_df.empty:
        # Sort the DataFrame in ascending order of payer_count
        payers_df = payers_df.sort_values(by="payer_count", ascending=True)
        
        st.subheader("Top Payers")
        fig_payers = px.bar(payers_df, x="payer_count", y="payer", title="Top Payers", labels={"payer": "Payer", "payer_count": "Payer Count"}, orientation="h", text="payer_count")
        fig_payers.update_traces(textposition="inside")
        st.plotly_chart(fig_payers)


#     # EMEA Distribution Pie Chart
    emea_df, error = fetch_emea_distribution()
    if error:
        st.error(f"Error fetching EMEA data: {error}")
        return
    if not emea_df.empty:
        total_count = emea_df['count'].sum()
        emea_df['percentage'] = (emea_df['count'] / total_count) * 100
        emea_df['percentage'] = emea_df['percentage'].round(2)
        st.subheader("EMEA Contribution")
        fig_emea = px.pie(emea_df, names="EMEA", values="percentage", title="EMEA Contribution in Percentage", labels={"EMEA": "Region", "percentage": "Percentage"},)
        st.plotly_chart(fig_emea)

    
    # Priority Distribution Pie Chart
    priority_df, error = fetch_priority_distribution()
    if error:
        st.error(f"Error fetching priority data: {error}")
        return
    if not priority_df.empty:
        total_priority = priority_df['count'].sum()
        priority_df['percentage'] = (priority_df['count'] / total_priority) * 100
        priority_df['percentage'] = priority_df['percentage'].round(2)
        st.subheader("Priority Distribution")
        fig_priority = px.pie(priority_df, names="priority", values="percentage", title="Priority Distribution in Percentage", labels={"priority": "Priority Level", "percentage": "Percentage"})
        st.plotly_chart(fig_priority)
    
    # Top 5 Languages Table with Total Percentage
    language_df, error = fetch_top_languages()
    if error:
        st.error(f"Error fetching languages data: {error}")
        return
    if not language_df.empty:
        
        total_languages = language_df['count'].sum()
        language_df['percentage'] = (language_df['count'] / total_languages) * 100
        language_df['percentage'] = language_df['percentage'].round(2)
        total_percentage = language_df['percentage'].sum()
        language_df.loc[len(language_df)] = ["Total", total_languages, total_percentage]
        language_df.index = range(1, len(language_df) + 1)
        st.subheader("Top 5 language")
        st.subheader("Foreign Languages")
        st.write(language_df)

if __name__ == "__main__":
    admin_dashboard()