import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

#Reads the school district GeoJSON file
districts = gpd.read_file("data/DistrictAreas2526_-284845464123469011.geojson")

#Filters the unified school districts only
unified = districts[districts["DistrictType"] == "Unified"].copy()

#Ensures the district polygons have a proper CRS
unified = unified.to_crs(epsg=4326)

#Convert property Latitude/Longitude into geographic points
list = pd.read_csv("filtered_datasets/feature_engineering_list_data.csv")
sold = pd.read_csv("filtered_datasets/feature_engineering_sold_data.csv")

#Create Geometry Columns
geometry_list = [Point(xy) for xy in zip(list["Longitude"], list["Latitude"])]
geometry_sold = [Point(xy) for xy in zip(sold["Longitude"], sold["Latitude"])]

properties_list = gpd.GeoDataFrame(list, geometry=geometry_list, crs="EPSG:4326")
properties_sold = gpd.GeoDataFrame(sold, geometry=geometry_sold, crs="EPSG:4326")

#Spatial Joins: assigned each property to a unified school district
list_joined = gpd.sjoin(
    properties_list,
    unified[["DistrictName", "geometry"]],
    how="left",
    predicate="within"
)

sold_joined = gpd.sjoin(
    properties_sold,
    unified[["DistrictName", "geometry"]],
    how="left",
    predicate="within"
)

#Adds the DistrictName to dataset
list['UnifiedSchoolDistrict'] = list_joined["DistrictName"]
sold['UnifiedSchoolDistrict'] = sold_joined["DistrictName"]

#Saves the datasets
list.to_csv("filtered_datasets/geo_list_dataset.csv", index=False)
sold.to_csv("filtered_datasets/geo_sold_dataset.csv", index=False)