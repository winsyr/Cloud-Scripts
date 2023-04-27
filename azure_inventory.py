from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient, ResourceManagementClient
import openpyxl

# This script uses the Azure SDK for Python to iterate through all Azure subscriptions 
# and resource groups to take inventory of all resources and save the output to an Excel document. 
# Add your info at the top.

# Set the following variables according to your organization and requirements
TENANT_ID = 'your_tenant_id'
OUTPUT_FILE_NAME = 'azure_inventory.xlsx'

# Create a credential object using the default Azure credentials
credential = DefaultAzureCredential()

# Create a Subscription Management client and list all subscriptions
subscription_client = SubscriptionClient(credential)
subscriptions = list(subscription_client.subscriptions.list())

# Create a workbook and worksheet
wb = openpyxl.Workbook()
ws = wb.active

# Write headers to the worksheet
headers = ['Subscription ID', 'Resource Group', 'Resource Type', 'Resource Name']
ws.append(headers)

# Iterate through all subscriptions
for subscription in subscriptions:
    # Set the subscription ID for the Resource Management client
    subscription_id = subscription.subscription_id
    resource_client = ResourceManagementClient(credential, subscription_id)

    # List all resource groups in the subscription
    resource_groups = list(resource_client.resource_groups.list())

    # Iterate through all resource groups
    for resource_group in resource_groups:
        # List all resources in the resource group
        resources = list(resource_client.resources.list_by_resource_group(resource_group.name))

        # Iterate through all resources and add them to the worksheet
        for resource in resources:
            ws.append([subscription_id, resource_group.name, resource.type, resource.name])

# Save the workbook to a file
wb.save(OUTPUT_FILE_NAME)
