This repository includes code for extracting top 50 restaurant and bar lists for Philadelphia over several years, taken from Foobooz.  Each restaurant and bar is associated with a rank for each year, and is classified by location, cuisine and pricing features.

The goal is to use machine learning techniques to make predictions for future rankings and to determine whether there are any substructures to the data.

To run:

python GetRest.py --makelist [--rest | --bar | --oldrest | --oldbar]

--rest and --bar generate data for the current lists (2014) for restaurants and bars respectively.  --oldrest and --oldbar do the same for previous years.

Note: The data for restaurants exists only for 2014 and 2012; rankings are only done every two years.