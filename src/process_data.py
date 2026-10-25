

import logging
from pathlib import Path

import pandas as pd


# Define input and output locations
INPUT_FILE = Path("data/yellow_tripdata_2026-01.parquet")
OUTPUT_FILE = Path("processed/yellow_tripdata_2026-01.parquet")


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def create_distance_quality_flag(distances):
    """Flag trips with zero or negative distances for review."""
    return distances.le(0).map({True: "REVIEW", False: "PASS"})


def create_fare_quality_flag(fares):
    """Flag trips with negative fares for review."""
    return fares.lt(0).map({True: "REVIEW", False: "PASS"})


def main():
    """Load, validate, and save the NYC Taxi dataset."""
    logger.info("Starting NYC Taxi data pipeline")

    try:
        # Step 1: Check that the input file exists
        if not INPUT_FILE.exists():
            raise FileNotFoundError(
                f"Input dataset not found: {INPUT_FILE}"
            )

        # Step 2: Load the original dataset
        df = pd.read_parquet(INPUT_FILE)
        logger.info("Source records loaded: %s", len(df))

        # Step 3: Apply data quality rules
        df["distance_quality_flag"] = create_distance_quality_flag(
            df["trip_distance"]
        )
        df["fare_quality_flag"] = create_fare_quality_flag(
            df["fare_amount"]
        )

        # Step 4: Create the output directory
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Step 5: Save the processed dataset
        df.to_parquet(OUTPUT_FILE, index=False)

        # Step 6: Log quality-check results
        logger.info(
            "Records flagged for distance review: %s",
            (df["distance_quality_flag"] == "REVIEW").sum(),
        )
        logger.info(
            "Records passing distance check: %s",
            (df["distance_quality_flag"] == "PASS").sum(),
        )
        logger.info(
            "Records flagged for fare review: %s",
            (df["fare_quality_flag"] == "REVIEW").sum(),
        )
        logger.info(
            "Records passing fare check: %s",
            (df["fare_quality_flag"] == "PASS").sum(),
        )

        logger.info("Processed records saved: %s", len(df))
        logger.info("Output file: %s", OUTPUT_FILE)
        logger.info("Pipeline completed successfully")

    except Exception:
        logger.exception("NYC Taxi data pipeline failed")
        raise


if __name__ == "__main__":
    main()
