Overview
The Agio Domain Pricing Tool allows you to query the GoDaddy API for domain availability and pricing. It generates combinations of domains based on a base word, customizable prefixes, suffixes, and TLDs (Top-Level Domains). The results are displayed in the terminal and saved to a CSV file for further analysis.



Features
Queries domain availability and pricing from the GoDaddy API.
Prompts for API Key and Secret during execution.
Uses a predefined list of valid TLDs to ensure accuracy.
Dynamically adds user-provided TLDs, prefixes, and suffixes after validation.
Handles errors and retries failed requests up to three times.
Saves the results to Agio_Domain_pricing.csv.
Displays results in paginated chunks in the terminal.


Setup Instructions
1. Prerequisites
Python: Ensure Python 3.7+ is installed on your system.

Download Python from python.org.
Verify installation

python --version


Pip: Ensure pip (Python package manager) is installed. Check with:

pip --version

Install Dependencies
Clone or download the repository containing this script.
Navigate to the directory where the script is located.
Install the required Python libraries

pip install requests pandas

 Get GoDaddy API Keys
Log in to the GoDaddy Developer Portal.
Navigate to My API Keys under your account profile.
Click Create API Key:
Choose Production for live queries.
Provide a name for the API key (e.g., "Domain Query Tool").
Copy the API Key and API Secret provided.

Running the Script
Open a terminal or command prompt.
Navigate to the directory where the script is saved.
Run the script:

python domain_query_tool.py

Follow the prompts:

Enter your GoDaddy API Key and Secret.
Specify the base word for the domain.
Optionally, add more TLDs, prefixes, and suffixes during the prompts.

Outputs

Terminal Display: Shows the progress of domain queries and results in paginated chunks.

CSV File: Saves the results to Agio_Domain_pricing.csv in the current directory.


