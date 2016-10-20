# Extracting historical data from "thetracktor.com" and saving the historical price of each product as a seperate json

import urllib2
from bs4 import BeautifulSoup



def main():
    file = open('sampleASIN.txt','r')
    asin_list = file.read().splitlines()

    # Getting JSON data of 10 products currently
    num_products = 10 
    for i in xrange(num_products):
        url = 'http://thetracktor.com/detail/' + asin_list[i] + '/us/'
        print url
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content)
        try:
            product_id = soup('input',{'id' : 'id_product'})[0]['value']
            product_name = soup.html.head.title.string
    
            #send GET request to get the JSON now
            num_days = 90
            url = 'https://thetracktor.com/ajax/prices/?id=' + str(product_id) + '&days=' + str(num_days)
            response_json = urllib2.urlopen(url).read()
            output_file = product_name[30:] + '_' + str(product_id) + '.json'
            file = open(output_file,'w')
            file.write(response_json)
            file.close()
        except IndexError:  
            print 'Historical data not available for this product'

if __name__ == "__main__":
    main()
