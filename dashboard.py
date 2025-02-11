#                                       without the date section

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from page.db import get_connection

# def fetch_processing_tool_usage(): 
#     connection = get_connection()
#     if not connection:
#         return None, "Failed to connect to the database."
#     try:
#         query = """
#             SELECT ocr, COUNT(*) AS user_count
#             FROM admin_database
#             WHERE ocr IS NOT NULL
#             GROUP BY ocr
#             ORDER BY user_count DESC;
#         """
#         with connection.cursor(dictionary=True) as cursor:
#             cursor.execute(query)
#             result = cursor.fetchall()
#         return pd.DataFrame(result), None
#     except Exception as e:
#         return None, str(e)

# def fetch_top_payers(): 
#     connection = get_connection()
#     if not connection:
#         return None, "Failed to connect to the database."
#     try:
#         query = """
#             SELECT payer, COUNT(*) AS payer_count
#             FROM admin_database
#             WHERE payer IS NOT NULL
#             GROUP BY payer
#             ORDER BY payer_count DESC
#             LIMIT 20;
#         """
#         with connection.cursor(dictionary=True) as cursor:
#             cursor.execute(query)
#             result = cursor.fetchall()
#         return pd.DataFrame(result), None
#     except Exception as e:
#         return None, str(e)
    
# def fetch_emea_distribution():
#     connection = get_connection()
#     if not connection:
#         return None, "Failed to connect to the database."
#     try:
#         query = """
#             SELECT EMEA, COUNT(*) AS count
#             FROM admin_database
#             WHERE EMEA IS NOT NULL
#             GROUP BY EMEA
#             ORDER BY count DESC;
#         """
#         with connection.cursor(dictionary=True) as cursor:
#             cursor.execute(query)
#             result = cursor.fetchall()
#         return pd.DataFrame(result), None
#     except Exception as e:
#         return None, str(e)

# def fetch_priority_distribution():
#     connection = get_connection()
#     if not connection:
#         return None, "Failed to connect to the database."
#     try:
#         query = """
#             SELECT priority, COUNT(*) AS count
#             FROM admin_database
#             WHERE priority IS NOT NULL
#             GROUP BY priority
#             ORDER BY count DESC;
#         """
#         with connection.cursor(dictionary=True) as cursor:
#             cursor.execute(query)
#             result = cursor.fetchall()
#         return pd.DataFrame(result), None
#     except Exception as e:
#         return None, str(e)

# def fetch_top_languages():
#     connection = get_connection()
#     if not connection:
#         return None, "Failed to connect to the database."
#     try:
#         query = """
#             SELECT foreign_language AS language, COUNT(*) AS count
#             FROM admin_database
#             WHERE foreign_language IS NOT NULL
#             GROUP BY foreign_language
#             ORDER BY count DESC
#             LIMIT 5;
#         """
#         with connection.cursor(dictionary=True) as cursor:
#             cursor.execute(query)
#             result = cursor.fetchall()
#         return pd.DataFrame(result), None
#     except Exception as e:
#         return None, str(e)

# def admin_dashboard():
#     st.title("Admin Dashboard")

#     # Processing Tool Usage
#     usage_df, error = fetch_processing_tool_usage()
#     if error:
#         st.error(f"Error fetching usage data: {error}")
#         return
#     if not usage_df.empty:
#         st.subheader("OCR wise volume")
#         fig_usage = px.bar(usage_df, x="ocr", y="user_count", title="Volume Count of OCR Tool", labels={"ocr": "OCR Tool", "user_count": "User Count"}, text="user_count")
#         fig_usage.update_traces(textposition="outside")
#         st.plotly_chart(fig_usage)
    
#     # Top 20 Payers Scatter Bar Chart
#     payers_df, error = fetch_top_payers()
#     if error:
#         st.error(f"Error fetching payers data: {error}")
#         return
#     if not payers_df.empty:
#         # Sort the DataFrame in ascending order of payer_count
#         payers_df = payers_df.sort_values(by="payer_count", ascending=True)
        
#         st.subheader("Top Payers")
#         fig_payers = px.bar(payers_df, x="payer_count", y="payer", title="Top Payers", labels={"payer": "Payer", "payer_count": "Payer Count"}, orientation="h", text="payer_count")
#         fig_payers.update_traces(textposition="inside")
#         st.plotly_chart(fig_payers)


