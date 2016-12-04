# Add the missing data points
import datetime
import pandas as pd
import sys 

#input_file = "B0010E1M02.csv"

data=pd.read_csv(sys.argv[1]) 
array=data.values


def print_missing_points(date1,date2,price):
    while(date1 > date2):
        print str(date2) + ","+ str(price)
        date2 = date2 + datetime.timedelta(days=1)


def insert_missing_points(array):
    i = 0
    print "Time" + "," + "Price"
    while (i < len(array) - 1):
        #dates and prices in string
        d1  = array[i][0]
        p1 = array[i][1]
        d2 = array[i+1][0]
        p2 = array[i+1][1]
        
        #convert the dates to datetime object
        cur_day = datetime.date(*(int(s) for s in d1.split('-')))
        second_day = datetime.date(*(int(s) for s in d2.split('-')))
        next_day = cur_day + datetime.timedelta(days=1)

        #Check if there are repeating element
        if(str(cur_day) == str(second_day)):
            pass
        #Check if the points are continous
        elif(str(cur_day) != str(second_day) and str(second_day) == str(next_day)):
            print str(cur_day) + "," + str(p1)

        #Check if the points are not continous and print the missing values if they arent     
        elif(str(second_day) != str(next_day)):
            print str(cur_day) + "," + str(p1)
            print_missing_points(second_day,next_day,p2)
            
        else:
            print "This condition should not be hit"

        i = i + 1 
        
      
insert_missing_points(array)



