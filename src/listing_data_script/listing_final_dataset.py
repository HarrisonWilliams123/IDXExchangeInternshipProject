import pandas as pd
import numpy as np

#Reads the .csv file to start making changes
list = pd.read_csv("filtered_datasets/feature_engineering_list_data.csv")

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
list['ClosePrice_outliers_flag'] = list[(list['ClosePrice'] >= lower) and (list['ClosePrice'] <= upper)]

#Outlier Detection for LivingArea
q1 = list['LivingArea'].quantile(0.25)
q3 = list['LivingArea'].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
list['LivingArea_outliers_flag'] = list[(list['LivingArea'] >= lower) and (list['LivingArea'] <= upper)]

#Outlier Detection for DaysOnMarket
q1 = list['DaysOnMarket'].quantile(0.25)
q3 = list['DaysOnMarket'].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
list['DaysOnMarket_outliers_flag'] = list[(list['DaysOnMarket'] >= lower) and (list['DaysOnMarket'] <= upper)]

#Saves the flagged .csv file
list.to_csv("filtered_datasets/final_flagged_listing_dataset.csv", index=False)

#Removes the rows with outliers
list = list[(list['ClosePrice_outliers_flag'] == False) and (list['LivingArea_outliers_flag'] == False) and (list['DaysOnMarket_outliers_flag'] == False)]

#Prints out the comparison
print("After Filtering: ")
print("Size of Dataset:", len(list))
print("ClosePrice median:", list['ClosePrice'].median())
print("LivingArea median:", list['LivingArea'].median())
print("DaysOnMarket median:", list['DaysOnMarket'].median())

#Saves the cleaned filtered dataset
list.to_csv("filtered_datasets/final_listing_dataset.csv", index=False)