# #     # EMEA Distribution Pie Chart
#     emea_df, error = fetch_emea_distribution()
#     if error:
#         st.error(f"Error fetching EMEA data: {error}")
#         return
#     if not emea_df.empty:
#         total_count = emea_df['count'].sum()
#         emea_df['percentage'] = (emea_df['count'] / total_count) * 100
#         emea_df['percentage'] = emea_df['percentage'].round(2)
#         st.subheader("EMEA Contribution")
#         fig_emea = px.pie(emea_df, names="EMEA", values="percentage", title="EMEA Contribution in Percentage", labels={"EMEA": "Region", "percentage": "Percentage"},)
#         st.plotly_chart(fig_emea)

    
#     # Priority Distribution Pie Chart
#     priority_df, error = fetch_priority_distribution()
#     if error:
#         st.error(f"Error fetching priority data: {error}")
#         return
#     if not priority_df.empty:
#         total_priority = priority_df['count'].sum()
#         priority_df['percentage'] = (priority_df['count'] / total_priority) * 100
#         priority_df['percentage'] = priority_df['percentage'].round(2)
#         st.subheader("Priority Distribution")
#         fig_priority = px.pie(priority_df, names="priority", values="percentage", title="Priority Distribution in Percentage", labels={"priority": "Priority Level", "percentage": "Percentage"})
#         st.plotly_chart(fig_priority)
    
#     # Top 5 Languages Table with Total Percentage
#     language_df, error = fetch_top_languages()
#     if error:
#         st.error(f"Error fetching languages data: {error}")
#         return
#     if not language_df.empty:
        
#         total_languages = language_df['count'].sum()
#         language_df['percentage'] = (language_df['count'] / total_languages) * 100
#         language_df['percentage'] = language_df['percentage'].round(2)
#         total_percentage = language_df['percentage'].sum()
#         language_df.loc[len(language_df)] = ["Total", total_languages, total_percentage]
#         language_df.index = range(1, len(language_df) + 1)
#         st.subheader("Top 5 language")
#         st.subheader("Foreign Languages")
#         st.write(language_df)

# if __name__ == "__main__":
#     admin_dashboard()

#----------------------------------------------------------------------------------------------------------------
#                                                     date updated code for dashboard 
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from page.db import get_connection

# def fetch_processing_tool_usage(start_date, end_date): 
#     connection = get_connection()
#     if not connection:
#         return None, "Failed to connect to the database."
#     try:
#         query = """
#             SELECT ocr, COUNT(*) AS user_count
#             FROM admin_database
#             WHERE ocr IS NOT NULL AND timestamp BETWEEN %s AND %s
#             GROUP BY ocr
#             ORDER BY user_count DESC;
#         """
#         with connection.cursor(dictionary=True) as cursor:
#             cursor.execute(query, (start_date, end_date))
#             result = cursor.fetchall()
#         return pd.DataFrame(result), None
#     except Exception as e:
#         return None, str(e)

# def fetch_top_payers(start_date, end_date): 
#     connection = get_connection()
#     if not connection:
#         return None, "Failed to connect to the database."
#     try:
#         query = """
#             SELECT payer, COUNT(*) AS payer_count
#             FROM admin_database
#             WHERE payer IS NOT NULL AND timestamp BETWEEN %s AND %s
#             GROUP BY payer
#             ORDER BY payer_count DESC
#             LIMIT 20;
#         """
#         with connection.cursor(dictionary=True) as cursor:
#             cursor.execute(query, (start_date, end_date))
#             result = cursor.fetchall()
#         return pd.DataFrame(result), None
#     except Exception as e:
#         return None, str(e)
    
# def fetch_emea_distribution(start_date, end_date):
#     connection = get_connection()
#     if not connection:
#         return None, "Failed to connect to the database."
#     try:
#         query = """
#             SELECT EMEA, COUNT(*) AS count
#             FROM admin_database
#             WHERE EMEA IS NOT NULL AND timestamp BETWEEN %s AND %s
#             GROUP BY EMEA
#             ORDER BY count DESC;
#         """
#         with connection.cursor(dictionary=True) as cursor:
#             cursor.execute(query, (start_date, end_date))
#             result = cursor.fetchall()
#         return pd.DataFrame(result), None
#     except Exception as e:
#         return None, str(e)

