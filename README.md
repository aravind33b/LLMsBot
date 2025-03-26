# LLMs.txt generator Bot
This bot scrapes v4 documentation and generates an LLMs.txt file

## Flow
1. Main.py makes a call to fetch_github_files and fetches the list of .mdx and .md files in v4 documentation repo (https://github.com/Uniswap/docs/tree/main/docs/contracts/v4)
2. The resultant data which has the list of github gist file links for every functionality is then sent to process_all_docs to parse the data.
3. Then parsed data is then pushed into extracted_data.json file before generate_llms_txt function generates the resultant llms.txt file

## Steps to run this project
1. Copy the .env.example file and rename it to .env and add the necessary keys
2. Run
```
python3 main.py
```

## Note: This is the initial version and needs improvement