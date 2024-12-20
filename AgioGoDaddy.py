import requests
import pandas as pd
import time
from itertools import islice

# Prompt for GoDaddy API credentials
API_KEY = input("Enter your GoDaddy API Key: ").strip()
API_SECRET = input("Enter your GoDaddy API Secret: ").strip()
BASE_URL = "https://api.godaddy.com/v1"

def batch_iterator(iterable, size):
    """Helper function to create batches of a specific size."""
    iterator = iter(iterable)
    for first in iterator:
        yield [first] + list(islice(iterator, size - 1))

def query_domains(base_name, tlds, prefixes, suffixes):
    headers = {
        "Authorization": f"sso-key {API_KEY}:{API_SECRET}",
        "Accept": "application/json",
    }
    domain_pricing = []
    max_retries = 3  # Retry limit

    # Generate domain combinations
    domain_combinations = [
        f"{prefix}{base_name}{suffix}.{tld}"
        for tld in tlds
        for prefix in prefixes
        for suffix in suffixes
    ]

    try:
        for batch in batch_iterator(domain_combinations, 50):  # Adjust batch size if necessary
            for domain in batch:
                print(f"Processing {domain}...")
                for attempt in range(max_retries):
                    try:
                        start_time = time.time()
                        response = requests.get(
                            f"{BASE_URL}/domains/available",
                            headers=headers,
                            params={"domain": domain},
                            timeout=30  # Increase timeout for slow responses
                        )
                        response.raise_for_status()
                        data = response.json()
                        domain_pricing.append({
                            "Domain": domain,
                            "Available": data.get("available", False),
                            "Price": data.get("price", "N/A") / 1000000 if "price" in data else "N/A",
                        })
                        print(f"Processed {domain} in {time.time() - start_time:.2f} seconds.")
                        break  # Exit retry loop if successful
                    except requests.exceptions.RequestException as e:
                        print(f"Error querying {domain} on attempt {attempt + 1}: {e}")
                        time.sleep(2)  # Retry delay
                else:
                    # If all retries fail
                    domain_pricing.append({
                        "Domain": domain,
                        "Available": "Error",
                        "Price": "Error",
                    })
                time.sleep(0.2)  # Delay between requests
    except KeyboardInterrupt:
        print("Script interrupted by user. Saving progress...")

    return domain_pricing

# Pagination function
def paginate_dataframe(df, rows_per_page=20):
    for i in range(0, len(df), rows_per_page):
        print(df.iloc[i:i+rows_per_page])  # Display rows in chunks
        input("Press Enter to see more...")

# Prompt for user input
base_name = input("Enter the base word for domain search (e.g., 'capital'): ").strip()

# Valid TLDs list
tlds = [
    "com", "net", "org", "finance", "capital", "money", "biz", "investments", 
    "bank", "group", "fund", "wealth", "loans", "credit", "markets", "ventures", 
    "io", "ai", "tech", "global", "online", "cloud", "store", "consulting", 
    "insurance", "agency", "partners"
]

# Prompt to add more TLDs
additional_tlds = input("Enter additional TLDs separated by commas (e.g., '.insurance,.agency'): ").strip()
if additional_tlds:
    user_tlds = [tld.strip().lstrip(".") for tld in additional_tlds.split(",")]
    valid_user_tlds = [tld for tld in user_tlds if tld in tlds]
    tlds.extend(valid_user_tlds)
    if not valid_user_tlds:
        print("No valid additional TLDs provided.")

# Financially relevant prefixes and suffixes
prefixes = ["", "My", "Pro", "Elite", "Secure"]  # Financially relevant prefixes
suffixes = ["", "Funds", "Capital", "Wealth", "Investments", "Banking", "Group"]  # Financial suffixes

# Prompt to add more prefixes or suffixes
additional_prefixes = input("Enter additional prefixes separated by commas (e.g., 'Super,Best'): ").strip()
if additional_prefixes:
    prefixes.extend([prefix.strip() for prefix in additional_prefixes.split(",")])

additional_suffixes = input("Enter additional suffixes separated by commas (e.g., 'Services,Solutions'): ").strip()
if additional_suffixes:
    suffixes.extend([suffix.strip() for suffix in additional_suffixes.split(",")])

# Query the domains and create a DataFrame
domain_data = query_domains(base_name, tlds, prefixes, suffixes)
df = pd.DataFrame(domain_data)

# Save to CSV
csv_filename = "Agio_Domain_pricing.csv"
df.to_csv(csv_filename, index=False)
print(f"Results saved to {csv_filename}")

# Adjust Pandas display settings
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pd.set_option("display.colheader_justify", "left")

# Display results with pagination
paginate_dataframe(df)
