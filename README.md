# AI-Powered Data Query Dashboard
This project is an AI-powered dashboard built with Streamlit, allowing users to upload a CSV file or connect to a Google Sheet to query specific columns. The application allows users to input natural language queries and fetch relevant search results using the SERP API. The results are displayed in a DataFrame and can be downloaded as CSV files.

# Project Setup:
## Prerequisites
Ensure you have the following installed:

Python 3.7+
Streamlit (for the frontend)
Pandas (for data manipulation)
Google API Client (for Google Sheets integration)
requests (for web scraping via SERP API)
Groq API Client (for AI-based processing)
Install Dependencies
To set up the project, follow these steps:

## Clone or download the repository:
git clone <your-repo-url>
cd <your-repo-directory>

## Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate   # On Windows, use venv\Scripts\activate

## Install the required packages:
pip install -r requirements.txt

## API Keys Configuration
You will need to set up your API keys for the project. Create a file named api_keys.json in the root of the project and include your API keys for GROQ and SERPAPI as shown below:

json

{
    
    "GROQ_API_KEY": "your-groq-api-key",
    
    "SERP_API_KEY": "your-serp-api-key"
}


Additionally, for Google Sheets access, you'll need to generate a Google Service Account key and save it as credentials.json in the project directory. You can follow the instructions here: Google Sheets API Quickstart.

## Project Workflow
1. Select Data Source
Upload CSV File: Users can upload a CSV file that will be loaded into the app as a DataFrame.
Connect Google Sheet: Users can enter the URL of a Google Sheet, and the application will fetch the available tabs (worksheets) within the sheet.
2. Select Column for Query
Once the data is loaded, the user can select a column from the sheet to query.
3. Enter Query
The user can enter a natural language query where {column_value} is the placeholder for values in the selected column. The system replaces this placeholder with the actual column values.
4. Web Search for Context
The application queries the SERP API to fetch search results based on the query entered by the user. The results are displayed in a DataFrame.
5. Export Results
Once the query results are fetched, users can download the results as a CSV file.

## Technology and Tools Used
Streamlit: For creating the interactive frontend.

Pandas: For data manipulation and processing of CSV files and Google Sheets data.

Google Sheets API: For reading Google Sheets data.

SERP API: For performing web searches and fetching contextual data for the user query.

Groq API: Used for AI-based processing (for future enhancement, not fully integrated in this version).

Python: The primary language for the backend logic.

## How the Project Works
1. Google Sheets Integration
The app connects to Google Sheets using the Google Sheets API, where you provide the Google Sheet URL.
The app dynamically fetches all available tab names (worksheets) and allows users to select one.
Data is read from the selected tab, and the first row is used as column headers.
2. Web Search Integration
The app uses the SERP API to perform web searches based on the user’s query. It replaces the {column_value} placeholder with each value in the selected column and fetches related search snippets.
3. Results Display and Download
After fetching the search results, the app displays the results in a table format. The user can download the results as a CSV file.
Running the Project

## Step-by-Step Instructions
Navigate to your project directory.
Start the Streamlit app with the following command:
streamlit run app.py
This will open a new tab in your browser where the dashboard will be running.

## Using the Dashboard
Step 1: Select your data source. You can either upload a CSV file or connect to a Google Sheet.

Step 2: Once the data is loaded, select the column you want to query.

Step 3: Enter a query where {column_value} will be replaced with the values from the selected column.

Step 4: Press Run Query to get the results. You will see the query results, and you can download the results as a CSV file.

## Result of the Project
1. Data Interaction:
Users can seamlessly interact with their data, either from a CSV file or Google Sheet, and perform queries based on columns they select.
2. AI-Powered Query Responses:
The app fetches context-specific information using the SERP API, which allows users to get detailed search results tailored to their queries.
3. Data Export:
After querying, users can download the results in CSV format for further analysis or reporting.
Sample Output
For a column containing product names, if the user queries, "Get detailed information for {column_value}", the results might look like:

## Example Demo: 
1. Upload a csv file or connect a google sheet via URL.
   
   <img src="https://github.com/user-attachments/assets/f6d8d9a8-7f84-4cc8-87ed-cfc02c5077f3" width="500" height="300">
  
2. Get the preview of the uploaded file.

   <img src="https://github.com/user-attachments/assets/e4170014-2361-42c2-8f9f-f928f94e6a39" width="650" height="550">

3. Select the column on which search query execution is to be made and enter the prompt. Do not change {column_name} as it is for dynamically handling multiple inputs.
   
   <img src="https://github.com/user-attachments/assets/1ed693d8-f616-4be9-8994-1df177e9c819" width="700" height="600">

4. Get the output. Users can download these results as a CSV file for further analysis.

   <img src="https://github.com/user-attachments/assets/d55c18c9-d81d-4d82-a8e0-ee1d3cabf91a" width="700" height="600">


# THANK YOU!!!
