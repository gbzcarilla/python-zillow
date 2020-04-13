import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup as bs

"""
Objective: Create a program to read an address from a row in a Google spreadsheet, connect to the Zillow API and append the:
	- Zestimate,
	- square footage and
	- year built of the house
back to the spreadsheet
"""

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'python-zillow-credentials.json', scope)
client = gspread.authorize(creds)

sheet = client.open('ZillowSheet').sheet1

print("Before inserting data: ")
print(sheet.get_all_records())

url_zillow_api = "http://www.zillow.com/webservice/GetDeepSearchResults.htm"
zws_id = "X1-ZWz18nuirxd4i3_2avji"

z_address = sheet.acell('A2').value
z_citystatezip = sheet.acell('B2').value

params = {'zws-id': zws_id, 'address': z_address,
          'citystatezip': z_citystatezip}

response = requests.get(url=url_zillow_api, params=params)

bs = bs(response.text, "xml")

zestimate = bs.find("zestimate")

amount = bs.find("zestimate").amount.text
lot_size = bs.find("lotSizeSqFt").text
year_built = bs.find("yearBuilt").text

sheet.update_acell('C2', f"{float(amount):,.2f}")
sheet.update_acell('D2', f"{float(lot_size):,.2f}")
sheet.update_acell('E2', year_built)

print("After inserting data: ")
print(sheet.get_all_records())
