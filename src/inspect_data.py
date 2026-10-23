import pandas as pd

file_path = "data/yellow_tripdata_2026-01.parquet"

df = pd.read_parquet(file_path)

print("Dataset loaded successfully!")
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values per column:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print("\nTrip distance summary:")
print(df["trip_distance"].describe())

print("\nFare amount summary:")
print(df["fare_amount"].describe())

print("\nTrips with zero or negative distance:")
print((df["trip_distance"] <= 0).sum())

print("\nTrips with distance greater than 100 miles:")
print((df["trip_distance"] > 100).sum())

print("\nTrips with negative fares:")
print((df["fare_amount"] < 0).sum())

print("\nTrips with zero fares:")
print((df["fare_amount"] == 0).sum())