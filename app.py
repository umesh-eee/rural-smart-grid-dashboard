import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title='Smart Grid Dashboard', layout='wide')

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title('⚡ Rural Smart Grid Monitoring Dashboard')
st.markdown('### Warangal Distribution Zone')
# -------------------------------------------------
# SCADA Integration Status
# -------------------------------------------------
st.markdown('---')
st.subheader('🏭 Industrial SCADA Integration')
# -------------------------------------------------
# Substation selector
# -------------------------------------------------
substation = st.selectbox(
    'Select Substation',
    ['Warangal 132/33kV', 'Hanamkonda 132/33kV', 'Kazipet 132/33kV']
)

st.info(f'Active SCADA Station: {substation}')
# -------------------------------------------------
# Simulated feeder telemetry
# -------------------------------------------------
st.subheader('📡 Feeder Telemetry')

telemetry = pd.DataFrame({
    'Feeder': ['FDR-01', 'FDR-02', 'FDR-03', 'FDR-04'],
    'Voltage_kV': [11.2, 10.7, 11.0, 10.5],
    'Current_A': [120, 185, 96, 210],
    'Power_MW': [2.1, 3.4, 1.5, 3.8],
    'Breaker': ['CLOSED', 'OPEN', 'CLOSED', 'CLOSED'],
    'Timestamp': [datetime.now().strftime('%H:%M:%S')]*4
})

st.dataframe(telemetry, use_container_width=True)
# -------------------------------------------------
# Alarm management
# -------------------------------------------------
st.subheader('🚨 Active Alarms')

alarms = pd.DataFrame({
    'Priority': ['HIGH', 'MEDIUM'],
    'Message': [
        'FDR-04 current exceeded threshold',
        'Town Y voltage below 0.95 pu'
    ],
    'Time': [datetime.now().strftime('%H:%M:%S')]*2
})

st.dataframe(alarms, use_container_width=True)

st.error('1 HIGH priority alarm requires operator acknowledgement')
# -------------------------------------------------
# Utility Data Gateway
# -------------------------------------------------
st.markdown('---')
st.subheader('🔌 Utility Data Gateway')

st.code('''
Future integration sources:
- SCADA OPC-UA Server
- Modbus TCP RTU
- IEC 60870-5-104 Gateway
- MQTT Smart Meter Broker
- Utility REST API
- Historian Database (SQL)
''')

st.caption('Current version uses simulated telemetry; architecture is ready for real utility data integration.')

sc1, sc2, sc3 = st.columns(3)

sc1.metric('SCADA Server', 'CONNECTED')
sc2.metric('RTU Heartbeat', 'OK')
sc3.metric('Last Telemetry', datetime.now().strftime('%H:%M:%S'))

st.success('SCADA communication channel healthy (simulated telemetry)')

# -------------------------------------------------
# Data
# -------------------------------------------------
data = {
    'Area': ['Village A', 'Village B', 'Village C', 'Town X', 'Town Y', 'City Z'],
    'Available_MW': [2.5, 1.2, 3.0, 5.0, 4.5, 20.0],
    'Demand_MW': [2.0, 1.8, 2.5, 4.7, 5.2, 22.0],
    'Status': ['ON', 'OFF', 'ON', 'ON', 'ALERT', 'ALERT'],
    'Voltage': [232, 218, 229, 235, 221, 227],
    'PF': [0.95, 0.88, 0.94, 0.96, 0.90, 0.92],
    'Lat': [17.90, 17.85, 17.92, 18.00, 18.05, 17.97],
    'Lon': [79.60, 79.55, 79.68, 79.72, 79.80, 79.65]
}

df = pd.DataFrame(data)

available = df['Available_MW'].sum()
demand = df['Demand_MW'].sum()
deficit = available - demand
outages = (df['Status'] == 'OFF').sum()

# -------------------------------------------------
# KPI cards
# -------------------------------------------------
c1, c2, c3 = st.columns(3)

c1.metric('Available Power', f'{available:.1f} MW')
c2.metric('Current Demand', f'{demand:.1f} MW', f'{deficit:.1f} MW')
c3.metric('Active Outages', outages)

if deficit < 0:
    st.error(f'⚠ Power deficit of {abs(deficit):.1f} MW detected')
else:
    st.success('Power supply is sufficient')

# -------------------------------------------------
# Area selector
# -------------------------------------------------
st.subheader('Select Area')

selected_area = st.selectbox('Area', df['Area'])

area_data = df[df['Area'] == selected_area].iloc[0]

a1, a2, a3, a4 = st.columns(4)

a1.metric('Available', f"{area_data['Available_MW']} MW")
a2.metric('Demand', f"{area_data['Demand_MW']} MW")
a3.metric('Voltage', f"{area_data['Voltage']} V")
a4.metric('Power Factor', f"{area_data['PF']:.2f}")

status = area_data['Status']

if status == 'ON':
    st.success(f'🟢 {selected_area} feeder is ON')
elif status == 'OFF':
    st.error(f'🔴 {selected_area} feeder is OFF')
else:
    st.warning(f'🟡 {selected_area} feeder is under ALERT')

# -------------------------------------------------
# Status table
# -------------------------------------------------
st.subheader('📋 Area Status')

display_df = df[['Area', 'Available_MW', 'Demand_MW', 'Status']]
st.dataframe(display_df, use_container_width=True)

# -------------------------------------------------
# Demand chart
# -------------------------------------------------
st.subheader('📊 Load Demand by Area')

fig = px.bar(
    df,
    x='Area',
    y='Demand_MW',
    color='Status',
    text='Demand_MW',
    title='Area-wise Load Demand'
)

