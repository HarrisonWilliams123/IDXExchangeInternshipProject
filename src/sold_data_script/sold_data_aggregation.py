import glob
import pandas as pd

#Finds all .csv files that start with "CRMLSSold"
sold_file_pattern = "data/CRMLSSold*.csv"
all_sold_files = glob.glob(sold_file_pattern)

#Initialize an empty list to store the individual data frames
sold_df_list = []

#Use a for loop to read each file and add it to the list
for filename in all_sold_files:
    sold_df = pd.read_csv(filename)
    sold_df_list.append(sold_df)

#Concatenates all data frames to create final sold data frame
combined_sold_df = pd.concat(sold_df_list, ignore_index=True)

#Save the combined data frame to a new .csv file
combined_sold_df.to_csv("combined_sold_df.csv", index=False)

