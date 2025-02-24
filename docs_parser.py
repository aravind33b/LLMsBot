import requests
import re

def fetch_and_parse_mdx(url):

    # Fetches the content of an .mdx file from a given URL and parses useful information.
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None

    content = response.text

    # Extract Headings
    headings = re.findall(r'^(#+)\s+(.*)', content, re.MULTILINE)

    # Extract Code Blocks (Assuming triple backticks are used)
    code_blocks = re.findall(r'```(.*?)```', content, re.DOTALL)

    # Extract Function Names
    function_names = re.findall(r'def\s+(\w+)\s*\(', content)

    return {
        "url": url,
        "headings": [h[1] for h in headings],
        "code_blocks": code_blocks,
        "function_names": function_names
    }

def process_all_docs(docs_urls):
    """
    Iterate over all docs URLs and parse their content.
    """
    parsed_docs = {}

    def recursive_parse(node, current_dict):
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, dict):
                    current_dict[key] = {}
                    recursive_parse(value, current_dict[key])
                else:
                    # Fetch and parse the content
                    parsed_data = fetch_and_parse_mdx(value)
                    current_dict[key] = parsed_data
        else:
            # Single URL
            parsed_data = fetch_and_parse_mdx(node)
            current_dict = parsed_data

    recursive_parse(docs_urls, parsed_docs)
    return parsed_docs