fig.update_traces(textposition='outside')
st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Trend chart
# -------------------------------------------------
st.subheader('📈 24-Hour Load Trend')

hours = list(range(24))
trend = [1.2,1.1,1.0,1.0,1.1,1.3,1.8,2.2,2.8,3.5,4.2,4.8,
         5.0,4.9,4.7,4.4,4.2,4.5,5.1,5.4,5.0,4.0,3.0,2.0]

trend_df = pd.DataFrame({'Hour': hours, 'Load_MW': trend})

fig2 = px.line(
    trend_df,
    x='Hour',
    y='Load_MW',
    markers=True,
    title='24-Hour Demand Trend'
)

st.plotly_chart(fig2, use_container_width=True)
# =================================================
# AI LOAD FORECASTING MODULE
# =================================================

st.markdown('---')
st.header('🤖 AI Load Forecasting')

# Historical load data (last 24 hours)
historical_load = trend_df['Load_MW'].tolist()

# Simple AI-style forecasting using recent trend
recent_changes = []
for i in range(len(historical_load)-5, len(historical_load)-1):
    recent_changes.append(historical_load[i+1] - historical_load[i])

avg_change = sum(recent_changes) / len(recent_changes)

next_hour_load = historical_load[-1] + avg_change

# Peak hour detection
peak_value = max(historical_load)
peak_hour = historical_load.index(peak_value)

# Display metrics
f1, f2, f3 = st.columns(3)

f1.metric('Current Load', f'{historical_load[-1]:.1f} MW')
f2.metric('Predicted Next Hour', f'{next_hour_load:.1f} MW',
          f'{next_hour_load-historical_load[-1]:.1f} MW')
f3.metric('Peak Hour', f'{peak_hour}:00')

# Alert
if next_hour_load > available:
    st.warning('⚠ Predicted demand may exceed available power.')
else:
    st.success('Predicted demand is within safe operating limit.')

# Forecast chart
forecast_hours = list(range(24)) + [24]
forecast_values = historical_load + [next_hour_load]

forecast_df = pd.DataFrame({
    'Hour': forecast_hours,
    'Load_MW': forecast_values,
    'Type': ['Historical']*24 + ['Forecast']
})

fig_forecast = px.line(
    forecast_df,
    x='Hour',
    y='Load_MW',
    color='Type',
    markers=True,
    title='AI-Based Load Forecast'
)

fig_forecast.update_layout(
    xaxis_title='Hour',
    yaxis_title='Load (MW)'
)

st.plotly_chart(fig_forecast, use_container_width=True)

# Operator recommendation
reserve_margin = available - next_hour_load

st.subheader('🧠 Forecast Recommendation')

if reserve_margin < 2:
    st.error(f'Reserve margin low: {reserve_margin:.1f} MW. Keep standby feeder ready.')
else:
    st.info(f'Reserve margin available: {reserve_margin:.1f} MW.')

st.caption('Forecast generated from recent load trend (educational AI-style model).')

# -------------------------------------------------
# Map
# -------------------------------------------------
st.subheader('🗺️ Outage Monitoring Map')

map_fig = go.Figure()

colors = {'ON':'green','OFF':'red','ALERT':'orange'}

for _, row in df.iterrows():
    map_fig.add_trace(go.Scattermap(
        lat=[row['Lat']],
        lon=[row['Lon']],
        mode='markers+text',
        marker=dict(size=14, color=colors[row['Status']]),
        text=[row['Area']],
        textposition='top center',
        name=row['Area']
    ))

map_fig.update_layout(
    map=dict(
        style='open-street-map',
        center=dict(lat=17.95, lon=79.68),
        zoom=8
    ),
    height=500,
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(map_fig, use_container_width=True)

# -------------------------------------------------
# Analytics
# -------------------------------------------------
st.markdown('---')
st.header('🧠 Smart Grid Analytics Engine')

df['Load_Percent'] = (df['Demand_MW'] / df['Available_MW']) * 100

overloaded = df[df['Load_Percent'] > 100]

st.subheader('⚠ Overload Detection')

if len(overloaded) > 0:
    st.error('Overloaded Areas Detected')
    st.dataframe(
        overloaded[['Area','Available_MW','Demand_MW','Load_Percent']],
        use_container_width=True
    )
else:
    st.success('No overloaded areas detected')

# Prediction
st.subheader('🔮 Next Hour Demand Prediction')

predicted = demand * 1.05

st.metric(
    'Predicted Demand',
    f'{predicted:.1f} MW',
    f'+{predicted-demand:.1f} MW'
)

# Priority ranking
st.subheader('🏥 Feeder Priority Ranking')

priority_df = pd.DataFrame({
    'Feeder':['Hospital','Water Supply','Emergency','School','Residential'],
    'Priority':[1,2,3,4,5]
})

st.dataframe(priority_df, use_container_width=True)

# Load shedding
st.subheader('💡 Load Shedding Recommendation')

reduction = max(0, predicted - available)

if reduction > 0:
    st.warning(f'Required reduction: {reduction:.1f} MW')
    st.markdown('**Suggested sequence:**')
    st.markdown('1. Residential')
    st.markdown('2. School')
    st.markdown('3. Commercial')
    st.markdown('4. Keep Hospital and Water Supply ON')
else:
    st.success('No load shedding required')

# Advisory
st.subheader('📢 Operator Advisory')

msg = f'''
Current demand: {demand:.1f} MW
Predicted demand: {predicted:.1f} MW
Available power: {available:.1f} MW
'''

st.code(msg)

# Download button
csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    '📥 Download Area Report',
    csv,
    file_name='smart_grid_report.csv',
    mime='text/csv'
)

st.info('Smart Grid Monitoring Platform | Developed by Umesh')