# def fetch_priority_distribution(start_date, end_date):
#     connection = get_connection()
#     if not connection:
#         return None, "Failed to connect to the database."
#     try:
#         query = """
#             SELECT priority, COUNT(*) AS count
#             FROM admin_database
#             WHERE priority IS NOT NULL AND timestamp BETWEEN %s AND %s
#             GROUP BY priority
#             ORDER BY count DESC;
#         """
#         with connection.cursor(dictionary=True) as cursor:
#             cursor.execute(query, (start_date, end_date))
#             result = cursor.fetchall()
#         return pd.DataFrame(result), None
#     except Exception as e:
#         return None, str(e)

# def fetch_top_languages(start_date, end_date):
#     connection = get_connection()
#     if not connection:
#         return None, "Failed to connect to the database."
#     try:
#         query = """
#             SELECT foreign_language AS language, COUNT(*) AS count
#             FROM admin_database
#             WHERE foreign_language IS NOT NULL AND timestamp BETWEEN %s AND %s
#             GROUP BY foreign_language
#             ORDER BY count DESC
#             LIMIT 5;
#         """
#         with connection.cursor(dictionary=True) as cursor:
#             cursor.execute(query, (start_date, end_date))
#             result = cursor.fetchall()
#         return pd.DataFrame(result), None
#     except Exception as e:
#         return None, str(e)

# def admin_dashboard():
#     st.title("Admin Dashboard")

#     # Date Range Input
#     start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
#     end_date = st.date_input("End Date", pd.to_datetime("2025-01-01"))
    
#     if start_date > end_date:
#         st.error("Start date cannot be after end date.")
#         return

#     # Processing Tool Usage
#     usage_df, error = fetch_processing_tool_usage(start_date, end_date)
#     if error:
#         st.error(f"Error fetching usage data: {error}")
#         return
#     if not usage_df.empty:
#         st.subheader("OCR wise volume")
#         fig_usage = px.bar(usage_df, x="ocr", y="user_count", title="Volume Count of OCR Tool", labels={"ocr": "OCR Tool", "user_count": "User Count"}, text="user_count")
#         fig_usage.update_traces(textposition="outside")
#         st.plotly_chart(fig_usage)
    
#     # Top 20 Payers Scatter Bar Chart
#     payers_df, error = fetch_top_payers(start_date, end_date)
#     if error:
#         st.error(f"Error fetching payers data: {error}")
#         return
#     if not payers_df.empty:
#         # Sort the DataFrame in ascending order of payer_count
#         payers_df = payers_df.sort_values(by="payer_count", ascending=True)
        
#         st.subheader("Top Payers")
#         fig_payers = px.bar(payers_df, x="payer_count", y="payer", title="Top Payers", labels={"payer": "Payer", "payer_count": "Payer Count"}, orientation="h", text="payer_count")
#         fig_payers.update_traces(textposition="inside")
#         st.plotly_chart(fig_payers)

#     # EMEA Distribution Pie Chart
#     emea_df, error = fetch_emea_distribution(start_date, end_date)
#     if error:
#         st.error(f"Error fetching EMEA data: {error}")
#         return
#     if not emea_df.empty:
#         total_count = emea_df['count'].sum()
#         emea_df['percentage'] = (emea_df['count'] / total_count) * 100
#         emea_df['percentage'] = emea_df['percentage'].round(2)
#         st.subheader("EMEA Contribution")
#         fig_emea = px.pie(emea_df, names="EMEA", values="percentage", title="EMEA Contribution in Percentage", labels={"EMEA": "Region", "percentage": "Percentage"})
#         st.plotly_chart(fig_emea)

#     # Priority Distribution Pie Chart
#     priority_df, error = fetch_priority_distribution(start_date, end_date)
#     if error:
#         st.error(f"Error fetching priority data: {error}")
#         return
#     if not priority_df.empty:
#         total_priority = priority_df['count'].sum()
#         priority_df['percentage'] = (priority_df['count'] / total_priority) * 100
#         priority_df['percentage'] = priority_df['percentage'].round(2)
#         st.subheader("Priority Distribution")
#         fig_priority = px.pie(priority_df, names="priority", values="percentage", title="Priority Distribution in Percentage", labels={"priority": "Priority Level", "percentage": "Percentage"})
#         st.plotly_chart(fig_priority)
    
#     # Top 5 Languages Table with Total Percentage
#     language_df, error = fetch_top_languages(start_date, end_date)
#     if error:
#         st.error(f"Error fetching languages data: {error}")
#         return
#     if not language_df.empty:
#         total_languages = language_df['count'].sum()
#         language_df['percentage'] = (language_df['count'] / total_languages) * 100
#         language_df['percentage'] = language_df['percentage'].round(2)
#         total_percentage = language_df['percentage'].sum()
#         language_df.loc[len(language_df)] = ["Total", total_languages, total_percentage]
#         language_df.index = range(1, len(language_df) + 1)
#         st.subheader("Top 5 Language")
#         st.write(language_df)

