import pandas as pd
import numpy as np

#Reads the csv file to begin editing
sold = pd.read_csv("combined_datasets/sold_with_rates.csv")
original_len = len(sold)

#Changes the date fields (CloseDate, PurchaseContractDate, ListingContractDate, ContractStatusChangeDate) to datetime format
sold['CloseDate'] = pd.to_datetime(sold['CloseDate'])
sold['PurchaseContractDate'] = pd.to_datetime(sold['PurchaseContractDate'])
sold['ListingContractDate'] = pd.to_datetime(sold['ListingContractDate'])
sold['ContractStatusChangeDate'] = pd.to_datetime(sold['ContractStatusChangeDate'])

numeric_cols = [
    'OriginalListPrice', 'ClosePrice', 'LivingArea', 'ListPrice',
    'DaysOnMarket', 'BathroomsTotalInteger', 'BedroomsTotal',
    'LotSizeAcres', 'LotSizeSquareFeet', 'YearBuilt',
    'StreetNumberNumeric', 'LotSizeArea'
]

#Converts the numeric fields to the numeric dtype
for col in numeric_cols:
    sold[col] = pd.to_numeric(sold[col], errors='coerce')

cols_to_drop = [
    'ListAgentFirstName', 'ListAgentLastName', 'BuyerAgentFirstName',
    'BuyerAgentLastName', 'ListAgentEmail', 'BuyerAgentMlsId',
    'CoListAgentFirstName', 'CoListAgentLastName', 'CoBuyerAgentFirstName'
]

#Removes unnecessary or redundant columns
sold = sold.drop(columns=cols_to_drop, errors='ignore')

#Handle missing values - categorical nulls with "Unknown"
cat_cols = ['City', 'CountyOrParish', 'StateOrProvince']
for col in cat_cols:
    sold[col] = sold[col].fillna("Unknown")

#Handles missing values - numeric fields with median
for col in numeric_cols:
    sold[col] = sold[col].fillna(sold[col].median())

#Flags invalid numeric values
sold['invalid_closeprice_flag'] = sold['ClosePrice'] <= 0
sold['invalid_livingarea_flag'] = sold['LivingArea'] <= 0
sold['invalid_days_flag'] = sold['DaysOnMarket'] < 0
sold['invalid_beds_flag'] = sold['BedroomsTotal'] < 0
sold['invalid_baths_flag'] = sold['BathroomsTotalInteger'] < 0

#Timeline consistency flags
sold['listing_after_close_flag'] = sold['ListingContractDate'] > sold['CloseDate']
sold['purchase_after_close_flag'] = sold['PurchaseContractDate'] > sold['CloseDate']
sold['negative_timeline_flag'] = sold['PurchaseContractDate'] < sold['ListingContractDate']

#Geographic data checks
sold['missing_coords_flag'] = sold['Latitude'].isna() | sold['Longitude'].isna()
sold['zero_coords_flag'] = (sold['Latitude'] == 0) | (sold['Longitude'] == 0)
sold['invalid_longitude_flag'] = sold['Latitude'] > 0
sold['implausible_coords_flag'] = ~(
    sold['Latitude'].between(32,42) &
    sold['Longitude'].between(-124, -114)
)

#Before/after row counts
print("Before cleaning:", original_len)
print("After cleaning:", len(sold))

#Print statement to confirm data types
print(sold.dtypes)

sold.to_csv("filtered_datasets/sold_cleaned.csv", index=False)