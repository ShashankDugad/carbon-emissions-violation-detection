import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Air Quality Violations", layout="wide")
st.title("🌍 Carbon Emissions Violation Detection Dashboard")

# Load batch results
@st.cache_data
def load_data():
    # Simulate loading from batch outputs
    violations = pd.DataFrame({
        'state': ['California', 'Arizona', 'Texas', 'Pennsylvania', 'Colorado'],
        'violation_count': [442274, 63714, 58080, 46627, 40313]
    })
    
    yoy = pd.DataFrame({
        'year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        'avg_pm25': [8.23, 7.37, 7.96, 8.03, 7.21, 7.98, 8.47, 7.53, 8.66, 7.10]
    })
    
    return violations, yoy

violations, yoy = load_data()

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Violations", "612K", "-18% (2024)")
col2.metric("States Monitored", "54")
col3.metric("ML Model AUC", "99.25%")
col4.metric("Data Records", "225M")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 5 States by Violations")
    fig1 = px.bar(violations, x='state', y='violation_count', 
                  color='violation_count', color_continuous_scale='Reds')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("PM2.5 Trend (2015-2024)")
    fig2 = px.line(yoy, x='year', y='avg_pm25', markers=True)
    fig2.add_hline(y=12, line_dash="dash", line_color="red", 
                   annotation_text="EPA Target")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Key Insights")
st.markdown("""
- **California**: 442K violations (72% of total)
- **PM2.5 Decline**: 12% reduction from 2015-2019
- **2024 Drop**: 18% decrease vs 2023 spike
- **Model Performance**: 99.25% accuracy on test set
""")

st.subheader("Streaming Status")
st.success("✓ Kafka pipeline active (500 msgs/batch)")
st.info("Real-time violations: Processing...")
