import pandas as pd
import numpy as np

#Reads the .csv file to start making changes
sold = pd.read_csv("filtered_datasets/geo_sold_dataset.csv")

#Prints out the comparison
print("Before Filtering: ")
print("Size of Dataset:", len(sold))
print("ClosePrice median:", sold['ClosePrice'].median())
print("LivingArea median:", sold['LivingArea'].median())
print("DaysOnMarket median:", sold['DaysOnMarket'].median())


#Outlier Detection for ClosePrice
q1 = sold['ClosePrice'].quantile(0.25)
q3 = sold['ClosePrice'].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
sold['ClosePrice_outliers_flag'] = (sold['ClosePrice'] < lower) | (sold['ClosePrice'] > upper)

#Outlier Detection for LivingArea
q1 = sold['LivingArea'].quantile(0.25)
q3 = sold['LivingArea'].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
sold['LivingArea_outliers_flag'] = (sold['LivingArea'] < lower) | (sold['LivingArea'] > upper)

#Outlier Detection for DaysOnMarket
q1 = sold['DaysOnMarket'].quantile(0.25)
q3 = sold['DaysOnMarket'].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
sold['DaysOnMarket_outliers_flag'] = (sold['DaysOnMarket'] < lower) | (sold['DaysOnMarket'] > upper)

#Saves the flagged .csv file
sold.to_csv("filtered_datasets/final_flagged_sold_dataset.csv", index=False)

#Removes the rows with outliers
sold = sold[
    (~sold['ClosePrice_outliers_flag']) &
    (~sold['LivingArea_outliers_flag']) &
    (~sold['DaysOnMarket_outliers_flag'])
]

#Prints out the comparison
print("\nAfter Filtering: ")
print("Size of Dataset:", len(sold))
print("ClosePrice median:", sold['ClosePrice'].median())
print("LivingArea median:", sold['LivingArea'].median())
print("DaysOnMarket median:", sold['DaysOnMarket'].median())

#Saves the cleaned filtered dataset
sold.to_csv("filtered_datasets/final_sold_dataset.csv", index=False)
