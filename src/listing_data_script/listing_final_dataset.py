import pandas as pd
import numpy as np

#Reads the .csv file to start making changes
list = pd.read_csv("filtered_datasets/geo_list_dataset.csv")

#Prints out the comparison
print("Before Filtering: ")
print("Size of Dataset:", len(list))
print("ClosePrice median:", list['ClosePrice'].median())
print("LivingArea median:", list['LivingArea'].median())
print("DaysOnMarket median:", list['DaysOnMarket'].median())


#Outlier Detection for ClosePrice
q1 = list['ClosePrice'].quantile(0.25)
q3 = list['ClosePrice'].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
list['ClosePrice_outliers_flag'] = (list['ClosePrice'] < lower) | (list['ClosePrice'] > upper)

#Outlier Detection for LivingArea
q1 = list['LivingArea'].quantile(0.25)
q3 = list['LivingArea'].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
list['LivingArea_outliers_flag'] = (list['LivingArea'] < lower) | (list['LivingArea'] > upper)

#Outlier Detection for DaysOnMarket
q1 = list['DaysOnMarket'].quantile(0.25)
q3 = list['DaysOnMarket'].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
list['DaysOnMarket_outliers_flag'] = (list['DaysOnMarket'] < lower) | (list['DaysOnMarket'] > upper)

#Saves the flagged .csv file
list.to_csv("filtered_datasets/final_flagged_listing_dataset.csv", index=False)

#Removes the rows with outliers
list = list[
    (~list['ClosePrice_outliers_flag']) &
    (~list['LivingArea_outliers_flag']) &
    (~list['DaysOnMarket_outliers_flag'])
]

#Prints out the comparison
print("\nAfter Filtering: ")
print("Size of Dataset:", len(list))
print("ClosePrice median:", list['ClosePrice'].median())
print("LivingArea median:", list['LivingArea'].median())
print("DaysOnMarket median:", list['DaysOnMarket'].median())

#Saves the cleaned filtered dataset
list.to_csv("filtered_datasets/final_listing_dataset.csv", index=False)
