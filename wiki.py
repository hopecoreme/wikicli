import sys
import requests
import re
import os

def sanitize_filename(name):
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')

def get_summary(query):
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
    response = requests.get(url, headers={"User-Agent": "wiki-cli-python"})
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No summary available.")
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"HTTP error: {response.status_code}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python wiki.py <search term>")
        return

    query = " ".join(sys.argv[1:])
    summary = get_summary(query)

    if summary:
        filename = sanitize_filename(query) + ".txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{query.title()}:\n{summary}")
        print(f"Saved to: {os.path.abspath(filename)}")
    else:
        print("Page not found.")

if __name__ == "__main__":
    main()
