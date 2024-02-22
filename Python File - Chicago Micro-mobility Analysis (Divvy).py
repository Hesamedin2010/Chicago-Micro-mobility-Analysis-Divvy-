# # Chicago Micro-mobility Analysis (Divvy)

# # 1 - Data setup and preliminary analysis

# You can fetch the data from the API by using the City of Chicago Data Portal URL (https://dev.socrata.com/foundry/data.cityofchicago.org/fg6s-gzvg). You need to sign up in order to create an APP token and then use your token for authentication to access the data of Divvy trips. Below are the codes you can use for this purpose:
# First you need to install sodapy 
#pip install sodapy

# Then you can achieve data

#import pandas as pd
#from sodapy import Socrata

# paste your copied app token in place of #APP_TOKEN
#client = Socrata("data.austintexas.gov", "#APP_TOKEN")

# First 2000 results, returned as JSON from API / converted to Python list of dictionaries by sodapy.
# "fg6s-gzvg" is taken from the last part of the URL of API Endpoint
#results = client.get("fg6s-gzvg", limit=2000)

# Convert results to pandas DataFrame
#df = pd.DataFrame.from_records(results)

# For this exercise, I have downloaded the csv dataset directly from City of Chicago Data Portal (https://data.cityofchicago.org/Transportation/Divvy-Trips/fg6s-gzvg/about_data) and read the file from that csv file

# The path of input files

# The file of Divvy trips
input_micro_mobility = "Divvy_Trips_20240103.csv"

# The file of city wards that we are going to use further in geopandas
input_boundaries = "Boundaries_-_Wards__2023-__20240103.csv"

# Reading Files as dataframes
import pandas as pd
df_micro_mobility = pd.read_csv(input_micro_mobility, on_bad_lines = 'warn', sep=',')
df_boundaries = pd.read_csv(input_boundaries, on_bad_lines = 'warn', sep=',')

# Showing a few rows of the tables

# Micro Mobolity
df_micro_mobility.head()

# Boundaries
df_boundaries.head()

# 1 - Data setup and preliminary analysis

# In this section, I am trying to do some pre-processing and clean the data and also do some exploratory analysis to know better the dataset and basic information hidden behind the micro-mobility data. I am going to answer simple questions such as:
# - The number of records before and after data cleaning.
# - When did collection of data start(start-date and time) for micro-mobility dataset and what is the most recent date and time available.
# - Number of records per year and month in micro-mobility dataset.
# - identify patterns e.g.,:
# - Are there more vehicles as years go  on ?
# - Is there some change in usage patterns among different days of the week , months is there a trend – seasonal or weekly ?
# - Are there any trends based on the gender and age of the user ?

# Using count() method to see the missing values in schema of the dataframe.
df_micro_mobility.count()

# ...........................................................................................

# - The number of records before and after data cleaning. 
# As observed, prior to data cleaning, there are 21,242,740 rows (TRIP ID). However, it is evident that certain columns contain missing values (LATITUDE, LONGITUDE, GENDER, BIRTH YEAR), requiring attention. The most important column for us to calculate OD matrix in further sections are LATITUDE and LONGITUDE, so in this level I am cleaning data based on these columns, however I will clean data based on GENDER and BIRTH YEAR separately. Various approaches exist for handling missing data, and for this exercise, I have decided to address it by removing the rows with missing values.

# Removing null values
df_MM_clean = df_micro_mobility.dropna(subset=["FROM LATITUDE", "TO LATITUDE"])
df_MM_clean.count()

# Following the data cleaning process, the dataset now consists of 21,241,850 rows for each column, and all necessary columns are non-null except for "GENDER" and "BIRTH YEAR". 

# ...........................................................................................

# - When did collection of data start(start-date and time) for micro-mobility dataset and what is the most recent date and time available.

# Turning "Start Time" column to datetime object
df_MM_clean_time = pd.to_datetime(df_MM_clean['START TIME'], format="%m/%d/%Y %I:%M:%S %p")

# Find the minimum value in the "Start Time" column
print("Minimum Start Time:", df_MM_clean_time.min())

# Collection of data start(start-date and time) for micro-mobility dataset starts from 01:06:00 of 27th of June 2013.
print("Most Recent Start Time:", df_MM_clean_time.max())

# The most recent date and time available in dataset is 23:57:17 of 31st December 2019.

# ...........................................................................................

# - Number of records per year and month in micro-mobility dataset.

# Create new columns that we need for further analysis (Year, Season, Month, Week, etc.)
import datetime as dt
df_MM_clean["YEAR"] = df_MM_clean_time.dt.strftime("%Y")

df_MM_clean["MONTH"] = df_MM_clean_time.dt.strftime("%m")

# Function for seasons
def get_season(month):
    if 3 <= month <= 5:
        return 'Spring'
    elif 6 <= month <= 8:
        return 'Summer'
    elif 9 <= month <= 11:
        return 'Autumn'
    else:
        return 'Winter'

df_MM_clean["SEASON"] = df_MM_clean_time.dt.month.apply(get_season)

df_MM_clean["DAY OF WEEK"] = df_MM_clean_time.dt.strftime("%A")

# See the final result
df_MM_clean.head()

# Number of trips per year
year_groups = df_MM_clean.groupby(["YEAR"]).size()
print(year_groups)
bp_year_groups = year_groups.plot(kind="bar")

# It is shown that there is an increasing trend for years and this growth was dramatic from 2013 to 2014 and one of the reasons is that our data start from the June 2013. Also, there was a litle decrease from 2017 to 2018.

# Number of trips per month
month_groups = df_MM_clean.groupby(["MONTH"]).size()
print(month_groups)
bp_month_groups = month_groups.plot(kind="bar")

# It shows that the majority of trips occur from June to October and it is less in cold months.

