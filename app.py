import os
import streamlit as st
import pandas as pd
import requests
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from groq import Groq

# Load API keys from a separate file
with open("api_keys.json", "r") as f:
    api_keys = json.load(f)

GROQ_API_KEY = api_keys["GROQ_API_KEY"]
SERP_API_KEY = api_keys["SERP_API_KEY"]

# Initialize GROQ API
client = Groq(api_key=GROQ_API_KEY)

# Google Sheets API Setup
def get_google_sheets_service():
    credentials = service_account.Credentials.from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
    )
    return build("sheets", "v4", credentials=credentials)

# Function to fetch all tab (worksheet) names in a spreadsheet
def get_tab_names(spreadsheet_id):
    service = get_google_sheets_service()
    try:
        # Get spreadsheet metadata
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        # Extract sheet names
        sheets = spreadsheet.get("sheets", [])
        tab_names = [sheet["properties"]["title"] for sheet in sheets]
        return tab_names
    except Exception as e:
        raise Exception(f"Error fetching tab names: {e}")

# Function to read Google Sheet with correct range handling
def read_google_sheet(spreadsheet_id, range_name):
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    try:
        # Attempt to get data from the sheet with the provided range
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get("values", [])
        # If data exists, return as DataFrame
        if values:
            return pd.DataFrame(values[1:], columns=values[0])  # The first row is used as column names
        else:
            return pd.DataFrame()  # Return an empty DataFrame if no data is found
    except Exception as e:
        raise Exception(f"Error reading Google Sheet: {e}")

# Function to perform a web search (for getting context-specific information)
def perform_web_search(query):
    url = f"https://serpapi.com/search.json?q={query}&api_key={SERP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("organic_results", [])
        return "\n".join([result.get("snippet", "") for result in results[:3]])  # Adjust for more results
    else:
        return "Error fetching search results."

# Streamlit UI
st.title("AI-Powered Data Query Dashboard")

# Store uploaded file, Google Sheet URL, or selected column in session state
if "df" not in st.session_state:
    st.session_state.df = None
if "column" not in st.session_state:
    st.session_state.column = None

# File Upload or Google Sheet Input
file_or_sheet = st.radio("Select Data Source", ["Upload CSV File", "Connect Google Sheet"])
if file_or_sheet == "Upload CSV File":
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data Preview:")
        st.dataframe(st.session_state.df)
elif file_or_sheet == "Connect Google Sheet":
    google_sheet_url = st.text_input("Enter Google Sheet URL")
    if google_sheet_url:
        try:
            # Extract Spreadsheet ID from URL
            spreadsheet_id = google_sheet_url.split("/")[5]
            
            # Fetch available tab names
            tab_names = get_tab_names(spreadsheet_id)
            st.write("Available Tabs:", tab_names)
            
            # Let the user select a tab
            selected_tab = st.selectbox("Select a Tab", tab_names)
            
            # Define the range dynamically based on the selected tab
            range_name = f"{selected_tab}!A1:Z1000"
            
            # Read data from the selected tab
            st.session_state.df = read_google_sheet(spreadsheet_id, range_name)
            st.write("Google Sheet Data Preview:")
            st.dataframe(st.session_state.df)
        except Exception as e:
            st.error(f"Error loading Google Sheet: {e}")

# Ensure that there is a DataFrame to interact with
if st.session_state.df is not None:
    # Allow user to select a column to query upon
    selected_column = st.selectbox("Select a Column to Query", st.session_state.df.columns)
    st.session_state.column = selected_column

    # Show a preview of the selected column
    st.write(f"Preview of '{selected_column}' Column:")
    st.write(st.session_state.df[selected_column].head())

    # Query input from the user
    query_prompt = st.text_area(
        "Enter your Query",
        "Example: Get detailed information for {column_value}.",
    )

    # Process query on data
    if st.button("Run Query"):
        if query_prompt and st.session_state.column:
            query_results = []
            # Process each item in the selected column based on the prompt
            for item in st.session_state.df[selected_column]:
                # Update the query to replace the placeholder with the actual column value
                prompt = query_prompt.replace("{column_value}", str(item))
                # Fetch results based on the prompt
                search_results = perform_web_search(prompt)
                query_results.append({"Context": item, "Result": search_results})

            # Convert the results to a DataFrame for display
            result_df = pd.DataFrame(query_results)
            st.write("Query Results:")
            st.dataframe(result_df)

            # Provide option to download results as CSV
            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv",
            )
        else:
            st.warning("Please enter a query and select a column.")
