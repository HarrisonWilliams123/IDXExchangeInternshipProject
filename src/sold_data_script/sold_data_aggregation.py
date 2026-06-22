import glob
import pandas as pd

#Finds all .csv files that start with "CRMLSSold"
sold_file_pattern = "data/CRMLSSold*.csv"
all_sold_files = glob.glob(sold_file_pattern)

#Initialize an empty list to store the individual data frames
sold_df_list = []

#Initialize an empty list to find the average of entries before
total_entries = []

#Use a for loop to read each file and add it to the list
for filename in all_sold_files:
    sold_df = pd.read_csv(filename)
    #Adds the amount of rows before
    total_entries.append(len(sold_df))
    sold_df_list.append(sold_df)

#Concatenates all data frames to create final sold data frame
combined_sold_df = pd.concat(sold_df_list, ignore_index=True)

#Removes the last two columns in the data frame (extra columns)
combined_sold_df = combined_sold_df.drop(columns=['latfilled', 'lonfilled'])

#Prints the amount of rows after
print(round(sum(total_entries) / len(total_entries), 0))
print(len(combined_sold_df))

#Before total amount of rows before concatenation: 21987 rows
#After total amount of rows after concatenation: 681599 rows

#Filters the Property Type to 'Residential' only
combined_sold_df = combined_sold_df[combined_sold_df['PropertyType'] == 'Residential']

#Prints the amount of rows after the filter
print(len(combined_sold_df))

#Before total amount of rows before filter: 681599 rows
#After total amount of rows after filter: 458336 rows

#Save the combined data frame to a new .csv file
combined_sold_df.to_csv("combined_datasets/combined_sold_df.csv", index=False)

