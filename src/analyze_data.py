
import logging
from pathlib import Path

import pandas as pd


INPUT_FILE = Path("processed/yellow_tripdata_2026-01.parquet")
OUTPUT_DIR = Path("reports")
OUTPUT_FILE = OUTPUT_DIR / "daily_trip_summary.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    """Generate daily business metrics from processed taxi data."""
    logger.info("Starting NYC Taxi daily analytics")

    try:
        if not INPUT_FILE.exists():
            raise FileNotFoundError(
                f"Processed dataset not found: {INPUT_FILE}. "
                "Run src/process_data.py first."
            )

        df = pd.read_parquet(INPUT_FILE)
        logger.info("Loaded %s processed records", len(df))

        # Keep trips with pickup timestamps in January 2026.
        df["tpep_pickup_datetime"] = pd.to_datetime(
            df["tpep_pickup_datetime"],
            errors="coerce",
        )

        january_start = pd.Timestamp("2026-01-01")
        february_start = pd.Timestamp("2026-02-01")

        january_df = df.loc[
            (df["tpep_pickup_datetime"] >= january_start)
            & (df["tpep_pickup_datetime"] < february_start)
        ].copy()

        if january_df.empty:
            raise ValueError("No January 2026 trips found in the dataset")

        logger.info("January trips selected: %s", len(january_df))

        # Create a daily grouping key.
        january_df["pickup_date"] = (
            january_df["tpep_pickup_datetime"].dt.date
        )

        # Calculate daily business metrics.
        daily_summary = (
            january_df.groupby("pickup_date")
            .agg(
                total_trips=("pickup_date", "size"),
                total_fare_amount=("fare_amount", "sum"),
                average_fare_amount=("fare_amount", "mean"),
                average_trip_distance=("trip_distance", "mean"),
                total_passenger_count=("passenger_count", "sum"),
            )
            .reset_index()
        )

        # Round averages for readability.
        daily_summary["average_fare_amount"] = (
            daily_summary["average_fare_amount"].round(2)
        )
        daily_summary["average_trip_distance"] = (
            daily_summary["average_trip_distance"].round(2)
        )

        # Save the report.
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        daily_summary.to_csv(OUTPUT_FILE, index=False)

        logger.info("Report days generated: %s", len(daily_summary))
        logger.info("Report saved to: %s", OUTPUT_FILE)
        logger.info("January trips analyzed: %s", int(daily_summary["total_trips"].sum()))
        logger.info("Analytics completed successfully")

    except Exception:
        logger.exception("NYC Taxi analytics failed")
        raise


if __name__ == "__main__":
    main()
