import glob
import pandas as pd

#Finds all .csv files that start with "CRMLSListing"
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
