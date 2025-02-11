import streamlit as st
import pandas as pd
from page.db import get_connection

# Function to fetch unique values for a specific column
def fetch_unique_values(column_name):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = f"SELECT DISTINCT {column_name} FROM admin_service_ WHERE {column_name} IS NOT NULL"
        cursor.execute(query)
        results = cursor.fetchall()
        return [row[column_name] for row in results]
    except Exception as e:
        st.error(f"Error fetching unique values for {column_name}: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

# Function to fetch data based on dynamic filters
def fetch_data_by_filters(email_address=None, OCR=None, payers=None, start_date=None, end_date=None, bill_ref_code=None, track_id=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM admin_service_ WHERE 1=1"
    parameters = []
    
    if email_address:
        query += " AND email_address = %s"
        parameters.append(email_address)
    if OCR:
        query += " AND OCR IN (" + ",".join(["%s"] * len(OCR)) + ")"
        parameters.extend(OCR)
    if payers:
        query += " AND payer IN (" + ",".join(["%s"] * len(payers)) + ")"
        parameters.extend(payers)
    if start_date and end_date:
        query += " AND DATE(timestamp) BETWEEN %s AND %s"
        parameters.append(start_date.strftime('%Y-%m-%d'))
        parameters.append(end_date.strftime('%Y-%m-%d'))
    if bill_ref_code:
        query += " AND bill_ref_code = %s"
        parameters.append(bill_ref_code)
    if track_id:
        query += " AND track_id = %s"
        parameters.append(track_id)

    try:
        cursor.execute(query, tuple(parameters))
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching data with filters: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

# Export Data Page
def export_data_page():
    st.title("Search and Export Data")

    email_options = fetch_unique_values("email_address")
    OCR_options = fetch_unique_values("OCR")
    payer_options = fetch_unique_values("payer")
    bill_ref_code_options = fetch_unique_values("bill_ref_code")
    track_id_options = fetch_unique_values("track_id")

    email_address = st.selectbox("Enter Email Address", options=[""] + email_options)
    OCR = st.multiselect("Enter Processing Tools", options=OCR_options)
    payers = st.multiselect("Enter Payers", options=payer_options)
    bill_ref_code = st.selectbox("Enter Bill Reference Code", options=[""] + bill_ref_code_options)
    track_id = st.selectbox("Enter Track ID", options=[""] + track_id_options)

    start_date = st.date_input("Start Date", value=None)
    end_date = st.date_input("End Date", value=None)

    if st.button("Search and Export Data"):
        if not (email_address or OCR or payers or start_date or end_date or bill_ref_code or track_id):
            st.warning("Select any one of the sections to filter data.")
        else:
            data = fetch_data_by_filters(
                email_address=email_address if email_address else None,
                OCR=OCR if OCR else None,
                payers=payers if payers else None,
                start_date=start_date,
                end_date=end_date,
                bill_ref_code=bill_ref_code if bill_ref_code else None,
                track_id=track_id if track_id else None
            )
            if data:
                df = pd.DataFrame(data)
                df.index = range(1, len(df) + 1)  # Set index to start from 1
                st.write("Filter Data:", df)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Data",
                    data=csv,
                    file_name="user_data.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data found for the selected filters.")

if __name__ == "__main__":
    export_data_page()
