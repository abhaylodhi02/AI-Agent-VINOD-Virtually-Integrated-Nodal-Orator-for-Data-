import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

def load_csv(file):
    return pd.read_csv(file)

def connect_google_sheet(credentials_json, sheet_id, range_name="Sheet1"):
    creds = service_account.Credentials.from_service_account_info(credentials_json)
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get("values", [])
    return pd.DataFrame(values[1:], columns=values[0])
