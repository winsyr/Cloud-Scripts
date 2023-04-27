import openpyxl
from google.cloud import resource_manager

# This script uses the GCP SDK for Python to iterate through all GCP subscriptions 
# and resource groups to take inventory of all resources and save the output to an Excel document. 
# Add your info at the top.

# Authenticate with Google Cloud SDK
client = resource_manager.Client()

# Create a new Excel workbook
wb = openpyxl.Workbook()

# Create a new worksheet
ws = wb.active
ws.title = 'GCP Resources'

# Define the header row
header = ['Type', 'Name', 'ID', 'Parent']

# Write the header row to the worksheet
ws.append(header)

# Iterate over all GCP resources
for resource in client.list_resources():
    # Extract relevant information
    res_type = resource.type
    res_name = resource.name
    res_id = resource.id
    res_parent = resource.parent

    # Write the information to the worksheet
    row = [res_type, res_name, res_id, res_parent]
    ws.append(row)

# Save the workbook to a file
wb.save('gcp_resources.xlsx')
