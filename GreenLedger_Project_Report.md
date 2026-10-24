# GreenLedger: Campus Resource Optimisation
## Sustainability & Climate Action — Hackathon Project Report

### 1. Abstract
GreenLedger is a software prototype designed to bring campus electricity, water, and waste records into one dashboard. It compares readings against a historical baseline, highlights unusual changes, supports an action register, and exports reports. The prototype runs locally on a laptop and does not require Arduino, sensors, or other hardware.

### 2. Problem statement
Campus resource records are often maintained separately. This makes it difficult to spot unusual consumption, compare current readings with a reference period, and follow up on potential wastage. GreenLedger provides a common view and a simple review workflow.

### 3. Objectives
- Combine electricity, water, and waste readings in one interface.
- Compare daily readings with a per-building baseline.
- Flag possible unusual consumption for human review.
- Track proposed corrective actions and their status.
- Export data and reports for review.

### 4. Proposed solution
The user uploads or uses a CSV dataset. Python and Pandas validate and aggregate the data. Streamlit presents KPIs, trend charts, building comparisons, baseline calculations, threshold alerts, and an editable action register. Plotly renders charts. CSV and text exports support reporting.

### 5. Architecture
**CSV data → Pandas validation and calculations → baseline/threshold alert logic → Streamlit dashboard → action register and exports**

### 6. Technology stack
- Python: application logic
- Streamlit: local web interface
- Pandas: data cleaning, aggregation and export
- Plotly: interactive charts
- CSV: portable input and storage format

### 7. Data model
Each reading contains date, building, electricity_kwh, water_m3, waste_kg, and data_status. The sample dataset contains 90 days across three example buildings. Every sample row is labelled `SYNTHETIC SAMPLE — NOT MEASURED`.

### 8. Baseline and alert method
For each building and resource, the baseline is the average daily value across the user-selected baseline period. For a later reading:

**Percentage change = ((reading − baseline) / baseline) × 100**

An alert is generated when percentage change is at least the configured threshold. The default threshold is 25%. A larger increase is labelled “High”; other qualifying increases are labelled “Review”. This is a screening rule only. It is not proof of a leak, faulty equipment, or avoidable waste.

### 9. Expected output
- Summary totals for electricity, water, and waste
- Resource time-series charts
- Building comparison chart
- Baseline and current-period comparison
- Unusual-consumption alert table
- Editable action register
- Downloadable CSV files and text report

### 10. Demonstration plan
1. Launch the dashboard with the sample dataset.
2. Explain the warning that the readings are synthetic.
3. Select the Academic Block and a reporting window.
4. Show a resource trend and baseline comparison.
5. Adjust the alert threshold and show how alerts change.
6. Add an action such as “Inspect schedule and verify meter record”, assign an owner, and save.
7. Download the alert CSV and report.

### 11. Testing plan
- Start-up test: dashboard loads from the supplied sample file.
- Filter test: building and date filters update the dashboard.
- Baseline test: baseline values are displayed for selected dates.
- Alert test: changing threshold changes the number of flagged readings.
- Export test: alert CSV, action CSV, filtered readings and report download.
- Upload test: a CSV matching `data/upload_template.csv` loads.
- Validation test: missing columns trigger an error.

### 12. Data quality and ethical use
The sample dataset is synthetic and must not be presented as actual campus measurement. For a real pilot, collect authorised utility bills, meter readings, water logs and waste records. Keep source identifiers and timestamps. Label estimates separately from measurements. Have facilities staff verify alerts before action. Do not claim measured savings, emissions reductions, or financial benefits without evidence and documented calculation factors.

### 13. Limitations and future improvements
Current alerts do not account for occupancy, weather, holidays, campus calendar, floor area, or meter anomalies. The app does not provide authentication or multi-user cloud storage. Future work could add role-based access, audit trails, scheduled imports, weather/occupancy normalization, local tariff and emissions factors with citations, and validation against actual facility records.

### 14. Conclusion
GreenLedger demonstrates a practical first step toward campus resource visibility using only a laptop and open-source Python tools. It combines simple trend analysis with a human-reviewed action workflow while keeping the distinction between synthetic demonstration data and verified measurements explicit.
