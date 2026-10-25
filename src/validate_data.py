
import pandas as pd

FILE_PATH = "data/yellow_tripdata_2026-01.parquet"


def load_data(file_path):
    """Load the source Parquet dataset."""
    print("Loading taxi dataset...")
    return pd.read_parquet(file_path)


def validate_data(df):
    """Run basic data-quality checks."""
    invalid_distance = df[df["trip_distance"] <= 0].copy()
    negative_fares = df[df["fare_amount"] < 0]
    duplicate_rows = df.duplicated().sum()
    missing_values = df.isnull().sum()

    print("\n--- DATA QUALITY REPORT ---")
    print("Total taxi trips:", len(df))
    print("Trips with zero or negative distance:", len(invalid_distance))
    print("Trips with negative fares:", len(negative_fares))
    print("Exact duplicate rows:", duplicate_rows)

    print("\nMissing values per column:")
    print(missing_values[missing_values > 0])

    return invalid_distance


def investigate_suspicious_trips(invalid_distance):
    """Investigate unusual records without deleting them."""
    invalid_distance["trip_duration_minutes"] = (
        invalid_distance["tpep_dropoff_datetime"]
        - invalid_distance["tpep_pickup_datetime"]
    ).dt.total_seconds() / 60

    suspicious_trips = invalid_distance[
        (invalid_distance["fare_amount"] >= 40)
        & (invalid_distance["trip_duration_minutes"] < 1)
    ]

    print("\n--- SUSPICIOUS TRIP INVESTIGATION ---")
    print("Records matching investigation criteria:", len(suspicious_trips))

    print("\nFirst 5 matching records:")
    print(
        suspicious_trips[
            [
                "trip_distance",
                "fare_amount",
                "total_amount",
                "trip_duration_minutes",
            ]
        ].head()
    )


def main():
    df = load_data(FILE_PATH)
    invalid_distance = validate_data(df)
    investigate_suspicious_trips(invalid_distance)


if __name__ == "__main__":
    main()

