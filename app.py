import streamlit as st

st.set_page_config(page_title='Smart Grid Dashboard', layout='wide')

st.title('⚡ Rural Smart Grid Monitoring Dashboard')

st.markdown('### Warangal Distribution Zone')

col1, col2, col3 = st.columns(3)

with col1:
st.metric('Available Power', '28 MW')

with col2:
st.metric('Current Demand', '31 MW', '-3 MW deficit')

with col3:
st.metric('Active Outages', '2 Feeders')

st.success('System running successfully')
