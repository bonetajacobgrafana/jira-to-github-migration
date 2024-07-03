import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Paths to the scripts
export_jira_script = './export_jira_issues.py'
import_github_script = './github_import.py'

# Run the Jira export script
print("Exporting issues from Jira...")
subprocess.run(['python', export_jira_script], check=True)

# Run the GitHub import script
print("Importing issues to GitHub...")
subprocess.run(['python', import_github_script], check=True)

print("Done.")