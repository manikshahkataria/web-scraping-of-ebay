import csv
import requests
from bs4 import BeautifulSoup
def get_page(url):
    response=requests.get(url)
    #url has responded
    #print(response.ok)
    # 200 means server responded successfully
    #print(response.status_code)
    if not response.ok:
        print('server responded', response.status_code)
    else:
        soup=BeautifulSoup(response.text,'lxml')
    return soup
        # the first argument of BeautifulSoup(response.text,'lxml') response.text is the html code of a page
        # the second argument is the parser lxml
def get_detail_data(soup):
    #tittle, price ,item soid items
    try:
        h1=soup.find('h1',id='itemTitle')
        h=h1.text
        j=h.split('   ')
        title=j[1]
        #print(title)
    except:
        title=''
    try:
        price_data=soup.find('span',id='prcIsum').text.strip().split(' ')
        continent=price_data[0]
        #print(continent)
        price=price_data[1]
        #print(price[1:])
        currency=price[:1]
        #print(currency )
    except:
        price=''
    try:
        sold=soup.find('a',class_='vi-txt-underline').text.split(' ')[0]
        #print(sold)
    except:
        sold= 0
    data={
        'title':title,
        'price':price,
        #'currency':currency,
        'sold':sold

    }
    return data



def get_index_data(soup):
    #this will return all the links of the products
    #the link of eacg product will be passed one by one into the grt detail function to get data of every product
    try:
        links = soup.find_all('a',class_='s-item__link')
    except:
        links=[]

    urls=[item.get('href')for item  in links]
    return urls

def write_csv(data,url):
    with open('output.csv','a') as csvfile:
        writer= csv.writer(csvfile)
        row=[data['title'],data['price'],data['sold'], url]
        writer.writerow(row)


def main():
   # url='https://www.ebay.com/itm/Rolex-Datejust-31-Black-MOP-Jubilee-Diamond-Dial-Ladies-18kt-Yellow-Gold/183515884131?_trkparms=%26rpp_cid%3D5cb7586a7b34a72b115fe0a3%26rpp_icid%3D5cb7586a7b34a72b115fe0a2'

    #url='https://www.ebay.com/itm/SEIKO-SARB033-Mechanical-Automatic-Stainless-Steel-Mens-Watch-Made-In-Japan/254605873598?hash=item3b47b151be:g:y7EAAOSw4YZeyT62'
    url='https://www.ebay.com/sch/i.html?&_nkw=watches&_pgn=1'
    products= get_index_data(get_page(url))
    for link in products:
        data=get_detail_data(get_page(link))
        print(data)
        write_csv(data,link)

if __name__=='__main__':
     main()