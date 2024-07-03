import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get environment variables
jira_domain = os.getenv("jira_domain")
email = os.getenv("email")
api_token = os.getenv("api_token")
project_key = os.getenv("project_key")

# Check if the environment variables are loaded correctly
if not all([jira_domain, email, api_token, project_key]):
    raise ValueError("Some environment variables are missing. Please check your .env file.")

# Set up the headers with basic authentication
auth = (email, api_token)
headers = {
    "Accept": "application/json"
}

# Jira API endpoint to get issues for a specific project
url = f"https://{jira_domain}/rest/api/2/search"

# Parameters to define the JQL query to fetch issues for the project
params = {
    "jql": f"project={project_key}",
    "maxResults": 100,
    "startAt": 0
}

issues = []

# Loop to handle pagination and collect all issues
while True:
    response = requests.get(url, headers=headers, params=params, auth=auth)
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print("Error response:", response.text)
        response.raise_for_status()

    try:
        response_data = response.json()
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        print("Response text:", response.text)
        break

    issues.extend(response_data['issues'])
    if len(response_data['issues']) < params['maxResults']:
        break
    params['startAt'] += params['maxResults']

# If no issues were retrieved, exit
if not issues:
    print("No issues retrieved. Exiting.")
    exit()

# Get today's date and format it
today_date = datetime.now().strftime("%Y-%m-%d")

# Create the new folder name
data_dir = 'data'
export_dir = os.path.join(data_dir, f"{today_date}_jira_export")

# Ensure the export directory exists
if not os.path.exists(export_dir):
    os.makedirs(export_dir)

# Save the issues to a JSON file in the export directory
json_file_path = os.path.join(export_dir, 'jira_issues.json')
with open(json_file_path, 'w') as json_file:
    json.dump(issues, json_file, indent=4)

print(f"Exported {len(issues)} issues to {json_file_path}")