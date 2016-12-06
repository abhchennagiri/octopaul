#!/bin/bash

dataPath="../../results"

echo "Automotive"
python createMeanErrorForCategory.py Automotive $dataPath/Automotive

# echo "AppsForAndroid"
# python createMeanErrorForCategory.py AppsForAndroid $dataPath/AppsForAndroid

echo "Baby"
python createMeanErrorForCategory.py Baby $dataPath/Baby

echo "Beauty"
python createMeanErrorForCategory.py Beauty $dataPath/Beauty

echo "CellPhones"
python createMeanErrorForCategory.py CellPhones $dataPath/CellPhones

echo "ClothingShoesJewelry"
python createMeanErrorForCategory.py ClothingShoesJewelry $dataPath/ClothingShoesJewelry

# echo "DigitalMusic"
# python createMeanErrorForCategory.py DigitalMusic $dataPath/DigitalMusic

# echo "GroceryGourmetFood"
# python createMeanErrorForCategory.py GroceryGourmetFood $dataPath/GroceryGourmetFood

echo "Health"
python createMeanErrorForCategory.py Health $dataPath/Health

echo "HomeKitchen"
python createMeanErrorForCategory.py HomeKitchen $dataPath/HomeKitchen

echo "KindleStore"
python createMeanErrorForCategory.py KindleStore $dataPath/KindleStore

# echo "MoviesTV"
# python createMeanErrorForCategory.py MoviesTV $dataPath/MoviesTV

echo "MusicalInstruments"
python createMeanErrorForCategory.py MusicalInstruments $dataPath/MusicalInstruments

echo "OfficeProducts"
python createMeanErrorForCategory.py OfficeProducts $dataPath/OfficeProducts

echo "PatioLawnGarden"
python createMeanErrorForCategory.py PatioLawnGarden $dataPath/PatioLawnGarden

echo "PetSupplies"
python createMeanErrorForCategory.py PetSupplies $dataPath/PetSupplies

echo "SportsOutdoors"
python createMeanErrorForCategory.py SportsOutdoors $dataPath/SportsOutdoors

echo "ToolsHomeImprovement"
python createMeanErrorForCategory.py ToolsHomeImprovement $dataPath/ToolsHomeImprovement

echo "ToysAndGames"
python createMeanErrorForCategory.py ToysAndGames $dataPath/ToysAndGames

# echo "VideoGames"
# python createMeanErrorForCategory.py VideoGames $dataPath/VideoGames

