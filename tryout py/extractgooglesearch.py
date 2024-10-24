import requests
from bs4 import BeautifulSoup

prompt = 'Software Engineering Geek for Geeks'
url = 'https://www.google.com/search?q=' + prompt

# Add a User-Agent header to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

# Use more general selectors
results = soup.select('div.g')

for result in results:
    title_elem = result.select_one('h3')
    link_elem = result.select_one('a')
    snippet_elem = result.select_one('div.VwiC3b')
    
    if title_elem and link_elem and snippet_elem:
        title = title_elem.get_text()
        link = link_elem.get('href')
        snippet = snippet_elem.get_text()
        
        print(f'Title: {title}')
        print(f'Link: {link}')
        print(f'Snippet: {snippet}')
        print()
    else:
        print("Couldn't find all elements for this result")
        print()