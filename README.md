\# NYC Taxi Data Engineering Platform



\## Project Overview

An end-to-end data engineering portfolio project using publicly available NYC Yellow Taxi trip records to explore data quality, transform raw data, and prepare reliable datasets for analytics.



\## Problem Statement

Real-world trip data can contain missing values, unusual trip distances, negative fares, and other records that require investigation before the data is used for reporting and analysis.



\## Objectives

\- Inspect and profile real-world taxi trip data.

\- Identify missing values, duplicate records, and suspicious values.

\- Develop repeatable data quality validation checks.

\- Transform raw records into analytics-ready datasets.

\- Document the pipeline and make the work reproducible.



\## Technology Stack

\- Python

\- Pandas

\- Parquet

\- Git and GitHub

\- SQL and Apache Spark — planned for later stages



\## Data Source

NYC Taxi \& Limousine Commission (TLC) Yellow Taxi trip records.



Official source: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page



Current dataset: January 2026 Yellow Taxi trip records.



The raw dataset is stored locally and excluded from Git version control.



\## Current Progress

\- Downloaded and loaded the January 2026 dataset.

\- Inspected 3,724,889 rows and 20 columns.

\- Examined missing values and exact duplicate rows.

\- Added initial checks for unusual trip distances and fare amounts.

\- Documented preliminary data quality findings.

\- Uploaded the initial code and documentation to GitHub.



\## Planned Next Steps

1\. Investigate suspicious records and define validation rules.

2\. Build a repeatable data cleaning process.

3\. Add automated data quality tests.

4\. Transform the data into analytics-ready tables.

5\. Explore SQL and distributed processing with Apache Spark.

6\. Document the completed workflow and results.



\*\*Project status:\*\* Initial profiling completed; pipeline development in progress.



