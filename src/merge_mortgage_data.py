import pandas as pd

sold = pd.read_csv("combined_datasets/combined_sold_df.csv")
listing = pd.read_csv("combined_datasets/combined_listing_df.csv")

#Fetch the mortgage rate data from FRED
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']

#Resample weekly rates to monthly averages
mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (
    mortgage.groupby('year_month')['rate_30yr_fixed']
    .mean()
    .reset_index()
)

#Create a matching year_month key on the MLS datasets

#Sold Dataset - key off CloseDate
sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')

#Listing Dataset = key off ListingContractDate
listing['year_month'] = pd.to_datetime(
    listing['ListingContractDate']
).dt.to_period('M')

#Merge 
sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left')
listing_with_rates = listing.merge(mortgage_monthly, on='year_month', how='left')

#Validate the merge
#Check for any unmatched rows (rate should not be null)
print(sold_with_rates['rate_30yr_fixed'].isnull().sum())
print(listing_with_rates['rate_30yr_fixed'].isnull().sum())
print(
    sold_with_rates[
        ['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']
    ].head()
)

#Saves new .csv files
sold_with_rates.to_csv("combined_datasets/sold_with_rates.csv", index=False)
listing_with_rates.to_csv("combined_datasets/listings_with_rates.csv", index=False)



