import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Franchise AI", page_icon="📊", layout="wide")

st.title("Agentic AI for Franchise Management System")
st.caption("Basic starter prototype — sample data only")

# Demonstration data. Replace with real franchise data when available.
data = pd.DataFrame({
    "Branch": ["North Branch", "South Branch", "East Branch", "West Branch"],
    "Monthly Revenue (₹)": [185000, 142000, 167000, 119000],
    "Monthly Expenses (₹)": [112000, 98000, 105000, 90000],
    "Target Revenue (₹)": [170000, 160000, 160000, 140000],
})

data["Profit (₹)"] = data["Monthly Revenue (₹)"] - data["Monthly Expenses (₹)"]
data["Status"] = data.apply(
    lambda row: "On target" if row["Monthly Revenue (₹)"] >= row["Target Revenue (₹)"] else "Below target",
    axis=1,
)

st.info("This is a basic demonstration using illustrative sample data. It is not connected to live business systems or an AI model.")

c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue", f"₹{data['Monthly Revenue (₹)'].sum():,.0f}")
c2.metric("Total Expenses", f"₹{data['Monthly Expenses (₹)'].sum():,.0f}")
c3.metric("Total Profit", f"₹{data['Profit (₹)'].sum():,.0f}")

st.subheader("Branch performance")
st.dataframe(data, use_container_width=True, hide_index=True)

chart = px.bar(
    data,
    x="Branch",
    y=["Monthly Revenue (₹)", "Target Revenue (₹)"],
    barmode="group",
    title="Revenue compared with target",
)
st.plotly_chart(chart, use_container_width=True)

st.subheader("Basic performance observations")
for _, row in data.iterrows():
    if row["Status"] == "Below target":
        st.warning(
            f"{row['Branch']} is below its revenue target by "
            f"₹{row['Target Revenue (₹)'] - row['Monthly Revenue (₹)']:,.0f}. "
            "Suggested next step: review sales trends and operating costs."
        )
    else:
        st.success(f"{row['Branch']} has met or exceeded its revenue target.")

st.caption("Starter version: performance checks use simple rules, not an autonomous agent or predictive AI.")
