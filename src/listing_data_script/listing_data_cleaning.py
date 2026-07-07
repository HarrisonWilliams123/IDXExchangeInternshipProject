import pandas as pd
import numpy as np

#Reads the csv file to begin editing
list = pd.read_csv("combined_datasets/sold_with_rates.csv")
original_len = len(list)

#Changes the date fields (CloseDate, PurchaseContractDate, ListingContractDate, ContractStatusChangeDate) to datetime format
list['CloseDate'] = pd.to_datetime(list['CloseDate'])
list['PurchaseContractDate'] = pd.to_datetime(list['PurchaseContractDate'])
list['ListingContractDate'] = pd.to_datetime(list['ListingContractDate'])
list['ContractStatusChangeDate'] = pd.to_datetime(list['ContractStatusChangeDate'])

numeric_cols = [
    'OriginalListPrice', 'ClosePrice', 'LivingArea', 'ListPrice',
    'DaysOnMarket', 'BathroomsTotalInteger', 'BedroomsTotal',
    'LotSizeAcres', 'LotSizeSquareFeet', 'YearBuilt',
    'StreetNumberNumeric', 'LotSizeArea'
]

#Converts the numeric fields to the numeric dtype
for col in numeric_cols:
    list[col] = pd.to_numeric(list[col], errors='coerce')

cols_to_drop = [
    'ListAgentFirstName', 'ListAgentLastName', 'BuyerAgentFirstName',
    'BuyerAgentLastName', 'ListAgentEmail', 'BuyerAgentMlsId',
    'CoListAgentFirstName', 'CoListAgentLastName', 'CoBuyerAgentFirstName'
]

#Removes unnecessary or redundant columns
list = list.drop(columns=cols_to_drop, errors='ignore')

#Handle missing values - categorical nulls with "Unknown"
cat_cols = ['City', 'CountyOrParish', 'StateOrProvince']
for col in cat_cols:
    list[col] = list[col].fillna("Unknown")

#Handles missing values - numeric fields with median
for col in numeric_cols:
    list[col] = list[col].fillna(list[col].median())

#Flags invalid numeric values
list['invalid_closeprice_flag'] = list['ClosePrice'] <= 0
list['invalid_livingarea_flag'] = list['LivingArea'] <= 0
list['invalid_days_flag'] = list['DaysOnMarket'] < 0
list['invalid_beds_flag'] = list['BedroomsTotal'] < 0
list['invalid_baths_flag'] = list['BathroomsTotalInteger'] < 0

#Timeline consistency flags
list['listing_after_close_flag'] = list['ListingContractDate'] > list['CloseDate']
list['purchase_after_close_flag'] = list['PurchaseContractDate'] > list['CloseDate']
list['negative_timeline_flag'] = list['PurchaseContractDate'] < list['ListingContractDate']

#Geographic data checks
list['missing_coords_flag'] = list['Latitude'].isna() | list['Longitude'].isna()
list['zero_coords_flag'] = (list['Latitude'] == 0) | (list['Longitude'] == 0)
list['invalid_longitude_flag'] = list['Latitude'] > 0
list['implausible_coords_flag'] = ~(
    list['Latitude'].between(32,42) &
    list['Longitude'].between(-124, -114)
)

#Before/after row counts
print("Before cleaning:", original_len)
print("After cleaning:", len(list))

#Print statement to confirm data types
print(list.dtypes)

list.to_csv("filtered_datasets/list_cleaned.csv", index=False)