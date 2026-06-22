import glob
import pandas as pd

#Finds all CSV that start with "CRMLSListing"
listing_file_pattern = "data/CRMLSListing*.csv"
all_listing_files = glob.glob(listing_file_pattern)

#Initialize an empty list to store the individual data frames
listing_df_list = []

#Use a for loop to read each file and add it to the list
for filename in all_listing_files:
    listing_df = pd.read_csv(filename)
    listing_df_list.append(listing_df)

#Concatenates all data frames to create final listing data frame
combined_listing_df = pd.concat(listing_df_list, ignore_index=True)

#Save the combined data frame to a new .csv file
combined_listing_df.to_csv("combined_listing_df.csv", index=False)

#Repeat the same process for "CRMLSSold"
sold_file_pattern = "data/CRMLSSold*.csv"
all_sold_files = glob.glob(sold_file_pattern)

sold_df_list = []

for filename in all_sold_files:
    sold_df = pd.read_csv(filename)
    sold_df_list.append(sold_df)

combined_sold_df = pd.concat(sold_df_list, ignore_index=True)

combined_sold_df.to_csv("combined_sold_df.csv", index=False)

