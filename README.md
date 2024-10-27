# Excel Query Wizard

**Excel Query Wizard** is a web app developed with **Streamlit** and powered by **Gemini-Pro LLM**. This tool allows users to import Excel files, automatically converting them into a **SQLite** database and generating **SQL queries** to extract key insights, simplifying data retrieval from complex spreadsheets.

## Features

- **Excel File Import**: Users can upload `.xlsx` files for data processing and analysis.
- **Automated Conversion**: Converts Excel data into a **SQLite** database to enable efficient querying.
- **SQL Query Creation**: Generates **SQL queries** based on user input, enabling easy access to specific data points.
- **Streamlit Interface**: Provides a simple, interactive UI for seamless app use.

## How It Works

1. Upload an Excel file (.xlsx) using the app interface.
2. The app automatically converts the Excel data into a SQLite database.
3. **Gemini-Pro LLM** generates SQL queries based on the user’s prompts to extract relevant data.
4. View query results directly in the app.

## Getting Started

### Prerequisites & Installation

- [Python 3.8+](https://www.python.org/downloads/)
- [Streamlit](https://docs.streamlit.io/)
- Required dependencies in `requirements.txt`
- Install dependencies: pip install -r requirements.txt
- Run the app: streamlit run app.py

### 1. App Interface
![App Interface](images/1.png)

### 2. SQL Query Generation
![SQL Query Generation](images/2.png)

### 3. Query Results
![Query Results](images/3.png)