# Number of trips per year and month
month_year_groups = df_MM_clean.groupby(["YEAR", "MONTH"]).size()
print(month_year_groups)

# Bar plot to show the year-month pattern of data
bp_month_year_groups = month_year_groups.plot(kind="bar", figsize=(30, 20))

# Number of records per year and month in micro-mobility dataset is shown above. It can be seen that majority of data belong to the middle of each year (from June to October) and generaly every year the trend was increasing.

# ...........................................................................................

# - identify patterns e.g.,:
# - Are there more vehicles as years go  on ?
# - Is there some change in usage patterns among different days of the week , months is there a trend – seasonal or weekly ?
# - Are there any trends based on the gender and age of the user ?
df_MM_clean.info()

# Comparing used bicycles in different years
vehicle_groups = df_MM_clean.groupby(["YEAR", "BIKE ID"]).size()
print(vehicle_groups)

# Analyzing seasonal trends
season_groups = df_MM_clean.groupby(["SEASON"]).size()
print(season_groups)
bp_season_groups = season_groups.plot(kind="bar")

# It shows that most of the trips happened on Summer and after that on Autumn

vehicle_season_groups = df_MM_clean.groupby(["SEASON", "BIKE ID"]).size()
print(vehicle_season_groups)

vehicle_month_groups = df_MM_clean.groupby(["YEAR", "MONTH", "BIKE ID"]).size()
print(vehicle_month_groups)

# Analyzing weekly trends
week_groups = df_MM_clean.groupby(["DAY OF WEEK"]).size()
print(week_groups)
bp_week_groups = week_groups.plot(kind="bar")

# It shows that most of the trips happened on weekdays but the difference is not very significant

vehicle_week_groups = df_MM_clean.groupby(["DAY OF WEEK", "BIKE ID"]).size()
print(vehicle_week_groups)

# ...........................................................................................

# Now I am going to clean the data again based on GENDER and BIRTH YEAR
df_MM_clean_GB = df_MM_clean.dropna(axis=0)
df_MM_clean_GB.count()

# Now there are 16,346,709 rows for all the columns.

df_MM_clean_GB['GENDER'].value_counts()
gender_year_groups = df_MM_clean_GB.groupby(["YEAR", "GENDER"]).size()
print(gender_year_groups)
bp_gender_year_groups = gender_year_groups.plot(kind="bar")

# It is shown that in general through these years the number of trips increased but the share of males have been always way more than females

# Evaluating the gender trends within months
gender_month_groups = df_MM_clean_GB.groupby(["MONTH", "GENDER"]).size()
print(gender_month_groups)
bp_gender_month_groups = gender_month_groups.plot(kind="bar")

# The same pattern is here for both males and females, warmer months are more delightful to use these modes of transport.

# ...........................................................................................

# Calculating the minimum and maximum of "BIRTH YEAR" in order to find out the data
df_MM_clean_GB['BIRTH YEAR'].min()
df_MM_clean_GB['BIRTH YEAR'].max()

# Check the "birth year" column to find out "bad data"
df_MM_clean_GB['BIRTH YEAR'].value_counts()

# It is shown that there are some data which are obviously incorrect such as 1790. So, I am getting rid of these data. 

# Drop incorrect rows
df_MM_clean_B = df_MM_clean_GB[df_MM_clean_GB['BIRTH YEAR'] >= 1925]
df_MM_clean_B.count()
df_MM_clean_B['BIRTH YEAR'].min()

# Now we can say that the minimum of BIRTH YEAR is 1925 and the maximum of it is 2017.

df_MM_clean_B = df_MM_clean_B.dropna(subset=['BIRTH YEAR'])

# Convert BIRTH YEAR and YEAR to integer
df_MM_clean_B['BIRTH YEAR'] = df_MM_clean_B['BIRTH YEAR'].astype('int')
df_MM_clean_B['YEAR'] = df_MM_clean_B['YEAR'].astype('int')

# Create age groups based on the age distribution of users
df_MM_clean_B['age'] = df_MM_clean_B['YEAR'] - df_MM_clean_B['BIRTH YEAR']

# Define age groups
age_bins = [0, 18, 30, 40, 50, 60, float('inf')]  # Define age bins/ranges
age_labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61+']  # Define corresponding labels

# Create 'age group' column using pd.cut
df_MM_clean_B['age group'] = pd.cut(df_MM_clean_B['age'], bins=age_bins, labels=age_labels, right=False)
age_groups = df_MM_clean_B.groupby("age group").size()
print(age_groups)
bp_age_groups = age_groups.plot(kind="bar")

# It can be seen that the majority of users belong to the age group between 19-40 years old.

# Evaluating the age trend within years
age_year_groups = df_MM_clean_B.groupby(["YEAR", "age group"]).size()
print(age_year_groups)
bp_age_year_groups = age_year_groups.plot(kind="bar", figsize=(30, 20))

# It is observed that the same pattern exists for each year.

# -------------------------------------------------------------------------------------------

# # 2 - OD Matrices

# In this section, I am going to do these tasks:
# - Associate each trip in the dataset to an origin and destination ward by combining the trip information with the information about the wards. Check which wards the FROM_LOCATION and TO_LOCATION fields belong to.
# - Compute then the O-D matrix, i.e., the number of bookings starting in ward i and ending in ward j.
# - Prepare OD matrices for different years and different age groups(3 OD matrices for each age-group of 3 consecutive years). Are there any periodicity or trends noticed? Is there a difference between the OD matrices for different age groups?
# - Based on observation, visualise selected OD matrices that show some trends/periodicity on a map. 
# - Create a flowmap for the OD matrices.

# First I installed geopandas in order to do spatial analysis and determine each trip point (from/to) is within which ward of Chicago based on latitude and longitude
pip install geopandas
pip install rtree
pip install pygeos

