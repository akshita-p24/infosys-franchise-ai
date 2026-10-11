"""Home Dashboard – KPIs, revenue trend, outlet comparison."""
import os
import pandas as pd, plotly.express as px, plotly.graph_objects as go
import streamlit as st
import data_gen, ui

D = data_gen.DATA_DIR

@st.cache_data
def load(name):
    data_gen.generate()
    df = pd.read_csv(os.path.join(D, f"{name}.csv"))
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    return df

def _style(fig, h=360):
    fig.update_layout(template="plotly_dark", height=h, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=30, b=10),
                      legend=dict(orientation="h", y=1.1))
    return fig

def _pct(cur, prev):
    return None if prev == 0 else (cur - prev) / prev * 100

def render(sess):
    outlets, sales, fb = load("outlets"), load("sales"), load("feedback")
    aud = load("audits")

    # outlet managers / staff see their own outlet if it matches, else all
    scope_ids = outlets.outlet_id.tolist()
    if sess["role"] in ("outlet_manager", "staff") and sess.get("outlet"):
        m = outlets[outlets.outlet_name.str.contains(sess["outlet"], case=False)
                    | outlets.city.str.contains(sess["outlet"], case=False)]
        if not m.empty:
            scope_ids = m.outlet_id.tolist()

    c1, c2 = st.columns([2, 1])
    names = outlets[outlets.outlet_id.isin(scope_ids)].set_index("outlet_id").outlet_name
    pick = c1.multiselect("Outlets", names.tolist(), default=names.tolist())
    days = c2.selectbox("Period", [7, 30, 60, 90], index=1, format_func=lambda x: f"Last {x} days")
    ids = [i for i, n in names.items() if n in pick] or scope_ids

    s = sales[sales.outlet_id.isin(ids)]
    end = s.date.max()
    cur = s[s.date > end - pd.Timedelta(days=days)]
    prev = s[(s.date <= end - pd.Timedelta(days=days)) & (s.date > end - pd.Timedelta(days=2 * days))]
    f = fb[fb.outlet_id.isin(ids)]
    fcur = f[f.date > end - pd.Timedelta(days=days)]

    k = st.columns(4)
    with k[0]: ui.kpi("Revenue", f"₹{cur.revenue.sum()/1e5:,.1f} L", _pct(cur.revenue.sum(), prev.revenue.sum()))
    with k[1]: ui.kpi("Orders", f"{cur.orders.sum():,}", _pct(cur.orders.sum(), prev.orders.sum()))
    with k[2]:
        aov = cur.revenue.sum() / max(cur.orders.sum(), 1)
        paov = prev.revenue.sum() / max(prev.orders.sum(), 1)
        ui.kpi("Avg order value", f"₹{aov:,.0f}", _pct(aov, paov))
    with k[3]:
        r = fcur.rating.mean() if len(fcur) else f.rating.mean()
        ui.kpi("Avg customer rating", f"{r:.2f} / 5", None)

    ui.section("Revenue trend")
    daily = cur.groupby("date", as_index=False).revenue.sum()
    daily["7-day avg"] = daily.revenue.rolling(7, min_periods=1).mean()
    fig = go.Figure()
    fig.add_bar(x=daily.date, y=daily.revenue, name="Daily revenue", marker_color="#3B4375")
    fig.add_scatter(x=daily.date, y=daily["7-day avg"], name="7-day avg",
                    line=dict(color="#20C6B6", width=3))
    st.plotly_chart(_style(fig), use_container_width=True)

    left, right = st.columns(2)
    with left:
        ui.section("Revenue by outlet")
        byo = (cur.groupby("outlet_id", as_index=False).revenue.sum()
               .merge(outlets[["outlet_id", "city"]], on="outlet_id").sort_values("revenue"))
        fig = px.bar(byo, x="revenue", y="city", orientation="h",
                     color="revenue", color_continuous_scale=["#3B4375", "#7C6CFF", "#20C6B6"])
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(_style(fig, 380), use_container_width=True)
    with right:
        ui.section("Cost & quality snapshot")
        snap = (cur.groupby("outlet_id", as_index=False)[["food_cost_pct", "wastage_pct"]].mean()
                .merge(outlets[["outlet_id", "city"]], on="outlet_id")
                .merge(aud.sort_values("date").groupby("outlet_id", as_index=False).last()
                       [["outlet_id", "compliance_score"]], on="outlet_id"))
        fig = px.scatter(snap, x="food_cost_pct", y="compliance_score", size="wastage_pct",
                         text="city", color="wastage_pct",
                         color_continuous_scale=["#20C6B6", "#FFC857", "#FF6B81"],
                         labels={"food_cost_pct": "Food cost %", "compliance_score": "Compliance score"})
        fig.update_traces(textposition="top center")
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(_style(fig, 380), use_container_width=True)
        st.caption("Bubble size = wastage %. Top-left (low cost, high compliance) is best.")

    ui.section("Outlet leaderboard")
    lb = (cur.groupby("outlet_id").agg(Revenue=("revenue", "sum"), Orders=("orders", "sum"))
          .reset_index().merge(outlets[["outlet_id", "city"]], on="outlet_id")
          .merge(f.groupby("outlet_id", as_index=False).rating.mean(), on="outlet_id")
          .sort_values("Revenue", ascending=False))
    lb["Revenue"] = lb.Revenue.round(0)
    lb["rating"] = lb.rating.round(2)
    st.dataframe(lb.rename(columns={"outlet_id": "ID", "city": "City", "rating": "Rating"}),
                 use_container_width=True, hide_index=True,
                 column_config={"Revenue": st.column_config.NumberColumn(format="₹%d")})