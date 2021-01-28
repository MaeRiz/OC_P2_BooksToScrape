import requests
from bs4 import BeautifulSoup
import os

url = 'http://books.toscrape.com/index.html'


def main():
    directorycreation()
    response = requests.get(url)
    if response.ok:
        catLinks = BeautifulSoup(response.text, features="html.parser")
        catLink = catLinks.find('ul',{'class': 'nav nav-list'}).find('ul').findAll('a')
        for i in range(len(catLink)):
            with open('books/' + catLink[i].text.replace('\n', '').replace(' ', '') + '.csv', 'w', encoding='utf-8') as file:
                file.write('product_page_url;universal_product_code;title;price_including_tax;price_excluding_tax;number_available;product_description;category;review_rating;image_url\n')
            print('Catégorie en cours de téléchargement : ' + catLink[i].text.replace('\n', '').replace(' ', '') + ' ' + str(i + 1) + '/' + str(len(catLink)))
            pagecat('http://books.toscrape.com/' + catLink[i].attrs['href'], catLink[i].text.replace('\n', '').replace(' ', ''))


#===================================================
#            Création des répertoires
#===================================================

def directorycreation():
    try:
        os.mkdir('books/')
        os.mkdir('imgs/')
    except OSError:
        pass
    else:
        pass


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
#       Récupérétion des infos d'un livre
#===================================================

def savebooks(link, cat):
    responseBookPage = requests.get(link)
    if responseBookPage.ok:
        with open('books/' + cat + '.csv', 'a', encoding='utf-8') as file:
            soup = BeautifulSoup(responseBookPage.text, features="html.parser")
            tds = soup.findAll('td')
            universalProductCode = tds[0].text.replace(',', '').replace(';', '')
            priceIncludingTax = tds[3].text.replace(',', '').replace(';', '')
            priceExcludingTax = tds[2].text.replace(',', '').replace(';', '')
            numberAvailable = tds[5].text.replace(',', '').replace(';', '')
            reviewRating = tds[6].text.replace(',', '').replace(';', '')
            title = soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text.replace(',', '').replace(';', '')
            productDescription = soup.find('article', {'class': 'product_page'}).findAll('p')[3].text.replace(',', '').replace(';', '')
            category = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].text.replace(',', '').replace(';', '')
            imageUrl = soup.find('div', {'class': 'item active'}).find('img').attrs['src'].replace('../..', 'http://books.toscrape.com')
            imagedownload(imageUrl, universalProductCode)
            file.write(link + ';' + universalProductCode + ';' + title + ';' + priceIncludingTax + ';' + priceExcludingTax + ';' + numberAvailable + ';' + productDescription + ';' + category + ';' + reviewRating + ';' + imageUrl + '\n')

#===================================================
#           Téléchargement d'image
#===================================================

def imagedownload(imageUrl, productCode):
    response = requests.get(imageUrl)
    file = open('imgs/' + productCode + '.jpg', "wb")
    file.write(response.content)
    file.close()

main()