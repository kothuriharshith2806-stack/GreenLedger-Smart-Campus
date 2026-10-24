from datetime import date, timedelta
from pathlib import Path
import io
import pandas as pd
import plotly.express as px
import streamlit as st

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / 'data'
DEFAULT_DATA = DATA_DIR / 'sample_resource_readings.csv'
ACTIONS_PATH = DATA_DIR / 'action_register.csv'
DATA_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title='GreenLedger | Campus Resource Optimisation', page_icon='🌱', layout='wide')
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root { --gl-ink:#142b35; --gl-muted:#617782; --gl-green:#16835f; --gl-lime:#b8ef72; --gl-line:#dce9e5; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background: linear-gradient(135deg,#f4faf7 0%,#f7fafc 52%,#eef6f2 100%); color:var(--gl-ink); }
.block-container {padding-top:1.35rem;padding-bottom:2.8rem;max-width:1500px;}
[data-testid="stHeader"] {background:rgba(244,250,247,.86);}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#102f35 0%,#164c43 100%);border-right:1px solid #2e6658;}
[data-testid="stSidebar"] * {color:#f1faf5 !important;}
[data-testid="stSidebar"] [data-baseweb="select"] > div {background:#214c48;border-color:#4b776d;}
[data-testid="stSidebar"] input,[data-testid="stSidebar"] textarea {background:#214c48 !important;color:#fff !important;}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {font-weight:600;}
[data-testid="stSidebar"] hr {border-color:#3b6a60;}
h1,h2,h3,h4 {font-family:'Manrope',sans-serif !important;color:#163c3a;letter-spacing:-.035em;}
h1 {font-weight:800 !important;font-size:2.35rem !important;}
h2 {font-weight:800 !important;}
h3 {font-weight:750 !important;}
[data-testid="stMetric"] {background:linear-gradient(145deg,#ffffff 0%,#eaf7ef 100%);border:1px solid #d6e9de;padding:18px 18px;border-radius:18px;box-shadow:0 5px 18px rgba(24,75,60,.055);}
[data-testid="stMetricLabel"] {color:#56736a !important;font-weight:700;}
[data-testid="stMetricValue"] {color:#117653 !important;font-family:'Manrope',sans-serif;font-weight:800;}
[data-testid="stMetricDelta"] {font-weight:600;}
[data-testid="stExpander"] {background:rgba(255,255,255,.82);border:1px solid #dce9e5;border-radius:14px;}
div[data-testid="stAlert"] {border-radius:14px;border:1px solid #dce9e5;}
.stButton > button,.stDownloadButton > button,[data-testid="stFormSubmitButton"] button {border-radius:11px;border:0;background:linear-gradient(110deg,#147b59,#21a477);color:#fff;font-weight:700;box-shadow:0 4px 12px rgba(20,123,89,.18);transition:transform .15s,box-shadow .15s;}
.stButton > button:hover,.stDownloadButton > button:hover,[data-testid="stFormSubmitButton"] button:hover {background:linear-gradient(110deg,#106749,#18865e);color:white;transform:translateY(-1px);box-shadow:0 7px 16px rgba(20,123,89,.22);}
[data-testid="stDataFrame"],[data-testid="stTable"] {border:1px solid #dce9e5;border-radius:13px;overflow:hidden;}
[data-testid="stPlotlyChart"] {background:#fff;border:1px solid #e0ece7;border-radius:17px;padding:8px;box-shadow:0 5px 18px rgba(24,75,60,.04);}
hr {border-color:#dce9e5;}
[data-testid="stCaptionContainer"] {color:#617782;}
.gl-hero {background:linear-gradient(120deg,#103b3b 0%,#176c51 58%,#2b9b6c 100%);padding:27px 30px;border-radius:22px;color:#f4fff8;margin:0 0 18px 0;box-shadow:0 12px 30px rgba(17,76,57,.16);position:relative;overflow:hidden;}
.gl-hero:after {content:' ';position:absolute;width:240px;height:240px;border:1px solid rgba(255,255,255,.16);border-radius:50%;right:-55px;top:-110px;box-shadow:0 0 0 28px rgba(255,255,255,.04),0 0 0 58px rgba(255,255,255,.03);}
.gl-kicker {text-transform:uppercase;letter-spacing:.14em;font-size:.72rem;font-weight:800;color:#c8f4d6;margin-bottom:8px;}
.gl-title {font-family:'Manrope',sans-serif;font-size:2.15rem;font-weight:800;letter-spacing:-.045em;color:white;line-height:1.12;}
.gl-sub {color:#e0f5e8;font-size:.96rem;margin-top:8px;max-width:750px;}
.gl-chip {display:inline-block;background:rgba(205,255,222,.14);border:1px solid rgba(220,255,233,.25);border-radius:999px;padding:6px 10px;font-size:.76rem;font-weight:700;margin:14px 7px 0 0;color:#f5fff8;}
.gl-section {font-size:1.22rem;font-weight:800;font-family:'Manrope',sans-serif;color:#173e39;margin:1.25rem 0 .2rem;}
@media (max-width: 700px) {.block-container{padding-left:1rem;padding-right:1rem}.gl-title{font-size:1.7rem}.gl-hero{padding:22px}}
</style>
""", unsafe_allow_html=True)
st.markdown('''<div class="gl-hero"><div class="gl-kicker">Campus sustainability intelligence</div><div class="gl-title">🌿 GreenLedger</div><div class="gl-sub">One clear view of campus energy, solar generation, water and waste — turn your readings into useful decisions.</div><span class="gl-chip">✦ Manual data entry</span><span class="gl-chip">↗ Live-updating charts</span><span class="gl-chip">♧ Smart threshold alerts</span><span class="gl-chip">▤ Exportable reports</span></div>''', unsafe_allow_html=True)
st.info('Start with a CSV upload or add readings manually. Charts, totals and threshold alerts are recalculated from your active dataset. Sample readings are simulated; this prototype does not connect to live meters or switch appliances.')

RESOURCE_CONFIG = {
    'Electricity': {'column':'electricity_kwh','unit':'kWh'},
    'Water': {'column':'water_m3','unit':'m³'},
    'Waste': {'column':'waste_kg','unit':'kg'},
    'Solar generation': {'column':'solar_generation_kwh','unit':'kWh'},
}
ALIASES = {'zone':'building','location':'building','area':'building','date_time':'date','timestamp':'date','solar_kwh':'solar_generation_kwh','solar_generation':'solar_generation_kwh','electricity':'electricity_kwh','water':'water_m3','waste':'waste_kg'}
REQUIRED_ID = ['date','building']
NUMERIC_COLUMNS = [v['column'] for v in RESOURCE_CONFIG.values()] + ['occupancy_pct']

SAMPLE_COLUMNS = ['date','building','electricity_kwh','solar_generation_kwh','water_m3','waste_kg','occupancy_pct','data_status','notes']

def normalize_data(raw):
    df = raw.copy()
    df.columns = [str(c).strip().lower().replace(' ','_').replace('-','_') for c in df.columns]
    df = df.rename(columns={c: ALIASES[c] for c in df.columns if c in ALIASES})
    missing_id = [c for c in REQUIRED_ID if c not in df.columns]
    if missing_id:
        raise ValueError('Missing required columns: ' + ', '.join(missing_id) + '. Include date and building (or zone).')
    available = [c for c in NUMERIC_COLUMNS if c in df.columns]
    if not available:
        raise ValueError('Add at least one numeric resource column: electricity_kwh, water_m3, waste_kg, or solar_generation_kwh.')
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.normalize()
    df['building'] = df['building'].astype('string').str.strip()
    for c in NUMERIC_COLUMNS:
        if c not in df.columns:
            df[c] = float('nan')
        df[c] = pd.to_numeric(df[c], errors='coerce')
    if 'data_status' not in df.columns:
        df['data_status'] = 'MEASURED (user supplied; unverified)'
    else:
        df['data_status'] = df['data_status'].fillna('UNSPECIFIED').astype(str).str.strip()
    if 'notes' not in df.columns:
        df['notes'] = ''
    df['notes'] = df['notes'].fillna('').astype(str)
    df = df.dropna(subset=['date','building'])
    df = df[df['building'].ne('')]
    if df.empty:
        raise ValueError('No valid rows remain after checking dates and building/zone names.')
    return df.sort_values(['date','building']).reset_index(drop=True)

def load_default():
    if DEFAULT_DATA.exists():
        try:
            return normalize_data(pd.read_csv(DEFAULT_DATA)), None
        except Exception as e:
            return pd.DataFrame(), str(e)
    return pd.DataFrame(), None

def baseline_map(df, col, start, end):
    part = df[(df.date.dt.date >= start) & (df.date.dt.date <= end)].dropna(subset=[col])
    if part.empty:
        return {}
    return part.groupby('building')[col].mean().to_dict()

def make_alerts(df, col, start, end, threshold, min_baseline_rows):
    base_part = df[(df.date.dt.date >= start) & (df.date.dt.date <= end)].dropna(subset=[col])
    current_part = df[df.date.dt.date > end].dropna(subset=[col])
    if current_part.empty or base_part.empty:
        return pd.DataFrame(columns=['date','building','resource','current_value','baseline_avg','change_pct','severity','data_status','recommended_check'])
    counts = base_part.groupby('building')[col].count().to_dict()
    bases = base_part.groupby('building')[col].mean().to_dict()
    rows=[]
    for _, r in current_part.iterrows():
        b = r['building']; base = bases.get(b)
        if base is None or pd.isna(base) or base <= 0 or counts.get(b,0) < min_baseline_rows:
            continue
        change = (float(r[col])-float(base))/float(base)*100
        if change >= threshold:
            rows.append({'date':r['date'].date().isoformat(),'building':b,'current_value':round(float(r[col]),2),'baseline_avg':round(float(base),2),'change_pct':round(change,1),'severity':'High' if change >= threshold*1.5 else 'Review','data_status':r['data_status'],'recommended_check':'Verify source reading, operating hours, occupancy and any leaks/waste spike before action.'})
    out=pd.DataFrame(rows)
    if not out.empty:
        out['resource']=col
    return out

st.sidebar.header('1. Data source')
uploaded = st.sidebar.file_uploader('Upload your campus readings CSV', type=['csv'])
if uploaded is not None:
    try:
        raw = pd.read_csv(uploaded)
        data = normalize_data(raw)
        st.sidebar.success(f'Loaded uploaded data: {len(data)} valid rows')
    except Exception as e:
        st.error(f'Could not read this CSV: {e}')
        st.stop()
else:
    data, err = load_default()
    if err:
        st.error('Sample data could not be loaded: '+err); st.stop()
    if data.empty:
        st.warning('No sample file found. Upload a CSV or add readings in the manual-entry section below.')

with st.expander('CSV format: how to add real data', expanded=False):
    st.markdown('Required: **date** and **building** (the app also accepts **zone**). Add any one or more resource columns. Missing resource types are allowed.')
    st.code('date,zone,electricity_kwh,solar_generation_kwh,water_m3,waste_kg,data_status,notes\n2026-10-20,Computer Lab 1,42.5,0,1.8,3.2,MEASURED,Submeter reading', language='csv')
    st.markdown('Use daily totals with consistent units: electricity and solar in kWh/day, water in m³/day, waste in kg/day. Keep **SIMULATED** and **MEASURED** labels honest. Avoid student names or personal data.')
    template = pd.DataFrame(columns=SAMPLE_COLUMNS)
    st.download_button('Download CSV template', template.to_csv(index=False).encode('utf-8'), 'greenledger_real_data_template.csv', 'text/csv')

st.markdown('<div class="gl-section">✚ Record a reading manually</div>', unsafe_allow_html=True)
with st.expander('Add a measured daily reading', expanded=False):
    with st.form('manual_reading_form'):
        c1,c2,c3 = st.columns(3)
        entry_date = c1.date_input('Reading date', value=date.today())
        existing_buildings = sorted(data['building'].dropna().unique().tolist()) if not data.empty else []
        building_name = c2.text_input('Building / zone', value=existing_buildings[0] if existing_buildings else '')
        status = c3.selectbox('Data status', ['MEASURED','BILL-BASED','ESTIMATED','SIMULATED'])
        st.caption('Tick each resource you measured. A value of 0 is accepted when it is a real reading; unticked resources remain blank.')
        c4,c5,c6,c7 = st.columns(4)
        use_e = c4.checkbox('Record electricity', value=True)
        e_val = c4.number_input('Electricity (kWh)', min_value=0.0, value=0.0, step=1.0, disabled=not use_e)
        use_s = c5.checkbox('Record solar', value=False)
        s_val = c5.number_input('Solar generation (kWh)', min_value=0.0, value=0.0, step=1.0, disabled=not use_s)
        use_w = c6.checkbox('Record water', value=False)
        w_val = c6.number_input('Water (m³)', min_value=0.0, value=0.0, step=0.1, disabled=not use_w)
        use_waste = c7.checkbox('Record waste', value=False)
        waste_val = c7.number_input('Waste (kg)', min_value=0.0, value=0.0, step=0.1, disabled=not use_waste)
        notes = st.text_input('Notes / source (optional)', placeholder='e.g. meter ID, bill date, reading source')
        submitted = st.form_submit_button('＋ Add reading')
    if submitted:
        if not building_name.strip():
            st.error('Enter a building or zone name.')
        elif not any([use_e, use_s, use_w, use_waste]):
            st.error('Select at least one resource to record.')
        else:
            new = {'date':pd.Timestamp(entry_date),'building':building_name.strip(),
                   'electricity_kwh':e_val if use_e else float('nan'),
                   'solar_generation_kwh':s_val if use_s else float('nan'),
                   'water_m3':w_val if use_w else float('nan'),
                   'waste_kg':waste_val if use_waste else float('nan'),
                   'occupancy_pct':float('nan'),'data_status':status,'notes':notes}
            current = st.session_state.get('greenledger_manual_data', data)
            data = pd.concat([current,pd.DataFrame([new])],ignore_index=True).sort_values(['date','building']).reset_index(drop=True)
            st.session_state['greenledger_manual_data'] = data
            st.success('Reading added. Charts, totals and alerts now use this reading; download the current CSV to keep a copy.')

# Persist manual additions across reruns during this app session.
if 'greenledger_manual_data' in st.session_state and uploaded is None:
    data = st.session_state['greenledger_manual_data']

if data.empty:
    st.stop()

st.sidebar.header('3. Filters')
buildings = sorted(data['building'].unique().tolist())
selected_buildings = st.sidebar.multiselect('Buildings / zones', buildings, default=buildings)
min_date, max_date = data['date'].min().date(), data['date'].max().date()
period = st.sidebar.date_input('Reporting period', value=(min_date,max_date), min_value=min_date, max_value=max_date, key='report_period')
if isinstance(period,(tuple,list)) and len(period)==2:
    report_start, report_end=period
else:
    report_start,report_end=min_date,max_date
filtered=data[data.building.isin(selected_buildings)&(data.date.dt.date>=report_start)&(data.date.dt.date<=report_end)].copy()

st.sidebar.header('4. Alert settings')
threshold = st.sidebar.slider('Alert threshold (% above baseline)',10,100,25,5)
base_default_end = min_date + timedelta(days=max(0,min(2,(max_date-min_date).days-1)))
base_start = st.sidebar.date_input('Baseline start date', value=min_date, min_value=min_date,max_value=max_date,key='base_start')
base_end = st.sidebar.date_input('Baseline end date', value=max(base_start,base_default_end), min_value=min_date,max_value=max_date,key='base_end')
min_rows = st.sidebar.selectbox('Minimum baseline readings per zone', [1,2,3,5], index=0, help='For a stronger baseline, use at least 3–7 daily readings if available.')
if base_end < base_start:
    st.sidebar.error('Baseline end must be on or after baseline start.'); st.stop()

st.markdown('<div class="gl-section">▦ Resource overview</div>', unsafe_allow_html=True)
st.caption('Totals and charts are recalculated from the active dataset and selected filters.')
kpis=st.columns(4)
for k,(name,cfg) in zip(kpis,RESOURCE_CONFIG.items()):
    series=filtered[cfg['column']].dropna()
    k.metric(f'{name} total', f'{series.sum():,.2f} {cfg["unit"]}' if not series.empty else 'No data')
st.caption(f'{len(filtered)} records in selected reporting period • Data statuses: {", ".join(sorted(filtered.data_status.dropna().astype(str).unique())) if not filtered.empty else "none"}')

available_resources=[n for n,cfg in RESOURCE_CONFIG.items() if filtered[cfg['column']].notna().any()]
if available_resources:
    left,right=st.columns([1.15,1])
    with left:
        st.subheader('Daily trend')
        trend_resource=st.selectbox('Choose resource',available_resources)
        tc=RESOURCE_CONFIG[trend_resource]['column']
        trend=filtered.dropna(subset=[tc]).groupby(['date','building'],as_index=False)[tc].sum()
        if not trend.empty:
            fig=px.line(trend,x='date',y=tc,color='building',markers=True,labels={'date':'Date',tc:f'{trend_resource} ({RESOURCE_CONFIG[trend_resource]["unit"]})','building':'Zone'},color_discrete_sequence=['#16835f','#45b978','#e2a93b','#4179a8','#8658a6','#df795e'])
            fig.update_layout(template='plotly_white',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans, sans-serif',color='#38534d'),margin=dict(l=12,r=12,t=24,b=12),legend=dict(orientation='h',yanchor='bottom',y=1.02,xanchor='left',x=0))
            fig.update_xaxes(showgrid=False,zeroline=False)
            fig.update_yaxes(gridcolor='#e7efeb',zeroline=False)
            st.plotly_chart(fig,use_container_width=True)
    with right:
        st.subheader('Zone comparison')
        compare_resource=st.selectbox('Compare resource',available_resources,key='compare_resource')
        cc=RESOURCE_CONFIG[compare_resource]['column']
        comp=filtered.groupby('building',as_index=False)[cc].sum(min_count=1).dropna()
        if not comp.empty:
            fig2=px.bar(comp,x='building',y=cc,labels={'building':'Zone',cc:f'{compare_resource} total ({RESOURCE_CONFIG[compare_resource]["unit"]})'},color=cc,color_continuous_scale=['#c9f0d8','#16835f'])
            fig2.update_layout(template='plotly_white',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans, sans-serif',color='#38534d'),margin=dict(l=12,r=12,t=24,b=12),coloraxis_showscale=False)
            fig2.update_xaxes(showgrid=False,zeroline=False)
            fig2.update_yaxes(gridcolor='#e7efeb',zeroline=False)
            st.plotly_chart(fig2,use_container_width=True)
else:
    st.warning('No numeric resource values found in the selected period. Check your CSV columns and values.')

st.markdown('<div class="gl-section">◷ Baseline comparison</div>', unsafe_allow_html=True)
st.caption('The baseline is the mean of readings between the selected baseline dates. The app checks later dates for threshold breaches.')
base_resources=[n for n,cfg in RESOURCE_CONFIG.items() if data[cfg['column']].notna().any()]
if base_resources:
    chosen=st.selectbox('Resource to inspect',base_resources,key='baseline_resource')
    col=RESOURCE_CONFIG[chosen]['column']
    bpart=data[(data.building.isin(selected_buildings))&(data.date.dt.date>=base_start)&(data.date.dt.date<=base_end)].dropna(subset=[col])
    cpart=filtered[filtered.date.dt.date>base_end].dropna(subset=[col])
    base=bpart.groupby('building')[col].mean().to_dict()
    rows=[]
    for b in sorted(set(base)|set(cpart.building)):
        bv=base.get(b); cv=cpart[cpart.building==b][col].mean() if not cpart[cpart.building==b].empty else None
        rows.append({'Building / zone':b,'Baseline average':round(bv,2) if bv is not None else None,'Later-period average':round(cv,2) if cv is not None and pd.notna(cv) else None,'Change (%)':round((cv-bv)/bv*100,1) if bv is not None and bv>0 and cv is not None and pd.notna(cv) else None,'Baseline rows':int(bpart[bpart.building==b][col].count())})
    st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
    if cpart.empty: st.info('No readings after the baseline end date. Move the baseline end earlier or upload later dates to test alerts.')

st.markdown('<div class="gl-section">⚑ Unusual-consumption alerts</div>', unsafe_allow_html=True)
st.caption('Alerts are investigation prompts—not proof of a fault. Current values are compared with each zone’s baseline average.')
alert_frames=[]
for name,cfg in RESOURCE_CONFIG.items():
    if data[cfg['column']].notna().any():
        a=make_alerts(data[data.building.isin(selected_buildings)],cfg['column'],base_start,base_end,threshold,min_rows)
        if not a.empty:
            a['resource']=name; a['unit']=cfg['unit']; alert_frames.append(a)
if alert_frames:
    alerts=pd.concat(alert_frames,ignore_index=True)
    alerts=alerts[(pd.to_datetime(alerts.date).dt.date>=report_start)&(pd.to_datetime(alerts.date).dt.date<=report_end)]
    if alerts.empty:
        st.success('No readings crossed the selected threshold in the reporting period.')
    else:
        alerts=alerts[['date','building','resource','current_value','unit','baseline_avg','change_pct','severity','data_status','recommended_check']].sort_values(['date','change_pct'],ascending=[False,False])
        st.dataframe(alerts,use_container_width=True,hide_index=True)
        st.download_button('Download alert list CSV',alerts.to_csv(index=False).encode('utf-8'),'greenledger_alerts.csv','text/csv')
else:
    st.info('No alerts can be calculated yet. You need baseline readings and at least one later reading for the same zone, plus a positive baseline value. Check the baseline dates and resource values.')

st.markdown('<div class="gl-section">✓ Action register</div>', unsafe_allow_html=True)
st.caption('Record follow-up after a person verifies the alert. This does not control appliances.')
if ACTIONS_PATH.exists():
    try: actions=pd.read_csv(ACTIONS_PATH)
    except Exception: actions=pd.DataFrame(columns=['date_logged','resource','building','observation','proposed_action','owner','status','notes'])
else:
    actions=pd.DataFrame(columns=['date_logged','resource','building','observation','proposed_action','owner','status','notes'])
if 'actions_editor' not in st.session_state:
    st.session_state['actions_initial']=actions
edited=st.data_editor(st.session_state.get('actions_initial',actions),num_rows='dynamic',use_container_width=True,key='actions_editor')
a1,a2=st.columns(2)
with a1:
    if st.button('Save action register locally'):
        edited.to_csv(ACTIONS_PATH,index=False); st.success('Saved to data/action_register.csv.')
with a2:
    st.download_button('Download action register CSV',edited.to_csv(index=False).encode('utf-8'),'greenledger_action_register.csv','text/csv')

st.markdown('<div class="gl-section">⇩ Export your report</div>', unsafe_allow_html=True)
report=['GREENLEDGER — CAMPUS RESOURCE OPTIMISATION',f'Generated: {date.today().isoformat()}',f'Reporting period: {report_start} to {report_end}',f'Records included: {len(filtered)}',f'Baseline period: {base_start} to {base_end}',f'Alert threshold: {threshold}%',f'Data status labels: {", ".join(sorted(filtered.data_status.dropna().astype(str).unique())) if not filtered.empty else "none"}','', 'RESOURCE TOTALS']
for name,cfg in RESOURCE_CONFIG.items():
    s=filtered[cfg['column']].dropna()
    report.append(f'{name}: {s.sum():.2f} {cfg["unit"]}' if not s.empty else f'{name}: no data supplied')
report += ['', 'DATA QUALITY', 'Data status comes from the uploaded file or user entry and is not independently verified.', 'Alerts are threshold-based prompts and require human verification.', 'No physical appliance shutdown or live meter connection is performed by this laptop prototype.', '', 'ACTION REGISTER', edited.to_csv(index=False)]
st.download_button('Download text report', '\n'.join(report).encode('utf-8'),'greenledger_report.txt','text/plain')
st.download_button('Download current readings CSV', data.to_csv(index=False).encode('utf-8'),'greenledger_current_readings.csv','text/csv')
with st.expander('Troubleshooting: why an alert may not appear'):
    st.markdown('''1. Confirm the same building/zone has readings during the baseline dates **and** on a later date.\n2. Set the baseline end date before the reading you expect to alert on.\n3. Check that the baseline average is greater than zero.\n4. Ensure resource columns contain numeric values and units are consistent.\n5. At a 25% threshold, a baseline of 100 and later reading of 125 should alert.\n6. If your file only has solar data or a different column name, use the CSV format help above.\n7. The app uses uploaded values; it cannot measure real energy by itself without meter data.''')
