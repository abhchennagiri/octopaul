import datetime
import pandas as pd
import sys
import os
import csv
from itertools import izip

#input_file = "B0010E1M02.csv"

class FillMissingValues():
	def insert_missing_values(self, filename):
		df = pd.read_csv(filename,parse_dates=[0],infer_datetime_format=True,index_col=0)
		df=df.sort_index()
		df=df[~df.index.duplicated()]
		index2= pd.date_range(df.first_valid_index(), df.last_valid_index())
		df=df.reindex(index2, method='ffill')
		df.to_csv(filename+'.new',index_label='Time')
