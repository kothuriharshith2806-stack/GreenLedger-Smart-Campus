# GreenLedger — Campus Resource Optimisation

A laptop-only Streamlit dashboard for manual readings or CSV uploads, dynamic charts, resource summaries, threshold alerts, and follow-up actions. It does not connect to live meters and does not physically switch appliances.

## Run on Windows
1. Install Python 3.10 or newer from python.org and select **Add Python to PATH**.
2. Extract this ZIP to a folder.
3. Open Command Prompt in that folder.
4. Run:
   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install -r requirements.txt
   python -m streamlit run app.py
   ```
5. Open the local address Streamlit prints (normally `http://localhost:8501`).

## Add real data
Use **Upload your campus readings CSV** in the sidebar. Required columns: `date` and `building`; `zone` is also accepted. Include at least one numeric resource column:
- `electricity_kwh` (kWh/day)
- `solar_generation_kwh` (kWh/day)
- `water_m3` (m³/day)
- `waste_kg` (kg/day)

Optional columns: `data_status`, `notes`, `occupancy_pct`. Use daily totals consistently. Label data accurately as MEASURED, BILL-BASED, ESTIMATED or SIMULATED. Do not include personal/student data. You can also add daily readings in the app. Choose which resources were actually measured; unticked resources stay blank, while a real zero reading is retained. Charts and alerts refresh from the active dataset. Download the current readings CSV to save/share the updated data. Manual additions persist during the current app session; download the CSV before closing the app.

## How alerts work
- Select baseline start/end dates.
- The baseline is the average for each zone over those dates.
- Each later reading is compared with that zone's baseline.
- At a 25% threshold, 100 kWh baseline and 125 kWh later reading triggers an alert.
- Baselines of zero/missing values are skipped; a zone needs a later reading to alert.
- An alert is an investigation prompt, not proof of a fault. Verify the meter, operating hours, occupancy and data source before action.

## Data and safety
The included CSV is synthetic demo data, not verified campus data. Solar generation is not automatically subtracted from electricity consumption because on-site generation, export and meter boundaries must be verified first. No live meter connection, automatic appliance shutdown, or real savings claim is provided. Physical control would require authorised compatible equipment, electrical protection and qualified campus staff.

## Tests
`test_alert_logic.py` documents the threshold scenarios. The core alert logic was smoke-tested during packaging. The full Streamlit UI still needs to be launched and checked on the user's laptop after dependencies are installed.