# if __name__ == "__main__":
#     admin_dashboard()

#---------------------------------------------------------------------------------------------------------
#                                                  updated code on date format
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from page.db import get_connection

# # Function to fetch data from the database
# def fetch_data(query, start_date, end_date):
#     connection = get_connection()
#     if not connection:
#         return None, "Failed to connect to the database."
#     try:
#         with connection.cursor(dictionary=True) as cursor:
#             cursor.execute(query, (start_date, end_date))
#             result = cursor.fetchall()
#         return pd.DataFrame(result), None
#     except Exception as e:
#         return None, str(e)

# # SQL Queries with timestamp filtering
# QUERIES = {
#     "processing_tool_usage": """
#         SELECT ocr, COUNT(*) AS user_count
#         FROM admin_database
#         WHERE ocr IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY ocr
#         ORDER BY user_count DESC;
#     """,
#     "top_payers": """
#         SELECT payer, COUNT(*) AS payer_count
#         FROM admin_database
#         WHERE payer IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY payer
#         ORDER BY payer_count DESC
#         LIMIT 20;
#     """,
#     "emea_distribution": """
#         SELECT EMEA, COUNT(*) AS count
#         FROM admin_database
#         WHERE EMEA IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY EMEA
#         ORDER BY count DESC;
#     """,
#     "priority_distribution": """
#         SELECT priority, COUNT(*) AS count
#         FROM admin_database
#         WHERE priority IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY priority
#         ORDER BY count DESC;
#     """,
#     "top_languages": """
#         SELECT foreign_language AS language, COUNT(*) AS count
#         FROM admin_database
#         WHERE foreign_language IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY foreign_language
#         ORDER BY count DESC
#         LIMIT 5;
#     """
# }

# # Admin Dashboard
# def admin_dashboard():
#     st.title("Admin Dashboard")

#     # Single Date Range Selector for all charts
#     st.header("Filter Charts according to the Date")
#     start_date = st.date_input("Start Date", value=None)
#     end_date = st.date_input("End Date", value=None)

    
#     if start_date is not None and end_date is not None:
#         if start_date > end_date:
#             st.error("Start date cannot be after end date.")
#             return
#         else:
#             st.warning("Please select both Start Date and End Date.")
#             return  # Stop further execution until dates are selected


#     # Fetch and visualize data using the same date range
#     data_fetchers = {
#         "OCR wise volume": ("processing_tool_usage", "ocr", "user_count"),
#         "Top Payers": ("top_payers", "payer", "payer_count"),
#         "EMEA Contribution": ("emea_distribution", "EMEA", "count"),
#         "Priority Distribution": ("priority_distribution", "priority", "count"),
#         "Top 5 Languages": ("top_languages", "language", "count"),
#     }

#     for section, (query_key, x_col, y_col) in data_fetchers.items():
#         df, error = fetch_data(QUERIES[query_key], start_date, end_date)
#         if error:
#             st.error(f"Error fetching {section.lower()} data: {error}")
#             continue
        
#         if df.empty:
#             st.warning(f"No data available for {section}.")
#             continue

#         st.subheader(section)

#         if section == "Top Payers":
#             df = df.sort_values(by=y_col, ascending=True)  # Sorting in ascending order for correct horizontal bar display
#             fig = px.bar(df, x=y_col, y=x_col, text=y_col, orientation="h", title=section)
#             fig.update_traces(textposition="inside")
#             st.plotly_chart(fig)
#         elif section == "OCR wise volume":
#             fig = px.bar(df, x=x_col, y=y_col, text=y_col, orientation="v", title=section)
#             fig.update_traces(textposition="outside")
#             st.plotly_chart(fig)

#         elif section in ["EMEA Contribution", "Priority Distribution"]:
#             df["percentage"] = (df[y_col] / df[y_col].sum()) * 100
#             fig = px.pie(df, names=x_col, values="percentage", title=f"{section} in Percentage",)
#             st.plotly_chart(fig)

