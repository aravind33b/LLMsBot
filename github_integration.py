import os
import json
from dotenv import load_dotenv
import requests
import re

def fetch_github_files(owner: str, repo: str, path: str, branch="main"):
    load_dotenv()
    
    bearer_token: str = os.getenv("GITHUB_TOKEN")
    if not bearer_token:
        raise ValueError("GITHUB_TOKEN is not set in the environment variables")

    base_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'

    def get_files(url):
        response = requests.get(url, headers={'Authorization': 'Bearer ' + bearer_token})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return []

    def fetch_files_recursive(url):
        files = []
        items = get_files(url)
        for item in items:
            if item['type'] == 'file' and item['name'].endswith(('mdx', 'md')):
                raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/refs/heads/{branch}/{item['path']}"
                files.append((item['path'], raw_url))
            elif item['type'] == 'dir':
                files.extend(fetch_files_recursive(item['url']))
        return files

    def arrange_files_on_topics(files):
        topics = {}

        def clean_name(name):
            return re.sub(r'^\d+\-?', '', name)

        def insert_into_dict(path_parts, url, current_dict):
            if len(path_parts) == 1:
                file_name = clean_name(path_parts[0]).replace('.mdx', '').replace('.md', '').replace('-', ' ').title()
                current_dict[file_name] = url
            else:
                #recursively create nested dictionaries
                folder = clean_name(path_parts[0]).replace('-', ' ').title()
                if folder not in current_dict:
                    current_dict[folder] = {}
                insert_into_dict(path_parts[1:], url, current_dict[folder])

        for file_path, raw_url in files:
            path_parts = file_path.split('/')[3:]
            insert_into_dict(path_parts, raw_url, topics)

        return topics

    all_files = fetch_files_recursive(base_url)
    indexed_files = arrange_files_on_topics(all_files)
    print(f"Found {len(all_files)} files with extension {['mdx', 'md']}")
    return indexed_files