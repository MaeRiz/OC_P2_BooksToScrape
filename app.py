import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/index.html'


def main():
    response = requests.get(url)
    if response.ok:
        catLinks = BeautifulSoup(response.text, features="html.parser")
        catLink = catLinks.find('ul',{'class': 'nav nav-list'}).find('ul').findAll('a')
        for i in range(len(catLink)):
            with open('books_' + catLink[i].text.replace('\n', '').replace(' ', '') + '.csv', 'w', encoding='utf-8') as file:
                file.write('product_page_url;universal_product_code;title;price_including_tax;price_excluding_tax;number_available;product_description;category;review_rating;image_url\n')
            pagecat('http://books.toscrape.com/' + catLink[i].attrs['href'], catLink[i].text.replace('\n', '').replace(' ', ''))


#===================================================
#       Récupérétion des infos d'un livre
#===================================================

def savebooks(link, cat):
    responseBookPage = requests.get(link)
    if responseBookPage.ok:
        with open('books_' + cat + '.csv', 'a', encoding='utf-8') as file:
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
            file.write(link + ';' + universalProductCode + ';' + title + ';' + priceIncludingTax + ';' + priceExcludingTax + ';' + numberAvailable + ';' + productDescription + ';' + category + ';' + reviewRating + ';' + imageUrl + '\n')


#===================================================
#      Récupérétion des livres d'une catégorie
#===================================================

def onepage(link, cat):
    responsePage = requests.get(link)
    booksLinks = BeautifulSoup(responsePage.text, features="html.parser")
    findBeconne = booksLinks.findAll('div', {'class': 'image_container'})
    for i in range(len(findBeconne)):
        savebooks(findBeconne[i].find('a').attrs['href'].replace('../../..', 'http://books.toscrape.com/catalogue'), cat)


#===================================================
#       Traitement de la pagination
#===================================================

def pagecat(linkCat, cat):
    linkCat = linkCat.replace('index.html', 'page-1.html')
    responseCatPage = requests.get(linkCat)
    if responseCatPage.ok:
        i = 1
        while responseCatPage.ok:
            onepage(linkCat, cat)
            i = i + 1
            linkCat = linkCat.replace('page-' + str(i - 1) + '.html', 'page-' + str(i) + '.html')
            responseCatPage = requests.get(linkCat)
    else:
        linkCat = linkCat.replace('page-1.html', 'index.html')
        onepage(linkCat, cat)


main()