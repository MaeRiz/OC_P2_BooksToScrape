import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/my-paris-kitchen-recipes-and-stories_910/index.html'

response = requests.get(url)

if response.ok:
    with open('book.csv', 'w', encoding='utf-8') as file:
        file.write('product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url\n')
        soup = BeautifulSoup(response.text, features="html.parser")
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

        file.write(url + ',' + universalProductCode + ',' + title + ',' + priceIncludingTax + ',' + priceExcludingTax + ',' + numberAvailable + ',' + productDescription + ',' + category + ',' + reviewRating + ',' + imageUrl)
        