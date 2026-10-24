import pandas as pd
from app import normalize_data, make_alerts

def test_zone_alias_and_alert_threshold():
    raw = pd.DataFrame({
        'date':['2026-10-01','2026-10-02','2026-10-03','2026-10-04'],
        'zone':['Lab 1']*4,
        'electricity_kwh':[100,100,100,130],
        'data_status':['MEASURED']*4,
    })
    df = normalize_data(raw)
    alerts = make_alerts(df,'electricity_kwh',pd.Timestamp('2026-10-01').date(),pd.Timestamp('2026-10-03').date(),25,1)
    assert len(alerts) == 1
    assert alerts.iloc[0]['change_pct'] == 30.0

def test_exact_threshold_triggers():
    df = normalize_data(pd.DataFrame({'date':['2026-10-01','2026-10-02'], 'building':['A','A'], 'water_m3':[2,2.5]}))
    alerts = make_alerts(df,'water_m3',pd.Timestamp('2026-10-01').date(),pd.Timestamp('2026-10-01').date(),25,1)
    assert len(alerts) == 1
