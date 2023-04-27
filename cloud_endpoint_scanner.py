import nmap
import json
from tqdm import tqdm

# Read input data from JSON file
with open('cloud_scanner_input.json') as f:
    data = json.load(f)

# Extract IP addresses from data
ips = data['ips']

# Initialize nmap scanner
nm = nmap.PortScanner()

# Initialize results dictionary
results = {}

# Loop through IP addresses and scan for open ports
for ip_address in tqdm(ips):
    nm.scan(hosts=ip_address, arguments='-sS -sV -O')
    open_ports = []
    for port in nm[ip_address]['tcp']:
        if nm[ip_address]['tcp'][port]['state'] == 'open':
            open_ports.append(port)
    os_info = nm[ip_address]['osmatch'][0]['osclass'][0]['osfamily']
    software_versions = {}
    for port in open_ports:
        service = nm[ip_address]['tcp'][port]['name']
        version = nm[ip_address]['tcp'][port]['version']
        software_versions[service] = version
    vulnerabilities = [str(nm[ip_address]['tcp'][int(port)]['script']) for port in nm[ip_address]['tcp'] if 'script' in nm[ip_address]['tcp'][int(port)]]
    results[ip_address] = {'open_ports': open_ports, 'os_info': os_info, 'software_versions': software_versions, 'vulnerabilities': vulnerabilities}

# Write results to output JSON file
with open('cloud_scanner_output.json', 'w') as f:
    json.dump(results, f, indent=4)
