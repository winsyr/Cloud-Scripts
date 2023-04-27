from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
import openpyxl

# This script uses the Azure SDK for Python to iterate through all Azure resources 
# and regions to identify all public IP addresses and saves the output to an Excel spreadsheet. 
# Add your info at the top

# Set the following variables according to your organization and requirements
SUBSCRIPTION_ID = 'your_subscription_id'
OUTPUT_FILE_NAME = 'azure_public_ips.xlsx'

# Create a credential object using the default Azure credentials
credential = DefaultAzureCredential()

# Create a Compute Management client and list all virtual machines
compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
vms = list(compute_client.virtual_machines.list_all())

# Create a workbook and worksheet
wb = openpyxl.Workbook()
ws = wb.active

# Write headers to the worksheet
headers = ['Account ID', 'Region', 'Resource Name', 'Public IP Address']
ws.append(headers)

# Iterate through all virtual machines and network interfaces to get public IP addresses
for vm in vms:
    # Get the resource group and region from the virtual machine
    resource_group = vm.id.split('/')[4]
    region = vm.location

    # Iterate through all network interfaces attached to the virtual machine
    for nic in vm.network_profile.network_interfaces:
        # Get the network interface ID
        nic_id = nic.id

        # Get the network interface and its IP configurations
        nic_obj = compute_client.network_interfaces.get(resource_group, nic_id)
        ip_configs = nic_obj.ip_configurations

        # Iterate through all IP configurations and get the public IP address
        for ip_config in ip_configs:
            if ip_config.public_ip_address:
                # Get the public IP address ID and its details
                public_ip_id = ip_config.public_ip_address.id
                public_ip_obj = compute_client.public_ip_addresses.get(resource_group, public_ip_id)

                # Add the public IP address to the worksheet
                ws.append([SUBSCRIPTION_ID, region, vm.name, public_ip_obj.ip_address])

# Save the workbook to a file
wb.save(OUTPUT_FILE_NAME)
