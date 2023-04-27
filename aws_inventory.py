import boto3
import openpyxl

# Set the following variables according to your organization and requirements
ORG_ID = 'your_org_id'
ROLE_NAME = 'YourRoleName'
SESSION_NAME = 'session_name'
SUPPORTED_SERVICES = ['ec2', 'rds', 's3', 'lambda', 'dynamodb']
OUTPUT_FILE_NAME = 'aws_inventory.xlsx'


# List all accounts in the organization
client = boto3.client('organizations')
accounts = []
next_token = None
while True:
    if next_token:
        response = client.list_accounts(NextToken=next_token)
    else:
        response = client.list_accounts()
    accounts += response['Accounts']
    if 'NextToken' in response:
        next_token = response['NextToken']
    else:
        break

# Create a workbook and worksheet
wb = openpyxl.Workbook()
ws = wb.active

# Write headers to the worksheet
headers = ['Account ID', 'Region', 'Service Name', 'Resource Type', 'Resource ID']
ws.append(headers)

# Iterate through all accounts and resources
for account in accounts:
    # Assume role in the account
    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=f"arn:aws:iam::{account['Id']}:role/{ROLE_NAME}",
        RoleSessionName=SESSION_NAME
    )
    credentials = assumed_role['Credentials']
    session = boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )

    # Iterate through all regions in the account
    for region in session.get_available_regions():
        for service_name in SUPPORTED_SERVICES:
            # Get the resource client
            try:
                resource_client = session.client(service_name, region_name=region)
                # Get all resources for the service
                resources = resource_client.list_resources()
            except Exception as e:
                print(f"Error listing resources in account {account['Id']} and region {region} for service {service_name}: {e}")
                continue
            for resource in resources['ResourceIdentifiers']:
                # Write the resource details to the worksheet
                ws.append([account['Id'], region, service_name.upper(), resource['ResourceType'], resource['ResourceIdentifier']])

# Save the workbook to a file
wb.save(OUTPUT_FILE_NAME)
