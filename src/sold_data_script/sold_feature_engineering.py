import pandas as pd
import numpy as np

#Reads the .csv file 
sold = pd.read_csv("filtered_datasets/sold_cleaned.csv")

#Convert these to datetimes again, since .csv files don't save the data type
sold['CloseDate'] = pd.to_datetime(sold['CloseDate'], errors='coerce')
sold['PurchaseContractDate'] = pd.to_datetime(sold['PurchaseContractDate'], errors='coerce')
sold['ListingContractDate'] = pd.to_datetime(sold['ListingContractDate'], errors='coerce')

#Feature Engineering
sold['Price Ratio'] = sold['ClosePrice'] / sold['OriginalListPrice']
sold['Price Per Sq Ft'] = sold['ClosePrice'] / sold['LivingArea']
sold['Days On Market'] = sold['DaysOnMarket']
sold['close_year'] = sold['CloseDate'].dt.year
sold['close_month'] = sold['CloseDate'].dt.month
sold['close_yrmo'] = sold['CloseDate'].dt.to_period('M').astype(str)
sold['Close to Original List Ratio'] = sold['ClosePrice'] / sold['OriginalListPrice']
sold['Listing to Contract Days'] = sold['PurchaseContractDate'] - sold['ListingContractDate']
sold['Contract to Close Days'] = sold['CloseDate'] - sold['PurchaseContractDate']

#Sample Output Table for the engineered metrics
sample_cols = [
    'Price Ratio', 'Price Per Sq Ft', 'Days On Market',
    'close_year', 'close_month', 'close_yrmo',
    'Close to Original List Ratio', 'Listing to Contract Days',
    'Contract to Close Days'
]

print("Sample Engineered Metrics Table:")
print(sold[sample_cols].head(10))

#Segmented Summary by CountyOrParish
segment_group = sold.groupby('CountyOrParish').agg({
    'ClosePrice': ['count', 'mean', 'median'],
    'Price Ratio': 'mean',
    'Price Per Sq Ft': 'mean',
    'Days On Market': 'mean',
    'Listing to Contract Days': 'mean',
    'Contract to Close Days': 'mean'
})

print("Segmented Summary by CountyOrParish")
print(segment_group)

sold.to_csv("filtered_datasets/feature_engineering_sold_data.csv", index=False)