# Jira to GitHub Integration

This project automates the process of exporting issues from Jira and importing them into GitHub.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_ORG/YOUR_REPOSITORY.git
   cd YOUR_REPOSITORY

2.  **Create a `.env` File**: Create a `.env` file in the project root with the following content:

    `# Jira export variables
    jira_domain=your-domain.atlassian.net
    email=your-email@example.com
    api_token=your-api-token
    project_id=your-project-id

    # GitHub import variables
    github_token=your-github-token
    github_repo=your-username/your-repository
    json_file_path=./jira_issues.json`

3.  **Install dependencies**:

    bash

    `pip install -r requirements.txt`

4.  **Run the main script**:


    bash

    `python main.py`

## Scripts
-   `export_jira_issues.py`: Exports issues from Jira and saves them to a JSON file.
-   `github_import.py`: Imports issues from the JSON file into a GitHub repository.
-   `main.py`: Orchestrates the export and import process.