#         elif section == "Top 5 Languages":
#             df["percentage"] = (df[y_col] / df[y_col].sum()) * 100
#             df.loc[len(df)] = ["Total", df[y_col].sum(), df["percentage"].sum()]
#             df.index = range(1, len(df) + 1)
#             st.write(df)

# if __name__ == "__main__":
#     admin_dashboard()

#-------------------------------------------------------------------------------------------------------------
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from page.db import get_connection

# # Function to fetch data from the database
# def fetch_data(query, start_date, end_date):
#     connection = get_connection()
#     if not connection:
#         return None, "Failed to connect to the database."
#     try:
#         with connection.cursor(dictionary=True) as cursor:
#             cursor.execute(query, (start_date, end_date))
#             result = cursor.fetchall()
#         return pd.DataFrame(result), None
#     except Exception as e:
#         return None, str(e)

# # SQL Queries with timestamp filtering
# QUERIES = {
#     "processing_tool_usage": """
#         SELECT ocr, COUNT(*) AS user_count
#         FROM admin_database
#         WHERE ocr IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY ocr
#         ORDER BY user_count DESC;
#     """,
#     "top_payers": """
#         SELECT payer, COUNT(*) AS payer_count
#         FROM admin_database
#         WHERE payer IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY payer
#         ORDER BY payer_count DESC
#         LIMIT 20;
#     """,
#     "emea_distribution": """
#         SELECT EMEA, COUNT(*) AS count
#         FROM admin_database
#         WHERE EMEA IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY EMEA
#         ORDER BY count DESC;
#     """,
#     "priority_distribution": """
#         SELECT priority, COUNT(*) AS count
#         FROM admin_database
#         WHERE priority IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY priority
#         ORDER BY count DESC;
#     """,
#     "top_languages": """
#         SELECT foreign_language AS language, COUNT(*) AS count
#         FROM admin_database
#         WHERE foreign_language IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY foreign_language
#         ORDER BY count DESC
#         LIMIT 5;
#     """
# }

# # Admin Dashboard
# def admin_dashboard():
#     st.title("Admin Dashboard")

#     # Single Date Range Selector for all charts
#     st.header("Filter Charts according to the Date")
#     start_date = st.date_input("Start Date", value=None)
#     end_date = st.date_input("End Date", value=None)

#     # Ensure both dates are selected
#     if start_date is None or end_date is None:
#         return  # Stop execution if dates are missing

#     if start_date > end_date:
#         st.error("Start date cannot be after end date.")
#         return

#     # Fetch and visualize data using the same date range
#     data_fetchers = {
#         "OCR wise volume": ("processing_tool_usage", "ocr", "user_count"),
#         "Top Payers": ("top_payers", "payer", "payer_count"),
#         "EMEA Contribution": ("emea_distribution", "EMEA", "count"),
#         "Priority Distribution": ("priority_distribution", "priority", "count"),
#         "Top 5 Languages": ("top_languages", "language", "count"),
#     }

#     for section, (query_key, x_col, y_col) in data_fetchers.items():
#         df, error = fetch_data(QUERIES[query_key], start_date, end_date)
#         if error:
#             st.error(f"Error fetching {section.lower()} data: {error}")
#             continue
        
#         if df.empty:
#             continue  # Skip this section if no data is available

#         st.subheader(section)

#         if section == "Top Payers":
#             df = df.sort_values(by=y_col, ascending=True)  # Sorting in ascending order for correct horizontal bar display
#             fig = px.bar(df, x=y_col, y=x_col, text=y_col, orientation="h", title=section)
#             fig.update_traces(textposition="inside")
#             st.plotly_chart(fig)
#         elif section == "OCR wise volume":
#             fig = px.bar(df, x=x_col, y=y_col, text=y_col, orientation="v", title=section)
#             fig.update_traces(textposition="outside")
#             st.plotly_chart(fig)

#         elif section in ["EMEA Contribution", "Priority Distribution"]:
#             df["percentage"] = (df[y_col] / df[y_col].sum()) * 100
#             fig = px.pie(df, names=x_col, values="percentage", title=f"{section} in Percentage")
#             st.plotly_chart(fig)

#         elif section == "Top 5 Languages":
#             df["percentage"] = (df[y_col] / df[y_col].sum()) * 100
#             df.loc[len(df)] = ["Total", df[y_col].sum(), df["percentage"].sum()]
#             df.index = range(1, len(df) + 1)
#             st.write(df)

# if __name__ == "__main__":
#     admin_dashboard()

#------------------------------------------------------------------------------------------------------------
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
