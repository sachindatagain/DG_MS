import streamlit as st
import pandas as pd
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
    st.success("Table created and data uploaded successfully.")

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
        st.warning("No unique records to insert.")
        return

    insert_data_in_batches(connection, new_records, table_name)
    st.success("Unique data uploaded successfully.")




# Function to insert data in batches
def insert_data_in_batches(connection, df, table_name, batch_size=2000):
    insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(df.columns))})"
    
    with connection.cursor() as cursor:
        for i in range(0, len(df), batch_size):
            batch_data = [tuple(row.where(pd.notna(row), None)) for _, row in df.iloc[i:i + batch_size].iterrows()]
            cursor.executemany(insert_query, batch_data)
            connection.commit()

# Import CSV Page
def import_csv_page():
    st.title("Import CSV Page")
    uploaded_file = st.file_uploader("Choose a CSV file to upload", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
            df.columns = clean_column_names(df.columns)
            df.index = range(1, len(df) + 1)
            
            missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            if missing_columns:
                st.error(f"Invalid file: Missing required columns - {', '.join(missing_columns)}")
                return
            
            st.success("CSV file loaded successfully!")
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
            st.error(f"Error loading CSV: {e}")
    else:
        st.warning("Please upload a CSV file.")

if __name__ == "__main__":
    import_csv_page()




###################################################################################
# import streamlit as st
# import pandas as pd
# from page.db import get_connection

# # Predefined required columns
# REQUIRED_COLUMNS = [
#     "Timestamp", "Email Address", "OCR", "Bill Ref Code", "Track ID", "Annotation ID", "Document Type",
#     "Matched Payee ID", "Payer", "Review", "Bill Lines", "Payee Name", "Invoice", "Invoice Date",
#     "Invoice Due Date", "Terms", "PO", "Tax Amt", "Total Amt", "Currency", "Foreign Language",
#     "Quality Analyst", "Invoice Pages", "Multiple Payees", "Comments", "PST to IST", "US Date",
#     "IND Date", "IND Time", "Team", "Agent", "Unique ID", "Priority", "Month", "Hour", "EMEA"
# ]

# # Function to check if a table exists in the database
# def table_exists(connection, table_name):
#     cursor = connection.cursor()
#     cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
#     result = cursor.fetchone()
#     cursor.close()
#     return result is not None

# # Function to clean column names
# def clean_column_names(columns):
#     return [col.strip().replace("\xa0", " ") for col in columns]  # Removes leading/trailing spaces & non-breaking spaces

# # Function to create table from dataframe
# def create_table_from_df(connection, df, table_name):
#     cursor = connection.cursor()
#     df.columns = clean_column_names(df.columns)

#     # Create table with LONGTEXT columns
#     columns = ", ".join([f"`{col}` LONGTEXT" for col in df.columns])
#     create_table_query = f"CREATE TABLE `{table_name}` ({columns})"
#     cursor.execute(create_table_query)
#     connection.commit()

#     # Insert data in batches of 10000 rows
#     insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(df.columns))})"
    
#     batch_size = 10000
#     for i in range(0, len(df), batch_size):
#         batch_data = [tuple(row.where(pd.notna(row), None)) for _, row in df.iloc[i:i + batch_size].iterrows()]
#         cursor.executemany(insert_query, batch_data)
#         connection.commit()

#     cursor.close()
#     st.success("Data uploaded successfully.")

# # Function to insert unique data into existing table
# def insert_unique_data(connection, df, table_name):
#     cursor = connection.cursor()
#     df.columns = clean_column_names(df.columns)

#     batch_size = 10000
#     records_inserted = False

#     for i in range(0, len(df), batch_size):
#         batch_data = []
#         for _, row in df.iloc[i:i + batch_size].iterrows():
#             row = row.where(pd.notna(row), None)
#             check_query = f"SELECT 1 FROM `{table_name}` WHERE `{df.columns[0]}` = %s LIMIT 1"
#             cursor.execute(check_query, (row[0],))
#             if cursor.fetchone() is None:
#                 batch_data.append(tuple(row))

#         if batch_data:
#             insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(df.columns))})"
#             cursor.executemany(insert_query, batch_data)
#             connection.commit()
#             records_inserted = True

#     cursor.close()
#     if records_inserted:
#         st.success("Unique data uploaded successfully.")
#     else:
#         st.warning("No unique records inserted.")

# # Import CSV page function
# def import_csv_page():
#     st.title("Import CSV Page")
#     uploaded_file = st.file_uploader("Choose a CSV file to upload", type=["csv"])

#     if uploaded_file is not None:
#         try:
#             df = pd.read_csv(uploaded_file, encoding="utf-8-sig")  # Handles BOM issues
#             df.index = range(1, len(df) + 1)
#             df.columns = clean_column_names(df.columns)  # Clean column names
            
#             # Check missing columns
#             missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
#             if missing_columns:
#                 st.error(f"Invalid file: Missing required columns - {', '.join(missing_columns)}")
#                 return  # Stop execution immediately
            
#             st.success("CSV file loaded successfully!")
#             st.dataframe(df)  # Display DataFrame
            
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
#             st.error(f"An error occurred while loading the CSV file: {e}")
#     else:
#         st.warning("Please upload a CSV file.")


























# import streamlit as st
# import pandas as pd
# from page.db import get_connection

# # Function to check if a table exists in the database
# def table_exists(connection, table_name):
#     cursor = connection.cursor()
#     cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
#     result = cursor.fetchone()
#     cursor.close()
#     return result is not None

# # Function to clean and ensure unique column names
# def clean_column_names(columns):
#     cleaned_columns = []
#     seen = set()

#     for i, col in enumerate(columns):
#         col = f"column_{i}" if pd.isna(col) or col.strip() == "" else col.replace(" ", "_")

#         # Ensure unique column names
#         original_col = col
#         counter = 1
#         while col in seen:
#             col = f"{original_col}_{counter}"
#             counter += 1
#         seen.add(col)
#         cleaned_columns.append(col)

#     return cleaned_columns

# # Function to create table from dataframe
# def create_table_from_df(connection, df, table_name):
#     cursor = connection.cursor()
#     df.columns = clean_column_names(df.columns)

#     # Create table with LONGTEXT columns
#     columns = ", ".join([f"`{col}` LONGTEXT" for col in df.columns])
#     create_table_query = f"CREATE TABLE `{table_name}` ({columns})"
#     cursor.execute(create_table_query)
#     connection.commit()

#     # Insert data in batches of 5000 rows
#     insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(df.columns))})"
    
#     batch_size = 10000 # 5000
#     for i in range(0, len(df), batch_size):
#         batch_data = [tuple(row.where(pd.notna(row), None)) for _, row in df.iloc[i:i + batch_size].iterrows()]
#         ''' 
#         First batch: i = 0 → i+5000 = 5000
#         Second batch: i = 5000 → i+5000 = 10000
#         Loop ends when i >= len(df) (no more records left).
#         This means no extra memory is needed to remember batch numbers—Python just calculates the next range automatically.
#         '''
#         cursor.executemany(insert_query, batch_data)
#         connection.commit()

#     cursor.close()
#     st.success("Data uploaded successfully.")

# # Function to insert unique data into existing table
# def insert_unique_data(connection, df, table_name):
#     cursor = connection.cursor()
#     df.columns = clean_column_names(df.columns)

#     # Insert only if primary column value doesn't exist
#     batch_size = 5000
#     records_inserted = False

#     for i in range(0, len(df), batch_size):
#         batch_data = []
#         for _, row in df.iloc[i:i + batch_size].iterrows():
#             row = row.where(pd.notna(row), None)
#             check_query = f"SELECT 1 FROM `{table_name}` WHERE `{df.columns[0]}` = %s LIMIT 1"
#             cursor.execute(check_query, (row[0],))
#             if cursor.fetchone() is None:
#                 batch_data.append(tuple(row))

#         if batch_data:
#             insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(df.columns))})"
#             cursor.executemany(insert_query, batch_data) # by this process it sends all the 5000 records in one go
#             connection.commit()
#             records_inserted = True

#     cursor.close()
#     if records_inserted:
#         st.success("Unique data uploaded successfully.")
#     else:
#         st.warning("No unique records inserted.")

# # Import CSV page function
# def import_csv_page():
#     st.title("Import CSV Page")
#     uploaded_file = st.file_uploader("Choose a CSV file to upload", type=["csv"])

#     if uploaded_file is not None:
#         try:
#             df = pd.read_csv(uploaded_file)
#             df.index = range(1, len(df) + 1)  # Start index from 1
#             st.success("CSV file loaded successfully!")
#             st.dataframe(df)  # Display DataFrame
            
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
#             st.error(f"An error occurred while loading the CSV file: {e}")
#     else:
#         st.warning("Please upload a CSV file.")



#-----------------------------------------------------------------------------------------------------------------------------
# import streamlit as st
# import pandas as pd
# from page.db import get_connection

# # Function to check if a table exists in the database
# def table_exists(connection, table_name):
#     cursor = connection.cursor()
#     cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
#     result = cursor.fetchone()
#     cursor.close()
#     return result is not None

# # Function to clean and ensure unique column names
# def clean_column_names(columns):
#     cleaned_columns = []
#     seen = set()

#     for i, col in enumerate(columns):
#         if pd.isna(col) or col.strip() == "":
#             col = f"column_{i}"  # Assign a default name
#         else:
#             col = col.replace(" ", "_")  # Replace spaces with underscores

#         original_col = col
#         counter = 1
#         while col in seen:
#             col = f"{original_col}_{counter}"
#             counter += 1
#         seen.add(col)
#         cleaned_columns.append(col)

#     return cleaned_columns

# # Function to create table from dataframe
# def create_table_from_df(connection, df, table_name):
#     cursor = connection.cursor()
#     df.columns = clean_column_names(df.columns)

#     columns = ", ".join([f"`{col}` longtext" for col in df.columns])
#     create_table_query = f"CREATE TABLE `{table_name}` ({columns})"
#     cursor.execute(create_table_query)
#     connection.commit()

#     insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(df.columns))})"

#     for _, row in df.iterrows():
#         row = row.where(pd.notna(row), None)
#         row = row.replace("", None)
#         cursor.execute(insert_query, tuple(row))

#     connection.commit()
#     cursor.close()
#     st.success("Data uploaded successfully.")

# # Function to insert unique data into existing table
# def insert_unique_data(connection, df, table_name):
#     cursor = connection.cursor()
#     records_inserted = False
#     df.columns = clean_column_names(df.columns)

#     for _, row in df.iterrows():
#         row = row.where(pd.notna(row), None)
#         row = row.replace("", None)
        
#         check_query = f"SELECT 1 FROM `{table_name}` WHERE `{df.columns[0]}` = %s LIMIT 1"
#         cursor.execute(check_query, (row[0],))
#         result = cursor.fetchone()

#         if result is None:
#             insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(df.columns))})"
#             cursor.execute(insert_query, tuple(row))
#             records_inserted = True

#     connection.commit()
#     cursor.close()
    
#     if records_inserted:
#         st.success("Unique data uploaded successfully.")
#     else:
#         st.warning("No unique records are inserted.")

# # Import CSV page function
# def import_csv_page():
#     st.title("Import CSV Page")
#     uploaded_file = st.file_uploader("Choose a CSV file to upload", type=["csv"])

#     if uploaded_file is not None:
#         try:
#             df = pd.read_csv(uploaded_file)
#             df.index = range(1, len(df) + 1)  # Start index from 1
#             st.success("CSV file loaded successfully!")
            
#             st.dataframe(df)  # Display DataFrame with index starting from 1
            
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
#             st.error(f"An error occurred while loading the CSV file: {e}")
#     else:
#         st.warning("Please upload a CSV file.")
