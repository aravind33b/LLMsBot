import requests
import re
import frontmatter

def fetch_and_parse_mdx(url):
    """
    Fetches the content of an .mdx or .md file from a given URL and extracts title and description.
    Returns None if fetch fails.
    """
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}")
            return None

        content = response.text

        # Try to extract title from frontmatter or first heading
        title = None
            
        if not title:
            if not re.match(r'^\s*---\s*(\n.*?)*?\s*---\s*\n', content, re.DOTALL):
                # Try first h1 heading that's not generic
                headings = re.findall(r'^#\s+(.+?)(?:\n|$)', content, re.MULTILINE)
                for heading in headings:
                    heading = heading.strip()
                    if not any(generic.lower() in heading.lower() for generic in ['introduction', 'guide', 'overview', 'quick start', 'requires']):
                        title = heading
                        break
            else:
                title = frontmatter.loads(content)['title']

        description = None
        desc_match = re.search(r'^description:\s*["\'](.+?)["\']', content, re.MULTILINE)
        if not desc_match:
            # Look for first non-empty paragraph after title that's not a heading or a code block
            paragraphs = re.findall(r'\n\n(?!#|\s*```|<)([^#\n][^\n]+(?:\n(?!#|\n)[^\n]+)*)', content)
            if paragraphs:
                description = ' '.join(paragraphs[0].strip().split())
            else:
                # Use first non-empty line that's not a heading as fallback
                lines = [line.strip() for line in content.split('\n') 
                        if line.strip() and not line.startswith('#') 
                        and not line.startswith('```')]
                description = ' '.join(lines[0].split()) if lines else f"Documentation for {title}"
        else:
            description = desc_match.group(1).strip()

        # Clean up description
        description = description.replace('\n', ' ').strip()
        description = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', description)

        return {
            "url": url,
            "title": title,
            "description": description
        }
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

def process_all_docs(docs_urls):
    """
    Process all documentation URLs and extract their content.
    """
    processed_docs = {}

    def process_entry(title, value, current_dict):
        if isinstance(value, str):
            parsed_data = fetch_and_parse_mdx(value)
            if parsed_data:
                current_dict[title] = parsed_data
        elif isinstance(value, dict):
            current_dict[title] = {}
            for sub_title, sub_value in value.items():
                process_entry(sub_title, sub_value, current_dict[title])

    for title, value in docs_urls.items():
        process_entry(title, value, processed_docs)

    return processed_docs