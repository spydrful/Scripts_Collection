import csv
import requests
from collections import defaultdict
import ipaddress

def is_private_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return False

def get_risk_for_ip(ip, token):
    api_url = f"https://api.spur.us/v2/context/{ip}"
    headers = {"Token": token}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        json_response = response.json()
        risk_field = json_response.get("risks", [])
        print(risk_field)
        return risk_field
    except Exception as e:
        print(f"Error making API call for IP {ip}: {e}")
        return []

input_file_path = "SecondAttack.csv"
output_file_path = "output_file_with_risk.csv"
api_token = "These are not the tokens you are looking for"

ip_count = defaultdict(int)

with open(input_file_path, "r", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)  # Store rows in a list for further iteration

    for row in rows:
        ip_list = row["context.ip"].split(",")
        risk_fields = []

        for ip in ip_list:
            ip = ip.strip()
            if not is_private_ip(ip):
                ip_count[ip] += 1

                try:
                    risk_field = get_risk_for_ip(ip, api_token)
                    risk_fields.extend(risk_field)
                except Exception as e:
                    print(f"Error making API call for IP {ip}: {e}")

        row["Risk"] = ", ".join(risk_fields)

# Reopen the input file and reinitialize the reader object
csvfile = open(input_file_path, "r", newline="")
reader = csv.DictReader(csvfile)

with open(output_file_path, "w", newline="") as outputfile:
    fieldnames = reader.fieldnames + ["Risk"]
    writer = csv.DictWriter(outputfile, fieldnames=fieldnames)

    writer.writeheader()

    # Write rows from the stored 'rows' list
    for row in rows:
        writer.writerow(row)

print("Processing complete. Output written to", output_file_path)
