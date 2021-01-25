import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/category/books/fiction_10/index.html'.replace('index.html', 'page-1.html')

response = requests.get(url)

with open('book.csv', 'w', encoding='utf-8') as file:
    file.write('product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url\n')


#===================================================
#       Récupérétion des infos d'un livre
#===================================================

def savebooks(link):
    responseBookPage = requests.get(link)
    if responseBookPage.ok:
        with open('book.csv', 'a', encoding='utf-8') as file:
            soup = BeautifulSoup(responseBookPage.text, features="html.parser")
            tds = soup.findAll('td')
            universalProductCode = tds[0].text
            priceIncludingTax = tds[3].text
            priceExcludingTax = tds[2].text
            numberAvailable = tds[5].text
            reviewRating = tds[6].text
            title = soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text
            productDescription = soup.find('article', {'class': 'product_page'}).findAll('p')[3].text.replace(',','')
            category = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].text
            imageUrl = soup.find('div', {'class': 'item active'}).find('img').attrs['src'].replace('../..', 'http://books.toscrape.com')
            file.write(link + ',' + universalProductCode + ',' + title + ',' + priceIncludingTax + ',' + priceExcludingTax + ',' + numberAvailable + ',' + productDescription + ',' + category + ',' + reviewRating + ',' + imageUrl + '\n')


def onepage(link):
    responsePage = requests.get(link)
    booksLinks = BeautifulSoup(responsePage.text, features="html.parser")
    findBeconne = booksLinks.findAll('div', {'class': 'image_container'})
    for i in range(len(findBeconne)):
        savebooks(findBeconne[i].find('a').attrs['href'].replace('../../..', 'http://books.toscrape.com/catalogue'))


if response.ok:
    i = 1
    while response.ok:
        onepage(url)
        i = i + 1
        url = url.replace('page-' + str(i - 1) + '.html', 'page-' + str(i) + '.html')
        response = requests.get(url)
else:
    url = url.replace('page-1.html', 'index.html')
    onepage(url)

