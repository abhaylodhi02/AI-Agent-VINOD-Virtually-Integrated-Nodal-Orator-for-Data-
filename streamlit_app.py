import streamlit as st
import pandas as pd
from utils.data_handler import load_csv, connect_google_sheet
from utils.search_api import search_web
from utils.llm_integration import parse_with_llm

st.title("AI Agent for Data Retrieval and Parsing")

st.sidebar.header("File Upload")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])
google_sheet = st.sidebar.text_input("Google Sheet ID")

st.sidebar.header("Query Input")
primary_column = st.sidebar.selectbox("Select Main Column", [""])
custom_prompt = st.sidebar.text_area("Custom Prompt", "Get the email address for {company}")

if uploaded_file:
    data = load_csv(uploaded_file)
    st.write("CSV Data Preview:", data.head())
elif google_sheet:
    # Fetch Google Sheet data (you'll need to implement the credentials JSON)
    credentials_json = {}  # Replace with Google API credentials
    data = connect_google_sheet(credentials_json, google_sheet)
    st.write("Google Sheet Data Preview:", data.head())
else:
    st.write("Please upload a file or provide a Google Sheet ID.")

if data is not None:
    selected_column = st.selectbox("Select column with entities:", data.columns)

    if st.button("Run Web Search & Extract Information"):
        extracted_info = []
        for entity in data[selected_column]:
            query = custom_prompt.format(entity=entity)
            search_results = search_web(query)

            if search_results:
                content = " ".join([result["snippet"] for result in search_results])
                parsed_info = parse_with_llm(content, custom_prompt)
                extracted_info.append((entity, parsed_info))
        
        result_df = pd.DataFrame(extracted_info, columns=[selected_column, "Extracted Info"])
        st.write("Results:", result_df)
        st.download_button(
            "Download Results as CSV",
            result_df.to_csv(index=False),
            file_name="extracted_info.csv"
        )
