import os
import json
import requests
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
github_token = os.getenv("github_token")
github_repo = os.getenv("github_repo")
json_file_path = os.getenv("json_file_path")

# Check if the environment variables are loaded correctly
if not all([github_token, github_repo, json_file_path]):
    raise ValueError("Some environment variables are missing. Please check your .env file.")

# Set up the headers with authentication
headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json"
}

# Read the JSON file
with open(json_file_path, 'r') as file:
    issues = json.load(file)

# Check if issues is a list of dictionaries
if not isinstance(issues, list) or not all(isinstance(issue, dict) for issue in issues):
    raise ValueError("JSON file format is incorrect. Expected a list of dictionaries.")

# GitHub API endpoint to create an issue
url = f"https://api.github.com/repos/{github_repo}/issues"

# Function to create an issue with rate limiting handling
def create_issue(issue_data):
    response = requests.post(url, headers=headers, json=issue_data)
    if response.status_code == 201:
        return True, response.json()
    elif response.status_code == 403:
        # Check if it's due to secondary rate limit
        if "secondary rate limit" in response.text:
            print("Hit secondary rate limit. Sleeping for 60 seconds.")
            time.sleep(60)  # Sleep for 60 seconds
            return create_issue(issue_data)  # Retry after sleep
    elif response.status_code == 429:
        # Handle 429 Too Many Requests by checking headers for retry information
        retry_after = int(response.headers.get('Retry-After', 60))
        print(f"Rate limited. Sleeping for {retry_after} seconds.")
        time.sleep(retry_after)
        return create_issue(issue_data)
    return False, response

# Iterate over the tasks and create issues in GitHub
for issue in issues:
    fields = issue.get('fields', {})
    title = fields.get('summary') or "No title provided"
    body = fields.get('description') or "No description provided"
    status_name = fields.get('status', {}).get('name') or "No status"
    
    # Extract labels from the original ticket
    original_labels = fields.get('labels', [])
    labels = [status_name] + original_labels  # Combine status name with original labels

    data = {
        "title": title,
        "body": body,
        "labels": labels  # Ensure labels is a list
    }
    
    success, response = create_issue(data)
    if success:
        print(f"Successfully created issue: {title}")
    else:
        print(f"Failed to create issue: {title}. Status Code: {response.status_code}, Response: {response.text}")
    time.sleep(2)  # Sleep for 2 seconds between requests to avoid hitting the rate limit