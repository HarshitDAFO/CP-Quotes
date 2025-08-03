import gspread
from oauth2client.service_account import ServiceAccountCredentials

def save_to_google_sheet(data_row):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("CoverPrime Leads").sheet1
    sheet.append_row(data_row)
