\# NYC Taxi Data Engineering Platform

\## Data Quality Findings — Day 1



\### 1. Dataset Overview

\- \*\*Source:\*\* NYC Taxi \& Limousine Commission (TLC) Yellow Taxi trip records

\- \*\*Data period:\*\* January 2026

\- \*\*Total records:\*\* 3,724,889

\- \*\*Total columns:\*\* 20

\- \*\*File format:\*\* Parquet



\### 2. Initial Data Quality Checks



| Check | Records Found |

|---|---:|

| Zero or negative trip distance | 125,738 |

| Trip distance greater than 100 miles | 162 |

| Negative fare amount | 39,463 |

| Zero fare amount | 2,082 |

| Exact duplicate rows | 0 |



\### 3. Initial Observations

\- Some trips have zero or negative distances and require investigation.

\- Trips exceeding 100 miles need review against business rules.

\- Negative fares may represent adjustments, reversals, or unusual records.

\- Zero-fare trips may be legitimate exceptions or data-quality issues.

\- No exact duplicate rows were detected by the initial duplicate-row check.

\- An exploratory filter identified 8,608 records with zero or negative trip distance, fare amounts of at least $40, and trip durations under one minute. These records require further investigation; they have not been classified as invalid or deleted.



\### 4. Important Decision

These findings are preliminary. No records have been deleted or modified. Further investigation is required before classifying records as invalid.



\### 5. Next Steps

\- Investigate suspicious records.

\- Define and document data-quality rules.

\- Build a repeatable validation process.

\- Preserve the original source data.





\### 6. Pipeline Implementation



The `src/process\_data.py` script reads the original January 2026 Yellow Taxi Parquet dataset, applies data-quality flags, and saves the transformed dataset to the `processed/` directory.



\#### Quality Rules Implemented



| Quality Rule | Condition | Flag |

|---|---|---|

| Distance check | `trip\_distance <= 0` | `REVIEW` |

| Distance check | `trip\_distance > 0` | `PASS` |

| Fare check | `fare\_amount < 0` | `REVIEW` |

| Fare check | `fare\_amount >= 0` | `PASS` |



\#### Pipeline Results



| Metric | Records |

|---|---:|

| Total records processed | 3,724,889 |

| Distance flagged for review | 125,738 |

| Distance passing the check | 3,599,151 |

| Negative fares flagged for review | 39,463 |

| Fares passing the check | 3,685,426 |



The output contains the original 20 columns and two additional columns:

\- `distance\_quality\_flag`

\- `fare\_quality\_flag`



All source records are retained. Records flagged for review are not automatically deleted because unusual values may represent legitimate business exceptions.



\#### Limitations



These checks cover only trip distance and fare amount. A `PASS` result does not guarantee that a record is valid across every data-quality dimension. Additional validation rules and business requirements are needed.



\## 4. Daily Business Analytics



\### Objective

Generate a daily summary of NYC yellow taxi activity for January 2026 using the processed dataset.



\### Metrics

\- Total trips per day

\- Total fare amount per day

\- Average fare amount per day

\- Average trip distance per day



\### Reporting Period Validation

The processed dataset contains 3,724,889 records. Pickup timestamps were checked against the January 2026 reporting period.



\- Records before January 1, 2026: 6

\- Records during January 2026: 3,724,882

\- Records on or after February 1, 2026: 1



The analytics script filters records to January 1 through January 31, 2026, using an exclusive February 1 end boundary. This ensures that only January pickups appear in the daily report.



\### Output

The script generates `reports/daily\_trip\_summary.csv`, containing 31 daily summaries.



\### Data Handling

Records outside the reporting period are excluded from this monthly report only. They remain in the processed dataset. The pipeline preserves source records rather than silently deleting data.