# In this part, because the size of the file is too much large and I encountered memory issues for spatial joining, I decided to select only 3 years to work on.
df_MM_clean_2016 = df_MM_clean[df_MM_clean['YEAR'] == '2016']

import geopandas as gpd
from shapely import wkt

# Convert 'the_geom' in wards_chicago from WKT(Well Known text) to shapely objects
# 'the_geom' column contains MULTIPOLYGON data in text format
df_boundaries['the_geom'] = df_boundaries['the_geom'].apply(wkt.loads)
wards_gdf = gpd.GeoDataFrame(df_boundaries, geometry='the_geom')

# Convert 'FROM LOCATION' and 'TO LOCATION' in df_chicago from WKT to shapely Point objects
# These columns contain POINT data in text format
df_MM_clean_2016['from_point'] = df_MM_clean_2016['FROM LOCATION'].apply(wkt.loads)
df_from_gdf_2016 = gpd.GeoDataFrame(df_MM_clean_2016, geometry='from_point')

df_MM_clean_2016['to_point'] = df_MM_clean_2016['TO LOCATION'].apply(wkt.loads)
df_to_gdf_2016 = gpd.GeoDataFrame(df_MM_clean_2016, geometry='to_point')

# Ensure the CRS for both GeoDataFrames are the same
# This can be done by setting the CRS(Co-ordinate Reference System) of df_from_gdf and df_to_gdf to match that of wards_gdf
df_from_gdf_2016 = df_from_gdf_2016.set_crs('EPSG:4326', inplace=True,allow_override = True)
df_to_gdf_2016 = df_to_gdf_2016.set_crs('EPSG:4326', inplace=True,allow_override = True)
wards_gdf = wards_gdf.set_crs('EPSG:4326', inplace=True,allow_override = True)

# Perform spatial joins
# Join df_from_gdf and df_to_gdf with wards_gdf to find the corresponding wards
from_joined_2016 = gpd.sjoin(df_from_gdf_2016, wards_gdf, how="left", op='within')
to_joined_2016 = gpd.sjoin(df_to_gdf_2016, wards_gdf, how="left", op='within')

# Add the ward information back to the original df_chicago DataFrame
df_MM_clean_2016['FROM WARD'] = from_joined_2016['Ward']  # Replace 'Ward' with the actual column name in wards_gdf
df_MM_clean_2016['TO WARD'] = to_joined_2016['Ward']      # Replace 'Ward' with the actual column name in wards_gdf
df_MM_clean_2016.to_csv("df_MM_clean_2016", index=False)

# Display the first few rows of the updated df_chicago to check the results
df_MM_clean_2016.head()


df_MM_clean_2017 = df_MM_clean[df_MM_clean['YEAR'] == '2017']

# Convert 'FROM LOCATION' and 'TO LOCATION' in df_chicago from WKT to shapely Point objects
# These columns contain POINT data in text format
df_MM_clean_2017['from_point'] = df_MM_clean_2017['FROM LOCATION'].apply(wkt.loads)
df_from_gdf_2017 = gpd.GeoDataFrame(df_MM_clean_2017, geometry='from_point')
df_MM_clean_2017['to_point'] = df_MM_clean_2017['TO LOCATION'].apply(wkt.loads)
df_to_gdf_2017 = gpd.GeoDataFrame(df_MM_clean_2017, geometry='to_point')

# Ensure the CRS for both GeoDataFrames are the same
# This can be done by setting the CRS(Co-ordinate Reference System) of df_from_gdf and df_to_gdf to match that of wards_gdf
df_from_gdf_2017 = df_from_gdf_2017.set_crs('EPSG:4326', inplace=True,allow_override = True)
df_to_gdf_2017 = df_to_gdf_2017.set_crs('EPSG:4326', inplace=True,allow_override = True)
wards_gdf = wards_gdf.set_crs('EPSG:4326', inplace=True,allow_override = True)

# Perform spatial joins
# Join df_from_gdf and df_to_gdf with wards_gdf to find the corresponding wards
from_joined_2017 = gpd.sjoin(df_from_gdf_2017, wards_gdf, how="left", op='within')
to_joined_2017 = gpd.sjoin(df_to_gdf_2017, wards_gdf, how="left", op='within')

# Add the ward information back to the original df_chicago DataFrame
df_MM_clean_2017['FROM WARD'] = from_joined_2017['Ward']  # Replace 'Ward' with the actual column name in wards_gdf
df_MM_clean_2017['TO WARD'] = to_joined_2017['Ward']      # Replace 'Ward' with the actual column name in wards_gdf
df_MM_clean_2017.to_csv("df_MM_clean_2017", index=False)

# Display the first few rows of the updated df_chicago to check the results
df_MM_clean_2017.head()

df_MM_clean_2018 = df_MM_clean[df_MM_clean['YEAR'] == '2018']

# Convert 'FROM LOCATION' and 'TO LOCATION' in df_chicago from WKT to shapely Point objects
# These columns contain POINT data in text format
df_MM_clean_2018['from_point'] = df_MM_clean_2018['FROM LOCATION'].apply(wkt.loads)
df_from_gdf_2018 = gpd.GeoDataFrame(df_MM_clean_2018, geometry='from_point')
df_MM_clean_2018['to_point'] = df_MM_clean_2018['TO LOCATION'].apply(wkt.loads)
df_to_gdf_2018 = gpd.GeoDataFrame(df_MM_clean_2018, geometry='to_point')

# Ensure the CRS for both GeoDataFrames are the same
# This can be done by setting the CRS(Co-ordinate Reference System) of df_from_gdf and df_to_gdf to match that of wards_gdf
df_from_gdf_2018 = df_from_gdf_2018.set_crs('EPSG:4326', inplace=True,allow_override = True)
df_to_gdf_2018 = df_to_gdf_2018.set_crs('EPSG:4326', inplace=True,allow_override = True)
wards_gdf = wards_gdf.set_crs('EPSG:4326', inplace=True,allow_override = True)

