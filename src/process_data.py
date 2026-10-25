
import pandas as pd
from pathlib import Path

# Define the input and output locations
input_file = Path("data/yellow_tripdata_2026-01.parquet")
output_file = Path("processed/yellow_tripdata_2026-01.parquet")


def main():
    print("Starting NYC Taxi data pipeline...")

    # Step 1: Load the original dataset
    df = pd.read_parquet(input_file)
    print("Source records loaded:", len(df))


    # Step 2: Flag trips with zero or negative distance
    df["distance_quality_flag"] = "PASS"
    df.loc[df["trip_distance"] <= 0, "distance_quality_flag"] = "REVIEW"
    # Step 3: Flag trips with negative fares
    df["fare_quality_flag"] = "PASS"
    df.loc[df["fare_amount"] < 0, "fare_quality_flag"] = "REVIEW"

    # Step 4 : Save the transformed dataset
    df.to_parquet(output_file, index=False)

    print("Records flagged for review:", (df["distance_quality_flag"] == "REVIEW").sum())
    print("Records passing distance check:", (df["distance_quality_flag"] == "PASS").sum())
    print("Records with negative fares:", (df["fare_quality_flag"] == "REVIEW").sum())
    print("Records passing fare check:", (df["fare_quality_flag"] == "PASS").sum())

    print("Processed records saved:", len(df))
    print("Output file:", output_file)
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
