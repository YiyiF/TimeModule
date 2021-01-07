#! /usr/bin/env python3

# scheduledDownloadImage.py - Check the comic web everyday.
#       If new comics posted since last check, download them.

import requests, os, bs4


def generateImageURL(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features="html.parser")
    # Find the URL of latest comic image.
    comicElem = soup.select('#comic img')
    if not comicElem:
        print('Could not find comic image.')
        return
    else:
        imageUrl = 'http:' + comicElem[0].get('src')
    prevLink = soup.select('a[rel="prev"]')[0].get('href')
    return imageUrl, prevLink


def hasUpdateToday(lastComicElemURL):
    URIFile = open('lastImageURI.txt')
    fileContent = URIFile.read()
    URIFile.close()
    if lastComicElemURL == fileContent:
        return False
    else:
        return True


def run():
    url = 'https://xkcd.com/'
    os.makedirs('xkcd', exist_ok=True)
    imageUrl, prevLink = generateImageURL(url)
    latestURL = imageUrl

    while hasUpdateToday(imageUrl) and not url.endswith('#'):
        # Download the image.
        print('Downloading image: %s' % imageUrl)
        comicRes = requests.get(imageUrl)
        comicRes.raise_for_status()
        # Save the image to ./xccd.
        imageFile = open(os.path.join('xkcd', os.path.basename(imageUrl)), 'wb')
        for chunk in comicRes.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
        # Get the prev page.
        url = 'https://xkcd.com' + prevLink
        imageUrl, prevLink = generateImageURL(url)
    URIFile = open('lastImageURI.txt', 'w')
    if URIFile.write(latestURL):
        print('Write %s done.' % latestURL)
    URIFile.close()


if __name__ == '__main__':
    run()
