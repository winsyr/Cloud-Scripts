import openpyxl
from google.cloud import compute_v1

# This script uses the GCP SDK for Python to iterate through all GCP subscriptions 
# and resource groups to take inventory of all resources and save the output to an Excel document. 
# Add your info at the top.

# Authenticate with Google Cloud SDK
client = compute_v1.InstancesClient()

# Create a new Excel workbook
wb = openpyxl.Workbook()

# Create a new worksheet
ws = wb.active
ws.title = 'GCP Public IPs'

# Define the header row
header = ['Instance Name', 'Public IP']

# Write the header row to the worksheet
ws.append(header)

# Iterate over all GCP instances
for instance in client.list():
    # Extract relevant information
    instance_name = instance.name
    public_ip = instance.network_interfaces[0].access_configs[0].nat_ip

    # Write the information to the worksheet
    row = [instance_name, public_ip]
    ws.append(row)

# Save the workbook to a file
wb.save('gcp_public_ips.xlsx')
