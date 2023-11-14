import csv
from collections import defaultdict as dd
import ipaddress


# Function to check if an IP address is private as for some reason Datadog will report that
def is_private_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        # If the IP address is invalid, treat it as non-private
        return False


# Input and output file paths
input_file_path = 'SecondAttack.csv'
output_file_path = 'output_file.csv'

# Dictionary to store counts of each non-private IP address
ip_count = dd(int)

# Read the CSV file and update non-private IP counts
with open(input_file_path, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        ip_list = row['context.ip'].split(',')

        for ip in ip_list:
            ip = ip.strip()
            if not is_private_ip(ip):
                ip_count[ip] += 1

# Filter rows based on non-private IP count and write to a new CSV file
with open(input_file_path, 'r', newline='') as csvfile, open(output_file_path, 'w', newline='') as outputfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outputfile, fieldnames=fieldnames)

    # Write headers to the output file
    writer.writeheader()

    for row in reader:
        ip_list = row['context.ip'].split(',')

        # Check if any non-private IP in the row has count greater than 3
        if any(ip_count[ip.strip()] > 3 for ip in ip_list):
            writer.writerow(row)

print("Processing complete. Output written to", output_file_path)
