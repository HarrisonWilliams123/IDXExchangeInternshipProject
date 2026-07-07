import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

#Opens the combined dataset from the first deliverable
sold_data = pd.read_csv("data/unfiltered_sold_df.csv")

#Prints out the different types of PropertyType
print(sold_data['PropertyType'].unique())

#Gets the specific amount of times a PropertyType comes up (e.g. Residential, Land, ComercialLease, etc.)
number_of_residential_properties = len(sold_data[sold_data['PropertyType'] == 'Residential'])
number_of_commercialsale_properties = len(sold_data[sold_data['PropertyType'] == 'CommercialSale'])
number_of_manufacturedinpark_properties = len(sold_data[sold_data['PropertyType'] == 'ManufacturedInPark'])
number_of_residentiallease_properties = len(sold_data[sold_data['PropertyType'] == 'ResidentialLease'])
number_of_land_properties = len(sold_data[sold_data['PropertyType'] == 'Land'])
number_of_residentialincome_properties = len(sold_data[sold_data['PropertyType'] == 'ResidentialIncome'])
number_of_commerciallease_properties = len(sold_data[sold_data['PropertyType'] == 'CommercialLease'])
number_of_businessopportunity_properties = len(sold_data[sold_data['PropertyType'] == 'BusinessOpportunity'])
sum_of_other_property_types = number_of_businessopportunity_properties + number_of_commercialsale_properties + number_of_land_properties + number_of_commerciallease_properties + number_of_manufacturedinpark_properties + number_of_residentialincome_properties + number_of_residentiallease_properties


#First Bar Plot
plt.figure(figsize=(10, 5))

categories = [
    'Residential', 'CommercialSale', 'ManufacturedInPark', 'ResidentialLease',
    'Land', 'ResidentialIncome', 'CommercialLease', 'BusinessOpportunity'
]

values = [
    number_of_residential_properties,
    number_of_commercialsale_properties,
    number_of_manufacturedinpark_properties,
    number_of_residentiallease_properties,
    number_of_land_properties,
    number_of_residentialincome_properties,
    number_of_commerciallease_properties,
    number_of_businessopportunity_properties
]

colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'skyblue', 'brown']

bars = plt.bar(categories, values, color=colors, edgecolor='black', linewidth=0.7)
plt.title('Property Types Comparison', fontsize=14, fontweight='bold')
plt.xlabel('Property Type')
plt.ylabel('Quantity')
plt.xticks(rotation=45)
plt.bar_label(bars, padding=3, fontweight='bold')

plt.tight_layout()
plt.savefig("reports/sold_property_types_comparison.png", dpi=300)


#Second Bar Chart
plt.figure(figsize=(10, 5))

categories_2 = ['Residential', 'Other Property Type']
values_2 = [number_of_residential_properties, sum_of_other_property_types]
colors_2 = ['red', 'blue']

bars2 = plt.bar(categories_2, values_2, color=colors_2, edgecolor='black', linewidth=0.7)
plt.title("Residential vs. Other Property Types", fontsize=14, fontweight='bold')
plt.xlabel('Property Type')
plt.ylabel('Quantity')
plt.bar_label(bars2, padding=3, fontweight='bold')

plt.tight_layout()
plt.savefig("reports/sold_residential_vs_other.png", dpi=300)