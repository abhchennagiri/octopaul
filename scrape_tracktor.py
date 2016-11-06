# Extracting historical data from "thetracktor.com" and saving the historical price of each product as a seperate json

import urllib2
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time, json, datetime
import csv
from itertools import izip

class Octopaul(object):
    def extract_tractor_info(self, response_json, resp_dict):
        #Ex:{ "prices": {"1469505600000.0": ["3104.25", "1095.00"]} ==> first item in
        # array is Amazon price; second is used price.
        #resp_array is of form [ [product1_dates], [product1_costs], [product2_dates], [product2_costs]]
        response_json = json.loads(response_json)
        if "prices" not in response_json:
            return
        return response_json["prices"]

    def extract_unimerc_info(self, response_json, resp_dict):
    	response_json = json.loads(response_json)
        if 'amazon' not in response_json:
            return
        prices = response_json['amazon'][0]
        print type(prices)
        for p in prices:
        	#print p
        	resp_dict[p[0]] = p[1]        
        

    def plot_graph(self, resp_array):
         f, axes = plt.subplots(len(resp_array), 1)
         for i in range(len(resp_array)):
            axes[i].plot(resp_array[i])
         #pplt.plot()
         plt.show()


    def write_to_file(self, product_id, resp_dict):
        output_file = str(product_id) + '.csv'
        sorted_keys = sorted(resp_dict)
        dates = []
        costs = []
        for key in sorted_keys:
        	isInt = False
        	if type(key) == 'int':
        		isInt = True
        	origKey = key
        	if len(str(key)) > 10:
        		key = str(key)[:10]
        	print key
        	date = datetime.datetime.fromtimestamp(float(key)).strftime('%Y-%m-%d')
        	dates.append(date)
        	if isInt:
        		origKey = int(origKey)
        	costs.append(resp_dict[origKey])

        with open(output_file, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(izip(dates, costs))


    def get_tractor_data(self, asin):
    	
            url = 'http://thetracktor.com/detail/' + asin + '/us/'
            print url
            content = urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)
            try:
                product_id = soup('input',{'id' : 'id_product'})[0]['value']
                product_name = soup.html.head.title.string

                #send GET request to get the JSON now
                url = 'https://thetracktor.com/ajax/prices/?id=' + str(product_id)
                print 'Price history URL: ' + url
                response_json = urllib2.urlopen(url).read()
                return response_json
            except IndexError:
                print 'Historical data not available for this product'

    def get_unimerc_data(self, asin):
    	
            url = 'http://www.unimerc.com/chart_output.php?sku=' + asin
            print url
            content = urllib2.urlopen(url).read()
            #soup = BeautifulSoup(content)
            try:
                #send GET request to get the JSON now
                response_json = urllib2.urlopen(url).read()
                return response_json[11:]
            except IndexError:
                print 'Historical data not available for this product'

    def get_price_history(self):
        file = open('sampleASIN.txt','r')
        asin_list = file.read().splitlines()

        # Getting JSON data of 10 products currently
        num_products = 10
        resp_dict = {}
        for i in xrange(num_products):
	        response_json = self.get_tractor_data(asin_list[i])
	        self.extract_tractor_info(response_json, resp_dict)
	        response_json = self.get_unimerc_data(asin_list[i])
	        self.extract_unimerc_info(response_json, resp_dict)
	        self.write_to_file(asin_list[i], resp_dict)


o = Octopaul()
o.get_price_history()
