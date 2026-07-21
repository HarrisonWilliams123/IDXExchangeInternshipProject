import pandas as pd
import numpy as np

#Reads the csv file to begin editing
list = pd.read_csv("combined_datasets/sold_with_rates.csv")
original_len = len(list)

#Removes the rows with >90% Missing Values
threshold = int(list.shape[1] * 0.10)
list = list[list.count(axis=1) >= threshold]

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
list['invalid_longitude_flag'] = list['Longitude'] > 0
list['implausible_coords_flag'] = ~(
    list['Latitude'].between(32,42) &
    list['Longitude'].between(-124, -114)
)

#Summary Reports
print("Row Counts:")
print("Original Rows:", original_len)
print("Final rows after full cleaning:", len(list))
print()

print("Data Types:")
print(list.dtypes)
print()

print("Date Consistency Flag Counts:")
print("Listing after close:", list['listing_after_close_flag'].sum())
print("Purchase after close:", list['purchase_after_close_flag'].sum())
print("Negative timeline:", list['negative_timeline_flag'].sum())
print()

print("Geographic Data Quality Summary:")
print("Missing coordinates:", list['missing_coords_flag'].sum())
print("Zero coordinates:", list['zero_coords_flag'].sum())
print("Invalid longitude (>0):", list['invalid_longitude_flag'].sum())
print("Implausible coordinates:", list['missing_coords_flag'].sum())

list.to_csv("filtered_datasets/list_cleaned.csv", index=False)