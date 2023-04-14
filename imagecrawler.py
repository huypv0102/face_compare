import requests
from bs4 import BeautifulSoup

url = input("URL:")
URL = url  # Replace this with the website's URL
getURL = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(getURL.text, 'html.parser')
print(soup)
images = soup.find_all('img')
print(images)
resolvedURLs = []
for image in images:
    src = image.get('src')
    print(src)
    resolvedURLs.append(requests.compat.urljoin(URL, src))

for image in resolvedURLs:
    if("data" in image):
        continue
    webs = requests.get(image)
    open('images/' + image.split('/')[-1], 'wb').write(webs.content)
