import streamlit as st
import pandas as pd
import plotly.express as px
import os
os.makedirs("outputs", exist_ok=True)

st.set_page_config(page_title="Climate Trend Analyzer", layout="wide")

# ======================
# HEADER
# ======================
st.title("🌍 Climate Trend Analyzer Dashboard")
st.markdown("### Real-world climate insights using data science 📊")

# ======================
# LOAD DATA
# ======================
df = pd.read_csv("data/climate.csv")

# Rename columns
df = df.rename(columns={
    "Date Time": "Date",
    "T (degC)": "Temperature",
    "rh (%)": "Humidity",
    "p (mbar)": "Pressure"
})

# Convert date
df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y %H:%M:%S")

df = df.sort_values("Date")
df = df.fillna(method="ffill")

# ======================
# SIDEBAR FILTERS
# ======================
st.sidebar.header("🔎 Filters")

start_date = st.sidebar.date_input("Start Date", df["Date"].min().date())
end_date = st.sidebar.date_input("End Date", df["Date"].max().date())

df = df[(df["Date"].dt.date >= start_date) & (df["Date"].dt.date <= end_date)]

# ======================
# KPI METRICS (IMPORTANT UPGRADE)
# ======================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("🌡 Avg Temperature", f"{df['Temperature'].mean():.2f} °C")
col2.metric("💧 Avg Humidity", f"{df['Humidity'].mean():.2f} %")
col3.metric("📉 Pressure", f"{df['Pressure'].mean():.2f} mbar")

# ======================
# TEMPERATURE TREND
# ======================
st.subheader("📈 Temperature Trend Over Time")

fig1 = px.line(
    df,
    x="Date",
    y="Temperature",
    title="Temperature Variation",
    template="plotly_dark"
)

st.plotly_chart(fig1, use_container_width=True)

# ======================
# HUMIDITY TREND
# ======================
st.subheader("💧 Humidity Trend")

fig2 = px.line(
    df,
    x="Date",
    y="Humidity",
    title="Humidity Variation",
    color_discrete_sequence=["blue"],
    template="plotly_dark"
)

st.plotly_chart(fig2, use_container_width=True)

# ======================
# SCATTER: TEMP vs HUMIDITY
# ======================
st.subheader("🌡️ Temperature vs Humidity Relationship")

fig3 = px.scatter(
    df,
    x="Temperature",
    y="Humidity",
    color="Temperature",
    title="Correlation Insight",
    template="plotly_dark"
)

st.plotly_chart(fig3, use_container_width=True)

# ======================
# ANOMALY DETECTION
# ======================
st.subheader("⚠️ Climate Anomalies")

mean = df["Temperature"].mean()
std = df["Temperature"].std()

df["Anomaly"] = df["Temperature"] > (mean + 2 * std)

st.dataframe(df[df["Anomaly"] == True])

# ======================
# DOWNLOAD BUTTON (PRO FEATURE)
# ======================
st.subheader("⬇️ Download Data")

csv = df.to_csv(index=False)
st.download_button("Download Filtered Data", csv, "climate_data.csv", "text/csv")

# ======================
# FOOTER
# ======================
st.success("Dashboard Loaded Successfully 🚀")
# Save cleaned data
df.to_csv("outputs/cleaned_data.csv", index=False)

# Save anomalies
df[df["Anomaly"] == True].to_csv("outputs/anomalies.csv", index=False)

# Save forecast
forecast_df.to_csv("outputs/forecast.csv", index=False)