import requests, os, bs4


url = 'https://xkcd.com/'
os.makedirs('xkcd', exist_ok=True)
iterCnt = 0
while iterCnt in range(10) and not url.endswith('#'):
    # Download the page.
    print('Downloading page: %s...' % url)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features="html.parser")
    # Find the URL of comic image.
    comicElem = soup.select('#comic img')
    if comicElem == []:
        print('Could not find comic image.')
    else:
        imageUrl = 'http:' + comicElem[0].get('src')
    # Download the image.
    print('Downloading %sth image: %s' % (iterCnt + 1, imageUrl))
    comicRes = requests.get(imageUrl)
    comicRes.raise_for_status()
    # Save the image to ./xccd.
    imageFile = open(os.path.join('xkcd', os.path.basename(imageUrl)), 'wb')
    for chunk in comicRes.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()
    iterCnt += 1
    # Get the prev button's url.
    prevLink = soup.select('a[rel="prev"]')[0].get('href')
    url = 'https://xkcd.com' + prevLink
print('Done.')