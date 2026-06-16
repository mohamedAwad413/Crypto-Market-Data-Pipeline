# Crypto Market Data Pipeline & Analytics Dashboard

An end-to-end Data Engineering pipeline designed to ingest, transform,
and visualize cryptocurrency market data in real-time.
This project implements a robust **Medallion Architecture**
using modern data stack tools to orchestrate and model high-frequency financial metrics, 
culminating in an executive-ready Power BI dashboard.

---

#  The Technical Stack

## PostgreSQL
PostgreSQL functions as the analytical data warehouse,
storing all pipeline outputs within a structured Medallion Architecture framework.
Data is organized across dedicated schemas:

Bronze Layer – Raw ingested API data
Silver Layer – Cleaned and standardized datasets
Gold Layer – Business-ready dimensional models and analytical tables

This layered approach improves data quality, maintainability, and governance.

---

#  Data Transformation & Dimensional Modeling

## dbt (Data Build Tool)
dbt powers the transformation layer by converting raw datasets into analytics-ready models. It is responsible for:

Data cleansing and standardization
Type casting and schema enforcement
Deduplication and validation checks
Building Fact and Dimension tables using the Kimball Dimensional Modeling approach

---
#  Infrastructure & Development Environment
## Docker & Docker Compose

Docker is used to containerize the entire platform, including Airflow and PostgreSQL services. This ensures:

Environment consistency
Simplified deployment
Reproducible development workflows
Platform portability across machines

---

# Docements

<table align="center">
  <tr>
    <td align="center" width="50%">
      <img src="docs/Dashboard-1.png" alt="img-1" width="100%"/>
    </td>
    <td align="center" width="50%">
      <img src="docs/Dashboard-2.png" alt="img-2" width="100%"/>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="docs/Data pipeline architecture.png" alt="img-3" width="100%"/>
    </td>
    <td align="center" width="50%">
      <img src="docs/Gold Layer.png" alt="img-4" width="100%"/>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="docs/crypto_bronze_ingestion.png" alt="img-4" width="100%"/>
    </td>
  </tr>
</table>
