import streamlit as st
import pandas as pd
from io import BytesIO
from page.db import get_connection

# Predefined required columns
REQUIRED_COLUMNS = [
    "Timestamp", "Email Address", "OCR", "Bill Ref Code", "Track ID", "Annotation ID", "Document Type",
    "Matched Payee ID", "Payer", "Review", "Bill Lines", "Payee Name", "Invoice", "Invoice Date",
    "Invoice Due Date", "Terms", "PO", "Tax Amt", "Total Amt", "Currency", "Foreign Language",
    "Quality Analyst", "Invoice Pages", "Multiple Payees", "Comments", "PST to IST", "US Date",
    "IND Date", "IND Time", "Team", "Agent", "Unique ID", "Priority", "Month", "Hour", "EMEA"
]

# Function to check if a table exists
def table_exists(connection, table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        return cursor.fetchone() is not None

# Function to clean column names
def clean_column_names(columns):
    return [col.strip().replace("\xa0", " ") for col in columns]  # Removes extra spaces & non-breaking spaces

# Function to create table
def create_table_from_df(connection, df, table_name):
    df.columns = clean_column_names(df.columns)
    columns = ", ".join([f"`{col}` LONGTEXT" for col in df.columns])
    create_query = f"CREATE TABLE `{table_name}` ({columns})"
    
    with connection.cursor() as cursor:
        cursor.execute(create_query)
        connection.commit()
    insert_data_in_batches(connection, df, table_name)
    st.success("data uploaded successfully.")

# Function to insert unique data
def insert_unique_data(connection, df, table_name):
    df.columns = clean_column_names(df.columns)

    # Fixing "Unique ID" as the primary key for uniqueness check
    primary_key_col = "Unique ID"
    
    if primary_key_col not in df.columns:
        st.error(f"Missing primary key column: {primary_key_col}")
        return

    # Normalize data for comparison
    df[primary_key_col] = df[primary_key_col].astype(str).str.strip().str.lower()
    df.drop_duplicates(subset=[primary_key_col], inplace=True)  # Remove duplicates within the CSV

    # Fetch existing records from database
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT `{primary_key_col}` FROM `{table_name}`")
        existing_records = {str(row[0]).strip().lower() for row in cursor.fetchall()}  # Normalize DB records

    st.write(f"Total existing records in DB: {len(existing_records)}")  # Debugging

    # Identify truly new records
    new_records = df[~df[primary_key_col].isin(existing_records)]
    
    st.write(f"New unique records to insert: {len(new_records)}")  # Debugging

    if new_records.empty:
        st.warning("records not inserted.")
        return

    insert_data_in_batches(connection, new_records, table_name)
    st.success("Unique data uploaded.")

# Function to insert data in batches
def insert_data_in_batches(connection, df, table_name, batch_size=2000):
    insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(df.columns))})"
    
    with connection.cursor() as cursor:
        for i in range(0, len(df), batch_size):
            batch_data = [tuple(row.where(pd.notna(row), None)) for _, row in df.iloc[i:i + batch_size].iterrows()]
            cursor.executemany(insert_query, batch_data)
            connection.commit()

# Function to generate and download CSV template
def generate_csv_template():
    df_template = pd.DataFrame(columns=REQUIRED_COLUMNS)
    buffer = BytesIO()
    df_template.to_csv(buffer, index=False, encoding="utf-8-sig")
    buffer.seek(0)
    return buffer

# Import CSV Page
def import_csv_page():
    st.title("Import Page")
    
    # Provide CSV download button
    st.download_button(
        label="Download CSV Template",
        data=generate_csv_template(),
        file_name="managed_services.csv",
        mime="text/csv"
    )
    
    uploaded_file = st.file_uploader("Choose a file to upload", type=["csv","xlsx","json"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
            df.columns = clean_column_names(df.columns)
            df.index = range(1, len(df) + 1)
            
            missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            if missing_columns:
                st.error(f"Invalid file: Missing required columns - {', '.join(missing_columns)}")
                return
            st.write(f"Total records : {len(df)}")  # Display total records            
            st.success("file loaded successfully!")
            st.dataframe(df)
            
            if st.button("Upload Data"):
                connection = get_connection()
                if connection:
                    table_name = uploaded_file.name.split('.')[0]
                    if table_exists(connection, table_name):
                        insert_unique_data(connection, df, table_name)
                    else:
                        create_table_from_df(connection, df, table_name)
                    connection.close()
                else:
                    st.error("Could not connect to the database.")
        except Exception as e:
            st.error(f"Error loading : {e}")
    else:
        st.warning("Please upload a file.")

if __name__ == "__main__":
    import_csv_page()


# # Function to insert data in batches
# def insert_data_in_batches(connection, df, table_name, batch_size=2000):
#     insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(df.columns))})"
    
#     with connection.cursor() as cursor:
#         for i in range(0, len(df), batch_size):
#             batch_data = [tuple(row.where(pd.notna(row), None)) for _, row in df.iloc[i:i + batch_size].iterrows()]
#             cursor.executemany(insert_query, batch_data)
#             connection.commit()
    
# # Import CSV Page
# def import_csv_page():
#     st.title("Import CSV Page")
#     uploaded_file = st.file_uploader("Choose a CSV file to upload", type=["csv"])
    
#     if uploaded_file is not None:
#         try:
#             df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
#             df.columns = clean_column_names(df.columns)
#             df.index = range(1, len(df) + 1)
            
#             missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
#             if missing_columns:
#                 st.error(f"Invalid file: Missing required columns - {', '.join(missing_columns)}")
#                 return
            
#             st.success("CSV file loaded successfully!")
#             st.dataframe(df)
            
#             if st.button("Upload Data"):
#                 connection = get_connection()
#                 if connection:
#                     table_name = uploaded_file.name.split('.')[0]
#                     if table_exists(connection, table_name):
#                         insert_unique_data(connection, df, table_name)
#                     else:
#                         create_table_from_df(connection, df, table_name)
#                     connection.close()
#                 else:
#                     st.error("Could not connect to the database.")
#         except Exception as e:
#             st.error(f"Error loading CSV: {e}")
#     else:
#         st.warning("Please upload a CSV file.")

# if __name__ == "__main__":
#     import_csv_page()
