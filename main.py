import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client
from supabase.client import ClientOptions
from github_integration import fetch_github_files
from docs_parser import process_all_docs
from llms_txt_generator import generate_llms_txt

def get_data_from_functions_table(supabase):
    response = (
    supabase.table("functions")
    .select("*")
    .execute()
)
    print(response)

def main():

    load_dotenv()

    # fetch all .mdx files
    file_list = fetch_github_files("uniswap", "docs", "docs/contracts/v4")
    
    # extract data from .mdx files
    parsed_docs = process_all_docs(file_list)

    try:
        output_file = os.path.abspath('extracted_data.json')
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(parsed_docs, file, indent=2)
        print(f"Extracted data saved to {output_file}")
    except Exception as e:
        print(f"Error writing extracted data: {e}")
        return

    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            extracted_data = json.load(file)
        print("Successfully read extracted_data.json")
    except FileNotFoundError:
        print(f"File {output_file} not found after writing.")
        return
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return

    # generate llms.txt
    try:
        generate_llms_txt(extracted_data)
    except Exception as e:
        print(f"Error generating llms.txt: {e}")

main()