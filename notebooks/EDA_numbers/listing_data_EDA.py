import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

listing_data = pd.read_csv("data/unfiltered_listing_df.csv")

#Inspects the sturcture of the data
print(listing_data.columns)
print(listing_data.head())

#Prints the property categories
print(listing_data['PropertyType'].unique())

#Answers the question, "What is the Residential vs. other property type share?"
print(listing_data['PropertyType'].value_counts(normalize=True) * 100)

#Filters data to residential only
listing_data = listing_data[listing_data['PropertyType'] == 'Residential']

#Answers the question, "What are the median and average close prices?"
print("Median: " + str(listing_data['ClosePrice'].median()))
print("Average: " + str(listing_data['ClosePrice'].mean()))

#For the question, "What does the Days on Market distribution look like?",
#look at hist_DaysOnMarket.png, box_DaysOnMarket.png, and summary.loc[:, 'DaysOnMarket']

#Answers the question, "What percentage of homes sold above vs. below list price?"
listing_data['PriceRatio'] = listing_data['ClosePrice'] / listing_data['ListPrice']

above = (listing_data['PriceRatio'] > 1).mean() * 100
below = (listing_data['PriceRatio'] < 1).mean() * 100

print("Above list:", above)
print("Below list:", below)

#Answers the question, "Are there any apparent date consistency issues?"
listing_data['CloseDate'] = pd.to_datetime(listing_data['CloseDate'])
listing_data['ListingContractDate'] = pd.to_datetime(listing_data['ListingContractDate'])

invalid_dates = listing_data[listing_data['CloseDate'] < listing_data['ListingContractDate']]
print(invalid_dates)

#Answers the question, "Which counties have the highest median prices?"
print(listing_data.groupby('CountyOrParish')['ClosePrice'].median().sort_values(ascending=False))

#Prints out Null count summary and flags a column for 90% missing
null_counts = listing_data.isnull().sum().sort_values(ascending=False)
null_percent = (null_counts / len(listing_data)) * 100

missing_report = pd.DataFrame({
    "NullCount": null_counts,
    "PercentNull": null_percent,
    "Flag_90pct": null_percent > 90
})

print(missing_report)

#Creates an array for the numeric fields to analyze
numeric_fields = [
    'ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea',
    'LotSizeAcres', 'BedroomsTotal', 'BathroomsTotalInteger',
    'DaysOnMarket', 'YearBuilt'
]


#Percentile Summary
summary = listing_data[numeric_fields].describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
print(summary)

#Prints Histograms and Boxplots for each numeric field
for col in numeric_fields:
    #Creates the histograms
    plt.figure(figsize=(10, 5), layout="constrained")
    plt.hist(listing_data[col].dropna(), bins=40, color='skyblue', edgecolor='black')
    plt.title(f"Histogram of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"reports/numeric_plots/listing_hist_{col}.png", dpi=300)
    plt.close()

    #Creates the box plots
    plt.figure(figsize=(10,5))
    sns.boxplot(x=listing_data[col], color='orange')
    plt.title(f"Boxplot of {col}")
    plt.tight_layout()
    plt.savefig(f"reports/numeric_plots/listing_box_{col}.png", dpi=300)
    plt.close()

#Identifies extreme outliers using the IQR method
outlier_report = {}

for col in numeric_fields:
    q1 = listing_data[col].quantile(0.25)
    q3 = listing_data[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = listing_data[(listing_data[col] < lower) | (listing_data[col] > upper)]
    outlier_report[col] = len(outliers)

print(outlier_report)

listing_data.to_csv("filtered_datasets/listing_residential_filtered.csv", index=False)
