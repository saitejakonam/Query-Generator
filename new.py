import streamlit as st
import sqlite3
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv() 

# Configure Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to convert an Excel sheet to SQLite database
def excel_to_sqlite(excel_file, db_path):
    conn = sqlite3.connect(db_path)
    excel_data = pd.read_excel(excel_file, sheet_name=None)  # Load all sheets
    for sheet_name, df in excel_data.items():
        # Write each sheet to SQLite
        df.to_sql(sheet_name, conn, index=False, if_exists='replace')

    # Check the created tables
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return [table[0] for table in tables]  # Return table names as a list

# Function to execute a SQL query and return the results
def execute_query(db_path, query):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        return str(e)
    finally:
        conn.close()

# Function to generate SQL query from natural language question using LLM
def generate_sql_query(question, table_name):
    prompt = f"""You are an expert in converting English questions to SQL queries! 
    If there are no records return No records found
    Convert the following question into a valid SQL query based on the table '{table_name}':{question}
    Make sure to:
    1. Use the correct column names as they appear in the table.
    2. Include any necessary clauses (e.g., WHERE, GROUP BY, ORDER BY) to accurately reflect the question.
    3. Provide only the SQL query without any additional text, formatting, or code blocks.
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt])
    sql_query = response.text.strip()  # Clean up the response
    return sql_query

# Streamlit App UI
st.title("Text-to-SQL Query Generator with Excel Upload")

# Step 1: Upload Excel File
uploaded_file = st.file_uploader("Upload your Excel file", type=['xlsx'])
db_path = "temp_database.db"

if uploaded_file:
    # Step 2: Convert Excel to SQLite Database
    created_tables = excel_to_sqlite(uploaded_file, db_path)
    st.success("Excel data has been converted to a database.")
    #st.write("Created tables in the database:", created_tables)  # Display created tables

    # Step 3: Ask a Question
    st.header("Ask a Question")
    question = st.text_input("Input your question:", "Give me the names of people with age above 30")

    if st.button("Convert to SQL Query and Get Result"):
        sql_query = generate_sql_query(question, created_tables[0])  # Pass the first table name

        if sql_query:
            st.write("Generated SQL Query:", sql_query)

            # Step 4: Execute the query
            if "SELECT" in sql_query:
                result = execute_query(db_path, sql_query)
                st.subheader("Query Result:")
                if isinstance(result, str):  # If there's an error
                    st.error(result)
                else:
                    if result:
                        for row in result:
                            st.write(row)
                    else:
                        st.write("No records found.")
            else:
                st.error("Failed to generate a valid SQL query.")
        else:
            st.error("Could not generate a SQL query from your question.")
