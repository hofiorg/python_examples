#!/usr/bin/env python3
"""
This module checks URLs defined in a JSON file. For each URL, it verifies if the response
contains a specific string and prints the result using emojis to indicate success or failure.
"""

import json
import sys
import requests

def read_json_file(file_path):
    """Read and return the content of the JSON file using UTF-8 encoding."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON file.")
        sys.exit(1)

def check_urls(url_data):
    """Check each URL for a specific string (or status 200 if 'contains' is not set) and print the result using emojis."""
    if 'urls' in url_data:
        for item in url_data['urls']:
            name = item['name']
            url = item['url']
            contains = item.get('contains', None)
            try:
                response = requests.get(url, timeout=10)
                if contains:
                    if contains in response.text:
                        print(f"✅ {name} - {url}")
                    else:
                        print(f"❌ {name} - {url}")
                else:
                    # If 'contains' is not provided, check if the status code is 200
                    if response.status_code == 200:
                        print(f"✅ {name} - {url}")
                    else:
                        print(f"❌ {name} - {url} - status {response.status_code}")
            except requests.RequestException as e:
                print(f"❌ {name} - {url} - failed to retrieve (error: {e})")
    else:
        print("No 'urls' key found in the JSON data.")

if __name__ == "__main__":
    # Ensure a file path is provided
    if len(sys.argv) < 2:
        print("Usage: ./check_urls.py <path_to_json_file>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    json_data = read_json_file(json_file_path)

    # Check URLs
    check_urls(json_data)
