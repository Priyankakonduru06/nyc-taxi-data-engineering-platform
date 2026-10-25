# NYC Taxi Data Engineering Platform

An end-to-end data engineering portfolio project built using real-world NYC Yellow Taxi trip records. The project demonstrates data profiling, validation, transformation, record-count reconciliation, automated testing, and daily analytics using Python and pandas.

## Project Overview

Real-world data can contain invalid values, missing fields, and unusual records that affect downstream analytics. This project builds a repeatable workflow to identify data quality issues, preserve source records, produce a processed dataset, and generate daily business metrics.

**Dataset:** NYC Yellow Taxi trip records for January 2026  
**Source records:** 3,724,889  
**Processing approach:** Python, pandas, and Parquet

## Architecture

The pipeline follows this workflow:

1. Load the raw Yellow Taxi Parquet dataset.
2. Profile records and inspect data quality.
3. Add quality flags for suspicious trip distances and fares.
4. Save the processed dataset without modifying the raw source.
5. Reconcile input and output record counts.
6. Generate daily analytics and export a CSV report.
7. Run automated tests for core data quality rules.

See the [architecture diagram](docs/architecture.md) for the pipeline components and data flow.

## Technology Stack

- **Python** — pipeline implementation and data processing
- **pandas** — data profiling, transformation, and aggregation
- **Parquet** — columnar dataset storage
- **pytest** — automated testing
- **Git and GitHub** — version control and project documentation

## Data Quality Findings

Initial profiling identified the following issues in the source dataset:

| Check | Finding |
|---|---:|
| Total source records | 3,724,889 |
| Total columns | 20 |
| Records with zero or negative trip distance | 125,738 |
| Records with negative fare amounts | 39,463 |
| Exact duplicate rows | 0 |
| Suspicious records selected for further review | 8,608 |

The 8,608 records are candidates for investigation based on a combined filter involving non-positive distance, fare amounts of at least $40, and trip duration under one minute. They are not confirmed fraud or confirmed invalid trips.

Missing values were also found in several fields, including passenger count, rate code, store-and-forward flag, congestion surcharge, and airport fee. Missing values are assessed in context rather than automatically treated as errors.

See [data quality findings](docs/data_quality_findings.md) for additional details.

## Processing and Reconciliation

The processing pipeline:

- Adds a distance quality flag: `REVIEW` for distances less than or equal to zero, otherwise `PASS`.
- Adds a fare quality flag: `REVIEW` for negative fares, otherwise `PASS`.
- Writes the processed dataset to `processed/`.
- Compares source and output record counts.
- Logs pipeline progress, validation results, and failures.

**Verified result:** 3,724,889 source records and 3,724,889 processed records. Record-count reconciliation passed.

Records are flagged for review rather than automatically deleted. The raw source file remains unchanged.

## Daily Analytics

The analytics script filters records by pickup timestamp to select January 2026 trips, groups them by pickup date, and exports a daily CSV report.

Metrics include:

- Daily trip count
- Total fare amount
- Average fare amount
- Average trip distance
- Total passenger count

The current report contains 3,724,882 January trips across 31 calendar dates. Seven source records fall outside the January pickup-timestamp window and are excluded from this report.

The total fare amount is a sum of recorded fare fields, not a measure of company revenue or profit.

## Repository Structure

```text
nyc-taxi-data-engineering-platform/
├── data/                       # Local raw dataset; excluded from Git
├── docs/
│   ├── architecture.md
│   └── data_quality_findings.md
├── processed/                  # Generated processed data; excluded from Git
├── reports/                    # Generated analytics reports; excluded from Git
├── sql/                        # SQL project area
├── src/
│   ├── inspect_data.py
│   ├── validate_data.py
│   ├── process_data.py
│   └── analyze_data.py
├── tests/
│   └── test_data_quality.py
├── .gitignore
├── requirements.txt
└── README.md
```

Generated datasets and reports are kept locally and excluded from version control.

## Getting Started

### Requirements

- Python 3.13 or a compatible Python environment
- The January 2026 Yellow Taxi Parquet dataset from the official NYC TLC data source
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Priyankakonduru06/nyc-taxi-data-engineering-platform.git
cd nyc-taxi-data-engineering-platform
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Add the source dataset

Download the January 2026 Yellow Taxi Parquet file from the [official NYC TLC trip record data page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) and place it at:

```text
data/yellow_tripdata_2026-01.parquet
```

### 4. Run the processing pipeline

```bash
python src/process_data.py
```

### 5. Generate daily analytics

```bash
python src/analyze_data.py
```

The analytics script expects the processed Parquet file to exist, so run the processing pipeline first.

### 6. Run automated tests

```bash
python -m pytest -v
```

## Current Status

Implemented:
- Source data inspection and profiling
- Data quality validation and findings documentation
- Distance and fare quality flags
- Structured logging and error handling
- Input/output record-count reconciliation
- Automated tests for quality rules and edge cases
- Daily analytics and CSV reporting
- Architecture and data quality documentation

## Future Enhancements

- Add continuous integration to run tests automatically on GitHub.
- Expand data quality rules and test coverage.
- Add SQL-based analytical transformations.
- Explore Apache Spark or Databricks for distributed processing.
- Add data orchestration and pipeline scheduling.
- Add reporting visualizations for daily trends.

## Data Source

NYC Taxi & Limousine Commission (TLC): [Official trip record data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

This is an educational portfolio project using public trip records. Quality flags identify records for review; they do not independently establish fraud or definitive data invalidity.
