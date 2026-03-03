import re

# Read file content
with open("questions.sql", "r", encoding="utf-8") as f:
    content = f.read()

# Regex pattern for links
pattern = r"https?://\S+"

# Find all links
links = re.findall(pattern, content)

# Print or save
# for link in links:
#     print(link)

import requests

def expand_link(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.url
    except Exception as e:
        return f"Error: {e}"

expanded_urls = list(map(expand_link, links))
print("Final URL:", expanded_urls)
