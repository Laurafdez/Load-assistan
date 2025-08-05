import streamlit as st
import requests
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="📊 Load Assistant Dashboard", layout="wide")
st.title("📊 Load Assistant - Operational Metrics")


try:
    response = requests.get("http://api:8000/api/v1/metrics")
    response.raise_for_status()
    data = response.json()

    st.markdown("### 🔢 General Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Total Loads", data["total_loads"])
    col2.metric("📞 Total Calls", data["total_calls"])
    col3.metric("💵 Avg Price", f"${data['avg_agreed_price']:.2f}")
    col4.metric("⏱️ Avg Duration", f"{data['avg_call_duration_sec']:.0f}s")

    st.markdown("---")
    st.markdown("### ✅ Call Outcomes")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("✔️ Accepted", data["accepted"])
    col6.metric("❌ Rejected", data["rejected"])
    col7.metric("🧩 Failed Negotiation", data["failed_negotiation"])
    col8.metric("⏳ No Response", data["no_response"])

    col9, col10 = st.columns(2)
    col9.metric("🔁 Follow-Up", data["interested_follow_up"])
    col10.metric("📊 Avg Attempts", f"{data['avg_attempts']:.1f}")

    st.markdown("---")
    st.markdown("### 😊 Sentiment Distribution")

    sentiment = data["sentiment_summary"]
    sentiment_df = pd.DataFrame.from_dict(
        sentiment, orient="index", columns=["Count"]
    ).reset_index()
    sentiment_df.columns = ["Sentiment", "Count"]

    fig_sentiment = px.bar(
        sentiment_df,
        x="Sentiment",
        y="Count",
        color="Sentiment",
        title="Sentiment Distribution",
        text="Count",
        color_discrete_map={"positive": "green", "neutral": "gray", "negative": "red"},
    )
    fig_sentiment.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_sentiment, use_container_width=True)

    st.markdown("### 👍 Satisfaction Overview")
    satisfaction = data["satisfaction_summary"]
    sat_df = pd.DataFrame.from_dict(
        satisfaction, orient="index", columns=["Count"]
    ).reset_index()
    sat_df.columns = ["Satisfaction", "Count"]

    fig_satisfaction = px.pie(
        sat_df,
        values="Count",
        names="Satisfaction",
        title="Carrier Satisfaction",
        color="Satisfaction",
        color_discrete_map={
            "satisfied": "green",
            "unsatisfied": "red",
            "unknown": "lightgray",
        },
    )
    fig_satisfaction.update_traces(textinfo="label+percent")
    st.plotly_chart(fig_satisfaction, use_container_width=True)

except Exception as e:
    st.error(f"🚨 Failed to load metrics from API: {e}")
