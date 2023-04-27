import openpyxl
from googleapiclient.discovery import build

# This script uses the GCP SDK for Python to iterate through all GCP subscriptions 
# and resource groups to take inventory of all resources and save the output to an Excel document. 
# Add your info at the top.

# Authenticate with Google Cloud SDK
service = build('iam', 'v1')

# Create a new Excel workbook
wb = openpyxl.Workbook()

# Create a new worksheet
ws = wb.active
ws.title = 'GCP Identities'

# Define the header row
header = ['Type', 'Name', 'Email']

# Write the header row to the worksheet
ws.append(header)

# Iterate over all GCP identities
for account in service.projects().serviceAccounts().list(name='projects/-').execute()['accounts']:
    # Extract relevant information
    account_name = account['name']
    account_email = account['email']

    # Write the information to the worksheet
    row = ['Service Account', account_name, account_email]
    ws.append(row)

# Iterate over all GCP users
for user in service.users().list().execute()['users']:
    # Extract relevant information
    user_name = user['name']
    user_email = user['email']

    # Write the information to the worksheet
    row = ['User', user_name, user_email]
    ws.append(row)

# Save the workbook to a file
wb.save('gcp_identities.xlsx')
