import json
import re

def generate_llms_txt(extracted_data, output_file='llms.txt'):
    """
    Generates llms.txt from the extracted documentation data in the format:
    - [Title](URL): Description
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write the base URL as a header
        f.write("# Uniswap v4\n\n")


        def convert_github_url_to_docs_url(github_url):
            try:
                if 'raw.githubusercontent.com' in github_url:
                    # Extract the path after /docs/contracts/
                    parts = github_url.split('/docs/contracts/')
                    if len(parts) > 1:
                        path = parts[1]
                        path = re.sub(r'\.(mdx|md)$', '', path)
                        segments = path.split('/')
                        cleaned_segments = []
                        for segment in segments:
                            # Remove numeric prefixes like "01-", "1.""
                            cleaned = re.sub(r'^\d+[-.]\s*', '', segment)
                            cleaned_segments.append(cleaned)
                        path = '/'.join(cleaned_segments)
                        return f"https://docs.uniswap.org/contracts/{path}"
                return github_url
            except Exception as e:
                print(f"Error converting URL {github_url}: {e}")
                return github_url

        def process_entry(section_data, parent_sections=[]):
            if isinstance(section_data, dict):
                if 'url' in section_data and 'title' in section_data and 'description' in section_data:
                    # a document entry
                    title = section_data['title']
                    docs_url = convert_github_url_to_docs_url(section_data['url'])
                    description = section_data['description']
                    if description and not description.isspace():
                        # Clean up any relative links in the description
                        description = re.sub(r'\]\([./]+[^)]+\)', ')', description)
                        f.write(f"- [{title}]({docs_url}): {description}\n")
                else:
                    # section containing other documents
                    for title, value in section_data.items():
                        process_entry(value, parent_sections + [title] if parent_sections else [title])

        for section, data in extracted_data.items():
            process_entry(data, [section] if isinstance(data, dict) else [])

    print(f"llms.txt has been successfully generated at '{output_file}'.")
