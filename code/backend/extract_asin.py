from pymongo import MongoClient
import os.path

client = MongoClient()
db = client.octopaul

min_epoch_time = 1420076973 #Jan 1st,2015 

categories = ["AmazonInstantVideo",
        "AppsForAndroid",
        "Automotive",
        "Baby",
        "Beauty",
        "CellPhones",
        "ClothingShoesJewelry",
        "DigitalMusic",
        "GroceryGourmetFood",
        "Health",
        "HomeKitchen",
        "KindleStore",
        "MoviesTV",
        "MusicalInstruments",
        "OfficeProducts",
        "PatioLawnGarden",
        "PetSupplies",
        "SportsOutdoors",
        "ToolsHomeImprovement",
        "ToysAndGames",
        "VideoGames"
]


def extract_asin(collection_name):
    asin_dict = {}
    coll = db[collection_name]
    cursor = coll.aggregate(
                        [
                            {
                                "$match" : {
                                    "unixReviewTime": { "$lt": min_epoch_time}
                                }
                             },
                             {  
                                "$project":
                                    {   "_id" : 0,
                                        "asin" : 1
                                    }
                             }
                        ]
                        )
    for document in cursor:
        key = document.values()[0].encode('ascii')
        asin_dict[key] = asin_dict.get(key,0) + 1
 
    filename = collection_name + "ASIN.dat"     
    f = open(os.path.join('../dat',filename),'w')
    count = 0
    for asin in sorted(asin_dict,key=asin_dict.get, reverse=True):
        f.write(asin)
        f.write('\n')
        count = count + 1
        if(count >= 1000):
            break
    f.close()       


def main():
    for c in categories: 
        extract_asin(c)    

if __name__ == "__main__":
    main()
