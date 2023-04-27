from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.resource import ResourceManagementClient
import openpyxl

# Azure SDK for Python to iterate through all Azure accounts and regions to identify all users, roles, 
# and service accounts and saves the output to an Excel spreadsheet. Add your info at the top.

# Set the following variables according to your organization and requirements
SUBSCRIPTION_ID = 'your_subscription_id'
OUTPUT_FILE_NAME = 'azure_accounts_users_roles.xlsx'

# Create a credential object using the default Azure credentials
credential = DefaultAzureCredential()

# Create an Authorization Management client and list all role assignments
auth_client = AuthorizationManagementClient(credential, SUBSCRIPTION_ID)
role_assignments = list(auth_client.role_assignments.list())

# Create a Resource Management client and list all resources
resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
resources = list(resource_client.resources.list())

# Create a workbook and worksheet
wb = openpyxl.Workbook()
ws = wb.active

# Write headers to the worksheet
headers = ['Account ID', 'Region', 'User/Role/Service Account Name', 'User/Role/Service Account ID', 'User/Role/Service Account Type']
ws.append(headers)

# Iterate through all resources and role assignments
for resource in resources:
    # Get the resource ID
    resource_id = resource.id

    # Get the resource group and region from the resource ID
    resource_group = resource_id.split('/')[4]
    region = resource_id.split('/')[2]

    # List all role assignments for the resource
    for role_assignment in role_assignments:
        # Check if the role assignment is for the current resource
        if role_assignment.scope == resource_id:
            # Get the principal ID and type of the role assignment
            principal_id = role_assignment.principal_id
            principal_type = role_assignment.principal_type

            # Get the principal name based on the principal type
            if principal_type == 'User':
                principal_name = auth_client.users.get(principal_id).display_name
            elif principal_type == 'ServicePrincipal':
                principal_name = auth_client.service_principals.get(principal_id).display_name
            elif principal_type == 'Group':
                principal_name = auth_client.groups.get(principal_id).display_name
            else:
                principal_name = principal_id

            # Add the user/role/service account to the worksheet
            ws.append([SUBSCRIPTION_ID, region, principal_name, principal_id, principal_type])

# Save the workbook to a file
wb.save(OUTPUT_FILE_NAME)
