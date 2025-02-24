import json

def generate_llms_txt(extracted_data, output_file='llms.txt'):
    """
    Generates llms.txt from the extracted documentation data.

    extracted_data: The structured data containing URLs, headings, code blocks, and function names.
    output_file: The name of the output file to write the formatted text.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        def write_section(section_name, section_data, indent_level=0):
            indent = '  ' * indent_level
            f.write(f"{indent}### Section: {section_name}\n")
            if 'url' in section_data:
                f.write(f"{indent}URL: {section_data['url']}\n\n")

            if 'headings' in section_data and section_data['headings']:
                f.write(f"{indent}#### Headings:\n")
                for heading in section_data['headings']:
                    f.write(f"{indent}- {heading}\n")
                f.write('\n')

            if 'code_blocks' in section_data and section_data['code_blocks']:
                f.write(f"{indent}#### Code Blocks:\n")
                for code in section_data['code_blocks']:
                    f.write(f"{indent}```\n{code}\n{indent}```\n")
                f.write('\n')

            if 'function_names' in section_data and section_data['function_names']:
                f.write(f"{indent}#### Function Names:\n")
                for func in section_data['function_names']:
                    f.write(f"{indent}- {func}\n")
                f.write('\n')

            # Recursively process nested sections
            for key, value in section_data.items():
                if isinstance(value, dict) and key not in ['url', 'headings', 'code_blocks', 'function_names']:
                    write_section(f"{section_name} -> {key}", value, indent_level + 1)

            f.write(f"{indent}---\n\n")

        for top_section, data in extracted_data.items():
            write_section(top_section, data)

    print(f"llms.txt has been successfully generated at '{output_file}'.")
