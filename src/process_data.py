
import logging
from pathlib import Path

import pandas as pd


INPUT_FILE = Path("data/yellow_tripdata_2026-01.parquet")
OUTPUT_FILE = Path("processed/yellow_tripdata_2026-01.parquet")

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
    """Load, validate, process, and reconcile the taxi dataset."""
    logger.info("Starting NYC Taxi data pipeline")

    try:
        # Step 1: Check that the source file exists
        if not INPUT_FILE.exists():
            raise FileNotFoundError(
                f"Input dataset not found: {INPUT_FILE}"
            )

        # Step 2: Load the source dataset
        df = pd.read_parquet(INPUT_FILE)
        source_count = len(df)
        logger.info("Source records loaded: %s", source_count)

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
        logger.info("Processed dataset written to: %s", OUTPUT_FILE)

        # Step 6: Read the saved output and reconcile record counts
        output_df = pd.read_parquet(OUTPUT_FILE)
        output_count = len(output_df)

        logger.info("Source record count: %s", source_count)
        logger.info("Output record count: %s", output_count)

        if source_count != output_count:
            raise ValueError(
                f"Record reconciliation failed: source={source_count}, "
                f"output={output_count}"
            )

        logger.info(
            "Record reconciliation passed: %s source records match "
            "the %s output records",
            source_count,
            output_count,
        )

        # Step 7: Log data quality results
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

        logger.info("Pipeline completed successfully")

    except Exception:
        logger.exception("NYC Taxi data pipeline failed")
        raise


if __name__ == "__main__":
    main()
