import argparse
import requests
import re
import shutil
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--out', default='images/', help='Folder where the images will be downloaded.')
parser.add_argument('-p', '--pages', default=166, type=int, help='Number of pages to scrap. 166 (all) by default.')
args = parser.parse_args()

out = args.out
end = args.pages

main_page = 'https://www.claudemonetgallery.org/'
url = main_page + 'the-complete-works.html?pageno='


def scrap(page_url):
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    images = soup.find_all('img', alt=re.compile('Claude'), src=re.compile('mini_small'))
    img_urls = []
    for image in images:
        img_urls.append(main_page + image.get('src'))

    for i, image in enumerate(img_urls):
        pos_slash = image.rfind('/') + 1
        pos_ques = image.rfind('?')
        img_name = image[pos_slash:pos_ques]

        response = requests.get(image, stream=True)
        with open(f'images/{img_name}', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response


def scrap_pages(first_page=0, last_page=5):
    for i in range(first_page, last_page+1):
        current_page = f'{url}{i}'
        scrap(current_page)


if __name__ == '__main__':
    scrap_pages(1, end)
