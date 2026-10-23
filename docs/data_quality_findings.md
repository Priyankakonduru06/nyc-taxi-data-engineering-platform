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



\### 4. Important Decision

These findings are preliminary. No records have been deleted or modified. Further investigation is required before classifying records as invalid.



\### 5. Next Steps

\- Investigate suspicious records.

\- Define and document data-quality rules.

\- Build a repeatable validation process.

\- Preserve the original source data.





