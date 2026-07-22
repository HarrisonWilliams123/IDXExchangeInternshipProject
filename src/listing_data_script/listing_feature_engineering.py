import pandas as pd
import numpy as np

#Reads the .csv file 
list = pd.read_csv("filtered_datasets/list_cleaned.csv")

#Convert these to datetimes again, since .csv files don't save the data type
list['CloseDate'] = pd.to_datetime(list['CloseDate'], errors='coerce')
list['PurchaseContractDate'] = pd.to_datetime(list['PurchaseContractDate'], errors='coerce')
list['ListingContractDate'] = pd.to_datetime(list['ListingContractDate'], errors='coerce')

#Feature Engineering
list['Price Ratio'] = list['ClosePrice'] / list['OriginalListPrice']
list['Price Per Sq Ft'] = list['ClosePrice'] / list['LivingArea']
list['Days On Market'] = list['DaysOnMarket']
list['close_year'] = list['CloseDate'].dt.year
list['close_month'] = list['CloseDate'].dt.month
list['close_yrmo'] = list['CloseDate'].dt.to_period('M').astype(str)
list['Close to Original List Ratio'] = list['ClosePrice'] / list['OriginalListPrice']
list['Listing to Contract Days'] = list['PurchaseContractDate'] - list['ListingContractDate']
list['Contract to Close Days'] = list['CloseDate'] - list['PurchaseContractDate']

#Sample Output Table for the engineered metrics
sample_cols = [
    'Price Ratio', 'Price Per Sq Ft', 'Days On Market',
    'close_year', 'close_month', 'close_yrmo',
    'Close to Original List Ratio', 'Listing to Contract Days',
    'Contract to Close Days'
]

print("Sample Engineered Metrics Table:")
print(list[sample_cols].head(10))

#Segmented Summary by CountyOrParish
segment_group = list.groupby('CountyOrParish').agg({
    'ClosePrice': ['count', 'mean', 'median'],
    'Price Ratio': 'mean',
    'Price Per Sq Ft': 'mean',
    'Days On Market': 'mean',
    'Listing to Contract Days': 'mean',
    'Contract to Close Days': 'mean'
})

print("Segmented Summary by CountyOrParish")
print(segment_group)

list.to_csv("filtered_datasets/feature_engineering_list_data.csv", index=False)