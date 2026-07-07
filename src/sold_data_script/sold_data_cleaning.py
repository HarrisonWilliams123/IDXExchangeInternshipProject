import pandas as pd

#Reads the csv file to begin editing
sold = pd.read_csv("combined_datasets/sold_with_rates.csv")

#Changes the date fields (CloseDate, PurchaseContractDate, ListingContractDate, ContractStatusChangeDate) to datetime format
sold['CloseDate'] = pd.to_datetime(sold['CloseDate'])
sold['PurchaseContractDate'] = pd.to_datetime(sold['PurchaseContractDate'])
sold['ListingContractDate'] = pd.to_datetime(sold['ListingContractDate'])
sold['ContractStatusChangeDate'] = pd.to_datetime(sold['ContractStatusChangeDate'])

#Drops the redundant rows
sold = sold.drop_duplicates()

