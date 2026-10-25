

import pandas as pd
from pathlib import Path

# Define the input and output locations
INPUT_FILE = Path("data/yellow_tripdata_2026-01.parquet")
OUTPUT_FILE = Path("processed/yellow_tripdata_2026-01.parquet")


def create_distance_quality_flag(distances):
    """Flag trips with zero or negative distances for review."""
    return distances.le(0).map({True: "REVIEW", False: "PASS"})


def create_fare_quality_flag(fares):
    """Flag trips with negative fares for review."""
    return fares.lt(0).map({True: "REVIEW", False: "PASS"})


def main():
    print("Starting NYC Taxi data pipeline...")

    # Step 1: Load the original dataset
    df = pd.read_parquet(INPUT_FILE)
    print("Source records loaded:", len(df))

    # Step 2: Apply reusable data quality rules
    df["distance_quality_flag"] = create_distance_quality_flag(
        df["trip_distance"]
    )
    df["fare_quality_flag"] = create_fare_quality_flag(
        df["fare_amount"]
    )

    # Step 3: Create the output directory if needed
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Step 4: Save the transformed dataset
    df.to_parquet(OUTPUT_FILE, index=False)

    print(
        "Records flagged for distance review:",
        (df["distance_quality_flag"] == "REVIEW").sum(),
    )
    print(
        "Records passing distance check:",
        (df["distance_quality_flag"] == "PASS").sum(),
    )
    print(
        "Records flagged for fare review:",
        (df["fare_quality_flag"] == "REVIEW").sum(),
    )
    print(
        "Records passing fare check:",
        (df["fare_quality_flag"] == "PASS").sum(),
    )

    print("Processed records saved:", len(df))
    print("Output file:", OUTPUT_FILE)
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
