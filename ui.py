"""Shared look & feel: CSS, hero banner, KPI cards."""
import streamlit as st

CSS = """
<style>
#MainMenu, footer {visibility: hidden;}
.block-container {padding-top: 2rem; max-width: 1200px;}
.hero {
  background: linear-gradient(135deg, #5B4BFF 0%, #7C6CFF 45%, #20C6B6 100%);
  border-radius: 20px; padding: 2rem 2.2rem; margin-bottom: 1.2rem;
  box-shadow: 0 10px 30px rgba(92,75,255,.25);
}
.hero h1 {margin: 0; font-size: 2.1rem; color: #fff; letter-spacing: -.5px;}
.hero p {margin: .4rem 0 0; color: rgba(255,255,255,.9); font-size: 1.02rem;}
.chips {margin-top: .9rem;}
.chip {display:inline-block; background: rgba(255,255,255,.18); color:#fff;
  padding: .25rem .7rem; border-radius: 999px; font-size: .78rem; margin: 0 .35rem .35rem 0;}
.kpi {background: #131A33; border: 1px solid #222B50; border-radius: 16px;
  padding: 1rem 1.2rem; height: 100%;}
.kpi .label {color:#9AA6CF; font-size:.78rem; text-transform:uppercase; letter-spacing:.8px;}
.kpi .value {font-size:1.75rem; font-weight:700; color:#fff; margin:.15rem 0;}
.kpi .delta-up {color:#2ED3A0; font-size:.85rem;}
.kpi .delta-down {color:#FF6B81; font-size:.85rem;}
.kpi .delta-flat {color:#9AA6CF; font-size:.85rem;}
.section-title {font-size:1.15rem; font-weight:600; margin: 1.2rem 0 .4rem;}
.badge {display:inline-block; padding:.15rem .6rem; border-radius:999px;
  font-size:.75rem; font-weight:600; background:#222B50; color:#C9D2F5;}
div[data-testid="stForm"] {border-radius: 16px; border: 1px solid #222B50; background:#131A33;}
.stTabs [data-baseweb="tab"] {font-weight: 600;}
.stButton > button, .stFormSubmitButton > button {border-radius: 10px; font-weight: 600;}
section[data-testid="stSidebar"] {border-right: 1px solid #222B50;}
</style>
"""

def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)

def hero(title, subtitle, chips=()):
    chips_html = "".join(f'<span class="chip">{c}</span>' for c in chips)
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p>'
        f'<div class="chips">{chips_html}</div></div>', unsafe_allow_html=True)

def kpi(label, value, delta=None):
    cls, txt = "delta-flat", ""
    if delta is not None:
        cls = "delta-up" if delta > 0 else "delta-down" if delta < 0 else "delta-flat"
        arrow = "▲" if delta > 0 else "▼" if delta < 0 else "•"
        txt = f'<div class="{cls}">{arrow} {abs(delta):.1f}% vs previous period</div>'
    st.markdown(f'<div class="kpi"><div class="label">{label}</div>'
                f'<div class="value">{value}</div>{txt}</div>', unsafe_allow_html=True)

def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)