import glob
import pandas as pd

#Finds all .csv files that start with "CRMLSListing"
listing_file_pattern = "data/CRMLSListing*.csv"
all_listing_files = glob.glob(listing_file_pattern)

#Initialize an empty list to store the individual data frames
listing_df_list = []

#Initialize an empty list to find the average of entries before
total_entries = []

#Use a for loop to read each file and add it to the list
for filename in all_listing_files:
    listing_df = pd.read_csv(filename)
    #Adds the amount of rows before
    total_entries.append(len(listing_df))
    listing_df_list.append(listing_df)

#Concatenates all data frames to create final listing data frame
combined_listing_df = pd.concat(listing_df_list, ignore_index=True)

#Prints the amount of rows after
print(round(sum(total_entries) / len(total_entries), 0))
print(len(combined_listing_df))

#Before total amount of rows before concatenation: 31914 rows
#After total amount of rows after concatenation: 893594 rows

#Filters the Property Type to 'Residential' only
combined_listing_df = combined_listing_df[combined_listing_df['PropertyType'] == 'Residential']

#Prints the amount of rows after the filter
print(len(combined_listing_df))

#Before total amount of rows before filter: 893594 rows
#After total amount of rows after filter: 567549 rows

#Save the combined data frame to a new .csv file
combined_listing_df.to_csv("combined_datasets/combined_listing_df.csv", index=False)