# Perform spatial joins
# Join df_from_gdf and df_to_gdf with wards_gdf to find the corresponding wards
from_joined_2018 = gpd.sjoin(df_from_gdf_2018, wards_gdf, how="left", op='within')
to_joined_2018 = gpd.sjoin(df_to_gdf_2018, wards_gdf, how="left", op='within')

# Add the ward information back to the original df_chicago DataFrame
df_MM_clean_2018['FROM WARD'] = from_joined_2018['Ward']  # Replace 'Ward' with the actual column name in wards_gdf
df_MM_clean_2018['TO WARD'] = to_joined_2018['Ward']      # Replace 'Ward' with the actual column name in wards_gdf
df_MM_clean_2018.to_csv("df_MM_clean_2018", index=False)

# Display the first few rows of the updated df_chicago to check the results
df_MM_clean_2018.head()

# ...........................................................................................

# - Compute then the O-D matrix, i.e., the number of bookings starting in ward i and ending in ward j.

# OD Matrix 2016 calculation using pivot table
matrix_2016 = (
    df_MM_clean_2016.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_2016


# OD Matrix 2017 calculation using pivot table
matrix_2017 = (
    df_MM_clean_2017.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_2017


# OD Matrix 2018 calculation using pivot table
matrix_2018 = (
    df_MM_clean_2018.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_2018


# Saving OD Matrices
matrix_2016.to_csv("matrix_2016", index=False)
matrix_2017.to_csv("matrix_2017", index=False)
matrix_2018.to_csv("matrix_2018", index=False)

# ...........................................................................................

# - Prepare OD matrices for different years and different age groups(3 OD matrices for each age-group of 3 consecutive years). Are there any periodicity or trends noticed? Is there a difference between the OD matrices for different age groups?

import pandas as pd

# Using saved dataframes with "from wards" and "to wards" to avoid kernel disconnecting.
df_MM_clean_2016 = pd.read_csv("df_MM_clean_2016", on_bad_lines = 'warn', sep=',')
df_MM_clean_2017 = pd.read_csv("df_MM_clean_2017", on_bad_lines = 'warn', sep=',')
df_MM_clean_2018 = pd.read_csv("df_MM_clean_2018", on_bad_lines = 'warn', sep=',')

# Drop null values
df_MM_clean_2016 = df_MM_clean_2016.dropna(subset=['BIRTH YEAR'])

# Convert BIRTH YEAR to integer
df_MM_clean_2016['BIRTH YEAR'] = df_MM_clean_2016['BIRTH YEAR'].astype('int')

# Create age groups based on the agr distribution of users
df_MM_clean_2016['age'] = df_MM_clean_2016['YEAR'] - df_MM_clean_2016['BIRTH YEAR']

# Define age groups
age_bins = [0, 18, 30, 40, 50, 60, float('inf')]  # Define age bins/ranges
age_labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61+']  # Define corresponding labels

# Create 'age group' column using pd.cut
df_MM_clean_2016['age group'] = pd.cut(df_MM_clean_2016['age'], bins=age_bins, labels=age_labels, right=False)


age_group_under_18_2016 = df_MM_clean_2016[df_MM_clean_2016['age group'] == '0-18']
# OD Matrix
matrix_age_under_18_2016 = (
    age_group_under_18_2016.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_under_18_2016


# It shows the OD matrix of under-18 age group users in 2016


age_group_19_30_2016 = df_MM_clean_2016[df_MM_clean_2016['age group'] == '19-30']
# OD Matrix
matrix_age_19_30_2016 = (
    age_group_19_30_2016.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_19_30_2016


age_group_31_40_2016 = df_MM_clean_2016[df_MM_clean_2016['age group'] == '31-40']
# OD Matrix
matrix_age_31_40_2016 = (
    age_group_31_40_2016.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_31_40_2016


age_group_41_50_2016 = df_MM_clean_2016[df_MM_clean_2016['age group'] == '41-50']
# OD Matrix
matrix_age_41_50_2016 = (
    age_group_41_50_2016.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_41_50_2016


age_group_51_60_2016 = df_MM_clean_2016[df_MM_clean_2016['age group'] == '51-60']
# OD Matrix
matrix_age_51_60_2016 = (
    age_group_51_60_2016.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_51_60_2016


age_group_above_61_2016 = df_MM_clean_2016[df_MM_clean_2016['age group'] == '61+']
# OD Matrix
matrix_age_above_61_2016 = (
    age_group_above_61_2016.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_above_61_2016


# ...........................................................................................

# Drop null values
df_MM_clean_2017 = df_MM_clean_2017.dropna(subset=['BIRTH YEAR'])

# Convert BIRTH YEAR to integer
df_MM_clean_2017['BIRTH YEAR'] = df_MM_clean_2017['BIRTH YEAR'].astype('int')

# Create age groups based on the agr distribution of users
df_MM_clean_2017['age'] = df_MM_clean_2017['YEAR'] - df_MM_clean_2017['BIRTH YEAR']

# Define age groups
age_bins = [0, 18, 30, 40, 50, 60, float('inf')]  # Define age bins/ranges
age_labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61+']  # Define corresponding labels

# Create 'age group' column using pd.cut
df_MM_clean_2017['age group'] = pd.cut(df_MM_clean_2017['age'], bins=age_bins, labels=age_labels, right=False)

age_group_under_18_2017 = df_MM_clean_2017[df_MM_clean_2017['age group'] == '0-18']
# OD Matrix
matrix_age_under_18_2017 = (
    age_group_under_18_2017.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_under_18_2017

# As it is shown, the number of under 18 years old users are low and the most trips happened inside ward 28.


age_group_19_30_2017 = df_MM_clean_2017[df_MM_clean_2017['age group'] == '19-30']
# OD Matrix 2018 calculation using pivot table
matrix_age_19_30_2017 = (
    age_group_19_30_2017.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_19_30_2017

# Because the siz of the matrix is too large, it is hard to conclude here, so we will wait untile the next part for further analysis.


age_group_31_40_2017 = df_MM_clean_2017[df_MM_clean_2017['age group'] == '31-40']
# OD Matrix 2018 calculation using pivot table
matrix_age_31_40_2017 = (
    age_group_31_40_2017.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_31_40_2017


age_group_41_50_2017 = df_MM_clean_2017[df_MM_clean_2017['age group'] == '41-50']
# OD Matrix 2018 calculation using pivot table
matrix_age_41_50_2017 = (
    age_group_41_50_2017.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_41_50_2017


age_group_51_60_2017 = df_MM_clean_2017[df_MM_clean_2017['age group'] == '51-60']
# OD Matrix 2018 calculation using pivot table
matrix_age_51_60_2017 = (
    age_group_51_60_2017.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_51_60_2017


age_group_above_61_2017 = df_MM_clean_2017[df_MM_clean_2017['age group'] == '61+']
# OD Matrix 2018 calculation using pivot table
matrix_age_above_61_2017 = (
    age_group_above_61_2017.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_above_61_2017

# ...........................................................................................

# Drop null values
df_MM_clean_2018 = df_MM_clean_2018.dropna(subset=['BIRTH YEAR'])

# Convert BIRTH YEAR to integer
df_MM_clean_2018['BIRTH YEAR'] = df_MM_clean_2018['BIRTH YEAR'].astype('int')

# Create age groups based on the agr distribution of users
df_MM_clean_2018['age'] = df_MM_clean_2017['YEAR'] - df_MM_clean_2017['BIRTH YEAR']

# Define age groups
age_bins = [0, 18, 30, 40, 50, 60, float('inf')]  # Define age bins/ranges
age_labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61+']  # Define corresponding labels

# Create 'age group' column using pd.cut
df_MM_clean_2018['age group'] = pd.cut(df_MM_clean_2018['age'], bins=age_bins, labels=age_labels, right=False)


age_group_under_18_2018 = df_MM_clean_2018[df_MM_clean_2018['age group'] == '0-18']
# OD Matrix 2018 calculation using pivot table
matrix_age_under_18_2018 = (
    age_group_under_18_2018.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_under_18_2018


age_group_19_30_2018 = df_MM_clean_2018[df_MM_clean_2018['age group'] == '19-30']
# OD Matrix 2018 calculation using pivot table
matrix_age_19_30_2018 = (
    age_group_19_30_2018.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_19_30_2018


age_group_31_40_2018 = df_MM_clean_2018[df_MM_clean_2018['age group'] == '31-40']
# OD Matrix 2018 calculation using pivot table
matrix_age_31_40_2018 = (
    age_group_31_40_2018.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_31_40_2018


age_group_41_50_2018 = df_MM_clean_2018[df_MM_clean_2018['age group'] == '41-50']
# OD Matrix 2018 calculation using pivot table
matrix_age_41_50_2018 = (
    age_group_41_50_2018.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_41_50_2018


age_group_51_60_2018 = df_MM_clean_2018[df_MM_clean_2018['age group'] == '51-60']
# OD Matrix 2018 calculation using pivot table
matrix_age_51_60_2018 = (
    age_group_51_60_2018.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_51_60_2018


age_group_above_61_2018 = df_MM_clean_2018[df_MM_clean_2018['age group'] == '61+']
# OD Matrix 2018 calculation using pivot table
matrix_age_above_61_2018 = (
    age_group_above_61_2018.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_above_61_2018

# ...........................................................................................

# - Based on observation, visualise selected OD matrices that show some trends/periodicity on a map. 
import seaborn as sns

# Heatmap general 2016
sns.heatmap(matrix_2016,cmap='crest')

# It shows that in general in 2016, most of the trips happened in ward 42. After that there are wards 34 and 43 and also the trips among these three wards.


# Heatmap 0-18 in 2016
sns.heatmap(matrix_age_under_18_2016,cmap='crest')

# It shows that most of the teenagers' trips (under 18) in 2016 happened in ward 10 and 44. after that there are wards 27, 30, etc.


# Heatmap 19-30 in 2016
sns.heatmap(matrix_age_19_30_2016,cmap='crest')

# It shows that most of the young people's trips (19-30) in 2016 happened in wards 42 and 43.


# Heatmap 31-40 in 2016
sns.heatmap(matrix_age_31_40_2016,cmap='crest')

# It shows that most of 31-40 people's trips in 2016 happened in ward 42. After that there are wards 43, 34 and 27 and also the trips among these wards.


# Heatmap 41-50 in 2016
sns.heatmap(matrix_age_41_50_2016,cmap='crest')

# Almost the same pattern exists for 41-50 travelers.


# Heatmap 51-60 in 2016
sns.heatmap(matrix_age_51_60_2016,cmap='crest')

# Almost the same pattern exists for 51-60 travelers.


# Heatmap above 61 in 2016
sns.heatmap(matrix_age_above_61_2016,cmap='crest')

# Almost the same pattern exists for above 61 years old travelers.

# In conclusion, we can say that wards 42, 34, and 27 are the most important wards for most of the age groups but ward 5 is only attractive for young people and most of their trips happened there.

# ...........................................................................................

# Heatmap general 2017
sns.heatmap(matrix_2017,cmap='crest')

# In general, for whole 2017, the most trips happened inside ward 42 and after that from ward 42 to ward 34. insode ward 34 and from ward 34 to 42 are comming after them.


# Heatmap 0-18 in 2017
sns.heatmap(matrix_age_under_18_2017,cmap='crest')

# It shows that in 2017, teenagers' trips mostly happened inside the ward 5 and 42. also from ward 42 to 2.


# Heatmap 19-30 in 2017
sns.heatmap(matrix_age_19_30_2017,cmap='crest')

# It shows that most of the yung people's trips (19-30) in 2017 happened in ward 5 and after that there are ward 42, 43, and 34.


# Heatmap 31-40 in 2017
sns.heatmap(matrix_age_31_40_2017,cmap='crest')

# It shows that most of the 31-40 people trips in 2017 happened in ward 42. After that there are 43, 34 and also among these wards.


# Heatmap 41-50 in 2017
sns.heatmap(matrix_age_41_50_2017,cmap='crest')

# It shows that most of 42-50 people's trips in 2017 happened in wards 42 and 34 and among these two wards.


# Heatmap 51-60 in 2017
sns.heatmap(matrix_age_51_60_2017,cmap='crest')

# The same pattern exists for 51-60 people.


# Heatmap above 61 in 2017
sns.heatmap(matrix_age_above_61_2017,cmap='crest')

# The same pattern exists for old people (above 61).

# ...........................................................................................

# Heatmap general 2018
sns.heatmap(matrix_2018,cmap='crest')

# Heatmap 0-18 in 2018
sns.heatmap(matrix_age_under_18_2018,cmap='crest')

# It shows that in 2018, the most of the teenagers' trips happened inside ward 42 and 34 and also between these two wards.


# Heatmap 19-30 in 2018
sns.heatmap(matrix_age_19_30_2018,cmap='crest')

# It shows that the most of the young people's trips (19-30) in 2018 happened inside ward 5. The rest of places respectively belong to ward 42, 34, and 44.


# Heatmap 31-40 in 2018
sns.heatmap(matrix_age_31_40_2018,cmap='crest')

# It shows that most of 31-40 travelers' trips in 2018 happened in ward 42. The second place belongs to ward 44. Thus, we can see that ward 5 is not very attractive for this group however it was attractive for young people.


# Heatmap 41-50 in 2018
sns.heatmap(matrix_age_41_50_2018,cmap='crest')

# It shows that 41-50 people's trips in 2018 happened in ward 42 and after that inside the ward 34. Additionally, the trips among these two wards (both ways) are also high. 


# Heatmap 51-60 in 2018
sns.heatmap(matrix_age_51_60_2018,cmap='crest')

# It shows that the same pattern exists for people between 51-60.


# Heatmap above 61 in 2018
sns.heatmap(matrix_age_above_61_2018,cmap='crest')

# It shows that, traveler above 61 years old, mostly travel inside ward 42 and after that from ward 42 to ward 34.

# In conclusion, It can be said that ward 42 is one of the most important zones in micromobility and ward 34 comes after that. Also, most of the young people's mobility happened in ward 5  but this ward is not very bold for other age groups.

# ...........................................................................................

# - Create a flowmap for the OD matrices.
# 2016
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

matrix_2016.index = matrix_2016.index.astype(int)
matrix_2016.columns = matrix_2016.columns.astype(int)

# Create a directed graph from the OD matrix
G = nx.DiGraph()

# Add nodes
for node in matrix_2016.index:
    G.add_node(node)

# Add edges
for from_node in matrix_2016.index:
    for to_node in matrix_2016.columns:
        weight = matrix_2016.loc[from_node, to_node]
        if weight > 0:
            G.add_edge(from_node, to_node, weight=weight)

# Draw the graph with a circular layout
pos = nx.circular_layout(G)

# Set node colors based on degree (number of connections)
node_colors = [G.degree(node) for node in G.nodes]

# Set edge colors based on weights
edge_colors = [G[from_node][to_node]['weight'] for from_node, to_node in G.edges]

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors, cmap=plt.cm.Blues)

# Draw edges with weights
nx.draw_networkx_edges(G, pos, width=1, edge_color=edge_colors, edge_cmap=plt.cm.Greens, arrowsize=10)

# Add labels
nx.draw_networkx_labels(G, pos, font_size=8, font_color='black', font_weight='bold')

# Add colorbar for edge weights
edge_weights = nx.get_edge_attributes(G, 'weight')
cbar = plt.colorbar()
cbar.set_label('Flow Counts')

plt.title("Flowmap for OD Matrix 2017")
plt.show()


# 2017
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

matrix_2017.index = matrix_2017.index.astype(int)
matrix_2017.columns = matrix_2017.columns.astype(int)

# Create a directed graph from the OD matrix
G = nx.DiGraph()

# Add nodes
for node in matrix_2017.index:
    G.add_node(node)

# Add edges
for from_node in matrix_2017.index:
    for to_node in matrix_2017.columns:
        weight = matrix_2017.loc[from_node, to_node]
        if weight > 0:
            G.add_edge(from_node, to_node, weight=weight)

# Draw the graph with a circular layout
pos = nx.circular_layout(G)

# Set node colors based on degree (number of connections)
node_colors = [G.degree(node) for node in G.nodes]

# Set edge colors based on weights
edge_colors = [G[from_node][to_node]['weight'] for from_node, to_node in G.edges]

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors, cmap=plt.cm.Blues)

# Draw edges with weights
nx.draw_networkx_edges(G, pos, width=1, edge_color=edge_colors, edge_cmap=plt.cm.Greens, arrowsize=10)

# Add labels
nx.draw_networkx_labels(G, pos, font_size=8, font_color='black', font_weight='bold')

# Add colorbar for edge weights
edge_weights = nx.get_edge_attributes(G, 'weight')
cbar = plt.colorbar()
cbar.set_label('Flow Counts')

plt.title("Flowmap for OD Matrix 2017")
plt.show()


# 2018
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

matrix_2018.index = matrix_2018.index.astype(int)
matrix_2018.columns = matrix_2018.columns.astype(int)

# Create a directed graph from the OD matrix
G = nx.DiGraph()

# Add nodes
for node in matrix_2018.index:
    G.add_node(node)

# Add edges
for from_node in matrix_2018.index:
    for to_node in matrix_2018.columns:
        weight = matrix_2018.loc[from_node, to_node]
        if weight > 0:
            G.add_edge(from_node, to_node, weight=weight)

# Draw the graph with a circular layout
pos = nx.circular_layout(G)

# Set node colors based on degree (number of connections)
node_colors = [G.degree(node) for node in G.nodes]

# Set edge colors based on weights
edge_colors = [G[from_node][to_node]['weight'] for from_node, to_node in G.edges]

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors, cmap=plt.cm.Blues)

# Draw edges with weights
nx.draw_networkx_edges(G, pos, width=1, edge_color=edge_colors, edge_cmap=plt.cm.Greens, arrowsize=10)

# Add labels
nx.draw_networkx_labels(G, pos, font_size=8, font_color='black', font_weight='bold')

# Add colorbar for edge weights
edge_weights = nx.get_edge_attributes(G, 'weight')
cbar = plt.colorbar()
cbar.set_label('Flow Counts')

plt.title("Flowmap for OD Matrix 2017")
plt.show()


# # 3 - Relation to Public transport line

# In this sectoin, I am going to do again some pre-processing on micro-mobility data (Divvy) and extract the csv files with coordinations. Also, I have downloaded the kml files of public transport in Chicago (such as bus stops, bus routes, subway rails, etc.). Thus, I will import the output of this section and those kml files into QGIS software to create some maps for further analysis.

# Group data by wards in order to be used into QGIS for further analysis.
import pandas as pd

df_MM_clean_2016 = pd.read_csv('df_MM_clean_2016', on_bad_lines = 'warn', sep=',')
df_MM_clean_2017 = pd.read_csv('df_MM_clean_2017', on_bad_lines = 'warn', sep=',')
df_MM_clean_2018 = pd.read_csv('df_MM_clean_2018', on_bad_lines = 'warn', sep=',')


number_of_start_trips = df_MM_clean_2016.groupby("FROM WARD").size().reset_index(name='number_of_start_trips_2016')
number_of_start_trips.to_csv("number_of_start_trips_2016", index=False)

number_of_start_trips_2017 = df_MM_clean_2017.groupby("FROM WARD").size().reset_index(name='number_of_start_trips_2017')
number_of_start_trips_2017.to_csv("number_of_start_trips_2017", index=False)

number_of_start_trips_2018 = df_MM_clean_2018.groupby("FROM WARD").size().reset_index(name='number_of_start_trips_2018')
number_of_start_trips_2018.to_csv("number_of_start_trips_2018", index=False)


number_of_end_trips_2016 = df_MM_clean_2016.groupby("TO WARD").size().reset_index(name='number_of_end_trips_2016')
number_of_end_trips_2016.to_csv("number_of_end_trips_2016", index=False)

number_of_end_trips_2017 = df_MM_clean_2017.groupby("TO WARD").size().reset_index(name='number_of_end_trips_2017')
number_of_end_trips_2017.to_csv("number_of_end_trips_2017", index=False)

number_of_end_trips_2018 = df_MM_clean_2018.groupby("TO WARD").size().reset_index(name='number_of_end_trips_2018')
number_of_end_trips_2018.to_csv("number_of_end_trips_2018", index=False)


df_MM_clean_2019 = pd.read_csv('df_2019.csv', on_bad_lines = 'warn', sep=',')
number_of_start_trips_2019 = df_MM_clean_2019.groupby("FROM WARD").size().reset_index(name='number_of_start_trips_2019')
number_of_start_trips_2019.to_csv("number_of_start_trips_2019", index=False)
number_of_end_trips_2019 = df_MM_clean_2019.groupby("TO WARD").size().reset_index(name='number_of_start_trips_2019')
number_of_end_trips_2019.to_csv("number_of_end_trips_2019", index=False)

# -------------------------------------------------------------------------------------------

# Here, I am dividing a day into 3 day times (Day, Evening and Night) to do some analysis based on the time of trips in QGIS software.

# day time
df_MM_clean_2016_time = pd.to_datetime(df_MM_clean_2016['START TIME'], format="%m/%d/%Y %I:%M:%S %p")
df_MM_clean_2017_time = pd.to_datetime(df_MM_clean_2017['START TIME'], format="%m/%d/%Y %I:%M:%S %p")
df_MM_clean_2018_time = pd.to_datetime(df_MM_clean_2018['START TIME'], format="%m/%d/%Y %I:%M:%S %p")


import datetime as dt
df_MM_clean_2016["HOUR"] = df_MM_clean_2016_time.dt.strftime("%H")
df_MM_clean_2017["HOUR"] = df_MM_clean_2017_time.dt.strftime("%H")
df_MM_clean_2018["HOUR"] = df_MM_clean_2018_time.dt.strftime("%H")

# Function for day time
def day_time(hour):
    if  hour=='00' or hour=='01' or hour=='02' or hour=='03' or hour=='04' or hour=='05' or hour=='06' or hour=='07':
        return 'Night'
    elif hour=='08' or hour=='09' or hour=='10' or hour=='11' or hour=='12' or hour=='13' or hour=='14' or hour=='15':
        return 'Day'
    elif hour=='16' or hour=='17' or hour=='18' or hour=='19' or hour=='20' or hour=='21' or hour=='22' or hour=='23':
        return 'Evening'

df_MM_clean_2016["DAY_TIME"] = df_MM_clean_2016["HOUR"].apply(day_time)
df_MM_clean_2017["DAY_TIME"] = df_MM_clean_2017["HOUR"].apply(day_time)
df_MM_clean_2018["DAY_TIME"] = df_MM_clean_2018["HOUR"].apply(day_time)

df_MM_clean_2016.head()


group_day_time_2016 = df_MM_clean_2016.groupby(["FROM WARD", "DAY_TIME"]).size().reset_index(name='group_day_time_2016')
group_day_time_2017 = df_MM_clean_2017.groupby(["FROM WARD", "DAY_TIME"]).size().reset_index(name='group_day_time_2017')
group_day_time_2018 = df_MM_clean_2018.groupby(["FROM WARD", "DAY_TIME"]).size().reset_index(name='group_day_time_2018')

group_day_time_2016.to_csv("group_day_time_2016", index=False)
group_day_time_2017.to_csv("group_day_time_2017", index=False)
group_day_time_2018.to_csv("group_day_time_2018", index=False)

# -------------------------------------------------------------------------------------------

# # 4 – Utilization of bicycles and costs

# In this section, I am going to calculate the utilization percentage of bicycles and also assess the cost and benefit of the bike-sharing company. For this purpose, I have made a rough estimation of bicycle maintenance costs and the revenue from each bike based on the trip duration. This is just a simple simulation of this kind of analysis.

# Working on the last year of data 2019
import pandas as pd
df_MM_clean_2019 = pd.read_csv('dataframe_2019 (1).csv', on_bad_lines = 'warn', sep=',')

# Create datetime from "START TIME", "STOP TIME"
df_MM_clean_2019['START TIME'] = pd.to_datetime(df_MM_clean_2019['START TIME'])
df_MM_clean_2019['STOP TIME'] = pd.to_datetime(df_MM_clean_2019['STOP TIME'])

# Geoup by "BIKE ID"
group_bikes = df_MM_clean_2019.groupby("BIKE ID").agg({"TRIP DURATION": "sum",
                                                      "START TIME": "min",
                                                      "STOP TIME": "max"})

# Convert from seconds to minutes
group_bikes["TRIP DURATION (MINUTES)"] = group_bikes["TRIP DURATION"]/60

# Classic bike price of divvy = 0.17$/min


# Calculate the revenue
group_bikes["REVENUE (USD)"] = group_bikes["TRIP DURATION (MINUTES)"] * 0.17

# Calculate the total time that each bicycle exists on the streets
group_bikes["ACTIVE TIME"] = (group_bikes["STOP TIME"] - group_bikes["START TIME"]).dt.total_seconds() / 60

# Calculate the utilization percentage of each bike
group_bikes["utilization_percentage"] = ((group_bikes["TRIP DURATION (MINUTES)"] / group_bikes["ACTIVE TIME"]) * 100)

group_bikes.head()

group_bikes["utilization_percentage"].mean()
# The average of utilization percentage of bikes is about 3.8%.

group_bikes["utilization_percentage"].median()
group_bikes["utilization_percentage"].max()
group_bikes["utilization_percentage"].min()

group_bikes.sort_values("REVENUE (USD)", ascending = False).head()
# We can see that Bike 3846 with 48% utilization percentage, made about 31,519 dolar with 185,408 minutes trip.

total_revenue = group_bikes["REVENUE (USD)"].sum()
print(f'the total revenue is {total_revenue}')
# The revenue that we hav calculated, shows that in 2019, divvy made at least 15.68 M$.

# Costs for classic bikes per ye
bikes_price = 300
maintenance = 50
infrastructure = 800
technology = 30
insurance = 10
operations = 60
marketing = 20
unexpected_costs = 20

# Calculate the total cost for divvy per each bike
cost = bikes_price + maintenance + infrastructure + technology + insurance + operations + marketing + unexpected_costs
print(f'the cost for each bike in 2019 is {cost}')

group_bikes.count()

total_cost = 6017 * cost
print(f'the total cost in 2019 is {total_cost}')

interest = total_revenue - total_cost
print(f'the interest in 2019 is {interest}')
# I have estimated that there was about 8 M$ benefit for Divvy in 2019.

# ...........................................................................................

# During different day of week
group_bikes_week = df_MM_clean_2019.groupby(["BIKE ID", "Day_of_Week"]).agg({"TRIP DURATION": "sum",
                                                                          "START TIME": "min",
                                                                          "STOP TIME": "max"})

# Convert from seconds to minutes
group_bikes_week["TRIP DURATION (MINUTES)"] = group_bikes_week["TRIP DURATION"]/60

# Calculate the total time that each bicycle exists on the streets in each day of week
group_bikes_week["ACTIVE TIME"] = (group_bikes_week["STOP TIME"] - group_bikes_week["START TIME"]).dt.total_seconds() / 60

# Calculate the utilization percentage of each bike in each day of week
group_bikes_week["utilization_percentage"] = ((group_bikes_week["TRIP DURATION (MINUTES)"] / group_bikes_week["ACTIVE TIME"]) * 100)

group_bikes_week.head(14)

group_bikes_week.sort_values('utilization_percentage', ascending=False).head()

week_days = group_bikes_week.groupby("Day_of_Week").agg({"utilization_percentage": "mean"})

week_days.head(7)
# It shows that the average of utilization of bikes was more on weekends.


# The bar plot of average of utilization percentage within each day of week:
bp_week_days = week_days.plot(kind = "bar")

week_days_median = group_bikes_week.groupby("Day_of_Week").agg({"utilization_percentage": "median"})

week_days_median.head(7)

group_bikes.to_csv("group_bikes_2019_2", index=False)

group_bikes_week.to_csv("group_bikes_week_2019_2", index=False)

# This is the end of this Analysis. More analysis can be done in further efforts.
