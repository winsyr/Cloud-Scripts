import nmap
import json
from tqdm import tqdm

# Define input and output file names
input_file = 'owasp_scanner_hosts.json'
output_file = 'owasp_scanner_results.json'

# Read input file
with open(input_file, 'r') as f:
    input_data = json.load(f)

# Extract list of IPs from input data
input_ips = input_data['ips'] if 'ips' in input_data else []

# Initialize dictionary to store results
results = {}

# Define nmap options to scan for the OWASP Top 10 vulnerabilities
nmap_options = '-sV --script http-sql-injection,http-shellshock,http-csrf,http-default-accounts,http-enum,http-fileuploads,http-php-version,http-iis-webdav-vuln,http-robots.txt'

# Loop through input IPs and scan for vulnerabilities
for ip in tqdm(input_ips, desc='Scanning IPs'):
    # Initialize nmap scanner
    nm = nmap.PortScanner()

    # Scan IP with nmap options
    nm.scan(hosts=ip, arguments=nmap_options)

    # Initialize dictionary to store results for this IP
    ip_results = {}

    # Check if IP is reachable
    if nm[ip].state() == 'up':
        # Loop through protocols and ports and store vulnerability results
        for protocol in nm[ip].all_protocols():
            ip_results[protocol] = {}
            if nm[ip][protocol]:
                for port in nm[ip][protocol].keys():
                    port_results = {}
                    if 'script' in nm[ip][protocol][port]:
                        for script_name, script_result in nm[ip][protocol][port]['script'].items():
                            if 'VULNERABLE' in script_result:
                                port_results[script_name] = True
                    ip_results[protocol][port] = port_results
    else:
        print(f'Error: {ip} is not reachable or did not return any vulnerabilities. There may be a security control in front of the endpoint.')
    
    # Add IP results to overall results dictionary
    results[ip] = ip_results

# Write results to output file
with open(output_file, 'w') as f:
    json.dump(results, f, indent=4)

print(f'Scan complete. Results written to {output_file}.')
