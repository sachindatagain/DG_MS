import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from page.db import get_connection

# Function to fetch data from the database
def fetch_data(query, start_date, end_date):
    connection = get_connection()
    if not connection:
        return None, "Failed to connect to the database."
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (start_date, end_date))
            result = cursor.fetchall()
        return pd.DataFrame(result), None
    except Exception as e:
        return None, str(e)

# SQL Queries with timestamp filtering
QUERIES = {
    "processing_tool_usage": """
        SELECT ocr, COUNT(*) AS user_count
        FROM admin_database
        WHERE ocr IS NOT NULL AND timestamp BETWEEN %s AND %s
        GROUP BY ocr
        ORDER BY user_count DESC;
    """,
    "top_payers": """
        SELECT payer, COUNT(*) AS payer_count
        FROM admin_database
        WHERE payer IS NOT NULL AND timestamp BETWEEN %s AND %s
        GROUP BY payer
        ORDER BY payer_count DESC
        LIMIT 20;
    """,
    "emea_distribution": """
        SELECT EMEA, COUNT(*) AS count
        FROM admin_database
        WHERE EMEA IS NOT NULL AND timestamp BETWEEN %s AND %s
        GROUP BY EMEA
        ORDER BY count DESC;
    """,
    "priority_distribution": """
        SELECT priority, COUNT(*) AS count
        FROM admin_database
        WHERE priority IS NOT NULL AND timestamp BETWEEN %s AND %s
        GROUP BY priority
        ORDER BY count DESC;
    """,
    "top_languages": """
        SELECT foreign_language AS language, COUNT(*) AS count
        FROM admin_database
        WHERE foreign_language IS NOT NULL AND timestamp BETWEEN %s AND %s
        GROUP BY foreign_language
        ORDER BY count DESC
        LIMIT 5;
    """
}

# Admin Dashboard
def admin_dashboard():
    st.title("Admin Dashboard")

    # Date Range Selector (Calendar Style)
    today = datetime.datetime.now()
    this_year = today.year
    jan_1 = datetime.date(2020, 1, 1)
    dec_31 = datetime.date(2028, 12, 31)

    date_range = st.date_input(
        "Enter Date Range",
        (jan_1, today.date()), # starting date
        jan_1,
        dec_31,
        format="MM.DD.YYYY",
    )

    # Ensure the user selects both dates in the range
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        st.warning("Please select a valid date range.")
        return  # Stop execution if invalid selection

    if start_date > end_date:
        st.error("Start date cannot be after end date.")
        return

    # Fetch and visualize data using the selected date range
    data_fetchers = {
        "OCR wise volume": ("processing_tool_usage", "ocr", "user_count"),
        "Top Payers": ("top_payers", "payer", "payer_count"),
        "EMEA Contribution": ("emea_distribution", "EMEA", "count"),
        "Priority Distribution": ("priority_distribution", "priority", "count"),
        "Top 5 Languages": ("top_languages", "language", "count"),
    }

    for section, (query_key, x_col, y_col) in data_fetchers.items():
        df, error = fetch_data(QUERIES[query_key], start_date, end_date)
        if error:
            st.error(f"Error fetching {section.lower()} data: {error}")
            continue
        
        if df.empty:
            continue  # Skip this section if no data is available

        st.subheader(section)

        if section == "Top Payers":
            df = df.sort_values(by=y_col, ascending=True)
            fig = px.bar(df, x=y_col, y=x_col, text=y_col, orientation="h", title=section)
            fig.update_traces(textposition="inside")
            st.plotly_chart(fig)
        elif section == "OCR wise volume":
            fig = px.bar(df, x=x_col, y=y_col, text=y_col, orientation="v", title=section)
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig)

        elif section in ["EMEA Contribution", "Priority Distribution"]:
            df["percentage"] = (df[y_col] / df[y_col].sum()) * 100
            fig = px.pie(df, names=x_col, values="percentage", title=f"{section} in Percentage")
            st.plotly_chart(fig)

        elif section == "Top 5 Languages":
            df["percentage"] = (df[y_col] / df[y_col].sum()) * 100
            df.loc[len(df)] = ["Total", df[y_col].sum(), df["percentage"].sum()]
            df.index = range(1, len(df) + 1)
            st.write(df)

if __name__ == "__main__":
    admin_dashboard()
