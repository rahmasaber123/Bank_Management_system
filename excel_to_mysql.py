import pandas as pd
import mysql.connector
import streamlit as st

st.title(" Excel/CSV to MySQL Importer")

# Config inputs
st.header(" MySQL Configuration")
host = st.text_input("Host", "localhost")
user = st.text_input("User", "root")
password = st.text_input("Password", type="password")
database = st.text_input("Database")
table_name = st.text_input("Target Table")

# File upload
st.header("Upload File")
uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file and st.button("Upload to MySQL"):
    try:
        # Read file
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            df = pd.read_csv(uploaded_file)

        st.write(f"Loaded {len(df)} rows with columns: {list(df.columns)}")
        st.dataframe(df.head())

        # Connect to MySQL
        conn = mysql.connector.connect(
            host=host, user=user, password=password, database=database)
        cursor = conn.cursor()

        # Prepare insert query dynamically
        cols = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        update_stmt = ", ".join([f"{col}=VALUES({col})" for col in df.columns])

        insert_sql = f"""
        INSERT INTO {table_name} ({cols})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE {update_stmt}
        """

        records = df.values.tolist()
        cursor.executemany(insert_sql, records)
        conn.commit()

        st.success(f"Inserted/Updated {cursor.rowcount} rows into {table_name} ")

        cursor.close()
        conn.close()

    except Exception as e:
        st.error(f" Error: {e}")
