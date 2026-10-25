
import pandas as pd
from pathlib import Path

INPUT_FILE = Path("processed/yellow_tripdata_2026-01.parquet")
OUTPUT_FILE = Path("reports/daily_trip_summary.csv")


def main():
    print("Loading processed taxi data...")
    df = pd.read_parquet(INPUT_FILE)

    # Keep trips with pickup timestamps in January 2026
    start_date = pd.Timestamp("2026-01-01")
    end_date = pd.Timestamp("2026-02-01")

    df = df[
        (df["tpep_pickup_datetime"] >= start_date)
        & (df["tpep_pickup_datetime"] < end_date)
    ].copy()

    print("January trips included in report:", len(df))

    # Create a date column from the pickup timestamp
    df["pickup_date"] = df["tpep_pickup_datetime"].dt.date

    # Calculate daily business metrics
    daily_summary = (
        df.groupby("pickup_date")
        .agg(
            total_trips=("pickup_date", "size"),
            total_fare_amount=("fare_amount", "sum"),
            average_fare_amount=("fare_amount", "mean"),
            average_trip_distance=("trip_distance", "mean"),
        )
        .reset_index()
    )

    # Save the report
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    daily_summary.to_csv(OUTPUT_FILE, index=False)

    print("\n--- DAILY TRIP SUMMARY ---")
    print(daily_summary.head(5).to_string(index=False))
    print("\nDays summarized:", len(daily_summary))
    print("Report saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()

