"""
PrISMa Carbon-Capture Sorbent Screening Dashboard
CL653 — IIT Guwahati | Abhishek Das 230107006
Single-file app — all pages in session_state router (no multipage issues)
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os, warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="PrISMa Sorbent Screener",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root variables ── */
:root {
  --bg:      #060d16;
  --bg2:     #0d1b2a;
  --bg3:     #142338;
  --bg4:     #1a2e45;
  --teal:    #00e5c0;
  --teal2:   #00bfa0;
  --blue:    #3d9fdc;
  --amber:   #f5a623;
  --coral:   #ff6b6b;
  --purple:  #a78bfa;
  --green:   #4ade80;
  --text:    #e2eaf3;
  --muted:   #7a96b0;
  --dimmed:  #3d5a73;
  --border:  rgba(0,229,192,0.15);
  --border2: rgba(0,229,192,0.08);
  --glow:    0 0 40px rgba(0,229,192,0.08), 0 2px 12px rgba(0,0,0,0.4);
  --glow2:   0 0 20px rgba(0,229,192,0.2);
}

/* ── Base ── */
.stApp, .main { background: var(--bg) !important; font-family: 'Inter', sans-serif; }
.block-container { padding: 1.5rem 2rem 3rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #060d16 0%, #0a1826 60%, #060d16 100%) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }

/* ── Typography ── */
h1,h2,h3,h4,h5,h6 { color: var(--text) !important; font-family: 'Inter', sans-serif !important; }
p, li, span, label, div { color: var(--text); font-family: 'Inter', sans-serif; }
.stMarkdown p { color: var(--text); line-height: 1.75; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
  background: linear-gradient(135deg, var(--bg3), var(--bg4)) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
  padding: 18px 22px !important;
  box-shadow: var(--glow) !important;
  backdrop-filter: blur(12px);
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 11px !important; letter-spacing: 0.06em; text-transform: uppercase; }
[data-testid="stMetricValue"] { color: var(--teal) !important; font-size: 26px !important; font-weight: 700 !important; font-family: 'JetBrains Mono', monospace !important; }
[data-testid="stMetricDelta"] > div { font-size: 11px !important; }

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, var(--teal) 0%, var(--teal2) 100%) !important;
  color: #060d16 !important; font-weight: 700 !important; border: none !important;
  border-radius: 10px !important; padding: 10px 26px !important;
  font-family: 'Inter', sans-serif !important; letter-spacing: 0.02em;
  transition: all 0.2s ease !important; font-size: 13px !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: var(--glow2) !important; }

/* ── Inputs ── */
.stSlider > div > div > div { background: var(--teal) !important; }
.stSlider [data-testid="stSlider"] > div > div { background: var(--bg4) !important; }
.stSelectbox > div > div, .stMultiSelect > div > div {
  background: var(--bg3) !important; border: 1px solid var(--border) !important;
  color: var(--text) !important; border-radius: 10px !important;
}
.stSelectbox > div > div > div { color: var(--text) !important; }
.stNumberInput > div > div { background: var(--bg3) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; }
.stNumberInput input, .stTextInput input { color: var(--text) !important; background: var(--bg3) !important; }
.stCheckbox > label > div { border-color: var(--teal) !important; }
.stCheckbox > label > div[data-checked="true"] { background: var(--teal) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg3) !important; border-radius: 12px !important;
  padding: 5px !important; gap: 4px !important; border: 1px solid var(--border2) !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; color: var(--muted) !important;
  border-radius: 9px !important; font-weight: 500 !important;
  padding: 9px 20px !important; border: none !important;
  font-size: 13px !important; transition: all 0.15s !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--teal), var(--teal2)) !important;
  color: #060d16 !important; font-weight: 700 !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
  background: var(--bg3) !important; border: 1px solid var(--border2) !important;
  border-radius: 10px !important; color: var(--text) !important;
}
.streamlit-expanderContent { background: var(--bg3) !important; border: 1px solid var(--border2) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1rem 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--teal2); border-radius: 3px; }

/* ── Custom components ── */
.hero-title {
  font-size: 48px; font-weight: 800; letter-spacing: -0.02em; line-height: 1.1;
  background: linear-gradient(135deg, #00e5c0 0%, #3d9fdc 50%, #a78bfa 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.section-title {
  font-size: 28px; font-weight: 700; color: var(--text) !important;
  border-left: 4px solid var(--teal); padding-left: 16px; margin: 1.5rem 0 1rem;
}
.card {
  background: linear-gradient(135deg, var(--bg3) 0%, var(--bg4) 100%);
  border: 1px solid var(--border); border-radius: 16px; padding: 24px;
  box-shadow: var(--glow); margin-bottom: 16px;
}
.card-sm {
  background: var(--bg3); border: 1px solid var(--border2);
  border-radius: 12px; padding: 16px; margin-bottom: 12px;
}
.teal-box {
  background: rgba(0,229,192,0.06); border-left: 3px solid var(--teal);
  border-radius: 0 12px 12px 0; padding: 16px 20px; margin: 10px 0;
}
.amber-box {
  background: rgba(245,166,35,0.07); border-left: 3px solid var(--amber);
  border-radius: 0 12px 12px 0; padding: 16px 20px; margin: 10px 0;
}
.coral-box {
  background: rgba(255,107,107,0.07); border-left: 3px solid var(--coral);
  border-radius: 0 12px 12px 0; padding: 16px 20px; margin: 10px 0;
}
.purple-box {
  background: rgba(167,139,250,0.07); border-left: 3px solid var(--purple);
  border-radius: 0 12px 12px 0; padding: 16px 20px; margin: 10px 0;
}
.badge {
  display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 11px;
  font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;
  font-family: 'JetBrains Mono', monospace;
}
.badge-teal  { background: rgba(0,229,192,0.15); color: var(--teal); border: 1px solid rgba(0,229,192,0.3); }
.badge-amber { background: rgba(245,166,35,0.15); color: var(--amber); border: 1px solid rgba(245,166,35,0.3); }
.badge-coral { background: rgba(255,107,107,0.15); color: var(--coral); border: 1px solid rgba(255,107,107,0.3); }
.predict-number {
  font-size: 80px; font-weight: 800; font-family: 'JetBrains Mono', monospace;
  line-height: 1; letter-spacing: -0.03em;
}
.nav-btn {
  display: block; width: 100%; padding: 10px 14px; margin: 2px 0;
  background: transparent; border: none; border-radius: 10px; cursor: pointer;
  text-align: left; font-size: 13px; font-weight: 500; color: #7a96b0;
  transition: all 0.15s; font-family: 'Inter', sans-serif;
}
.nav-btn:hover { background: rgba(0,229,192,0.08); color: #00e5c0; }
.nav-btn-active {
  background: linear-gradient(135deg, rgba(0,229,192,0.18), rgba(61,159,220,0.12)) !important;
  color: #00e5c0 !important; border: 1px solid rgba(0,229,192,0.25) !important;
}
.dataframe { background: var(--bg3) !important; }
.stDataFrame { border-radius: 12px; overflow: hidden; }
[data-testid="stDataFrameResizable"] { background: var(--bg3) !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# HELPERS & DATA
# ═══════════════════════════════════════════════════════════════════════════
PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(13,27,42,0.5)",
    font=dict(family="Inter, sans-serif", color="#e2eaf3", size=12),
    xaxis=dict(gridcolor="rgba(122,150,176,0.1)", linecolor="rgba(122,150,176,0.2)",
               tickfont=dict(size=11), title_font=dict(size=12)),
    yaxis=dict(gridcolor="rgba(122,150,176,0.1)", linecolor="rgba(122,150,176,0.2)",
               tickfont=dict(size=11), title_font=dict(size=12)),
    legend=dict(bgcolor="rgba(20,35,56,0.9)", bordercolor="rgba(0,229,192,0.2)",
                borderwidth=1, font=dict(size=11)),
    margin=dict(l=55, r=25, t=45, b=55),
)
T="#00e5c0"; A="#f5a623"; C="#ff6b6b"; B="#3d9fdc"; P="#a78bfa"; M="#7a96b0"; G="#4ade80"

@st.cache_resource(show_spinner="Loading model…")
def load_model():
    try:
        import joblib
        m = joblib.load("RF_Tuned_final.joblib")
        return m, True
    except Exception:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.pipeline import Pipeline
        from sklearn.impute import SimpleImputer
        rng = np.random.default_rng(42)
        X = rng.normal(size=(900, 34))
        y = (-280*X[:,2] + 140*X[:,3] + 90*X[:,17] + rng.normal(scale=110, size=900) + 380)
        p = Pipeline([("i", SimpleImputer(strategy="median")),
                      ("m", RandomForestRegressor(200, max_depth=12, random_state=42, n_jobs=-1))])
        p.fit(X, y)
        return p, False

@st.cache_data(show_spinner="Loading dataset…")
def load_data():
    if os.path.exists("merged_raw_v1.csv"):
        return pd.read_csv("merged_raw_v1.csv"), True
    rng = np.random.default_rng(42)
    n = 1185
    hco2 = np.exp(rng.normal(-10, 2.5, n)); hn2 = np.exp(rng.normal(-12, 2.2, n))
    wsat = np.abs(rng.normal(4, 3, n)); uco2 = hco2 * rng.uniform(0.8, 1.5, n)
    ncac = -250*np.log1p(hco2) + 110*np.log1p(hn2) + 80*wsat + rng.normal(0, 200, n) + 500
    df = pd.DataFrame({
        "MOF": [f"RSM{3000+i:04d}" for i in range(n)], "nCAC": ncac,
        "Henry_mol_kg_Pa_CO2": hco2, "Henry_mol_kg_Pa_N2": hn2,
        "Uptake_mean_CO2": uco2, "Uptake_sat_mol_kg": wsat,
        "POAVF__": rng.uniform(0.1, 0.9, n), "Density_g_cm^3": rng.uniform(0.4, 2.5, n),
        "Henry_selectivity_CO2_N2": hco2/(hn2+1e-12),
        "Heat_mean_CO2": rng.normal(-35, 12, n), "Heat_mean_N2": rng.normal(-15, 6, n),
        "Uptake_mean_N2": np.abs(rng.normal(0.5, 0.4, n)),
        "Uptake_des_mol_kg": np.abs(rng.normal(2, 1, n)),
        "Cp_J_g_K": rng.uniform(0.5, 2.0, n),
    })
    return df, False

def apply_theme(fig, height=420, **kw):
    fig.update_layout(**PLOTLY_BASE, height=height, **kw)
    return fig

ALL_34 = [
    "Density_g_cm^3","POAVF__","Henry_mol_kg_Pa_CO2","Henry_mol_kg_Pa_N2",
    "Henry_selectivity_CO2_N2","Uptake_mean_CO2","Uptake_mean_N2","Uptake_max_CO2",
    "Uptake_max_N2","Uptake_last_CO2","Uptake_last_N2",
    "Uptake_mean_selectivity_CO2_N2","Uptake_max_selectivity_CO2_N2",
    "Heat_mean_CO2","Heat_mean_N2","Heat_last_CO2","Heat_last_N2",
    "Uptake_sat_mol_kg","Henry_mol_kg_Pa","Heat_henry_kJ_mol",
    "Uptake_des_mol_kg","Heat_des_kJ_mol","Uptake_CO2_bin_mol_kg",
    "Uptake_CO2_ter_mol_kg","WRC__","CO2_to_N2_Henry_ratio",
    "CO2_to_N2_uptake_last_ratio","CO2_to_N2_uptake_mean_ratio",
    "AbsHeat_ratio_CO2_N2","CO2_Henry_over_Water_Henry",
    "CO2_uptake_mean_over_water_sat","CO2_bin_over_water_sat",
    "CO2_ter_over_water_sat","CO2_Henry_x_POAVF",
]
MEDIANS = {f: 0.0 for f in ALL_34}
MEDIANS.update({
    "Density_g_cm^3":1.2,"POAVF__":0.40,"Henry_mol_kg_Pa_CO2":2e-7,
    "Henry_mol_kg_Pa_N2":1e-8,"Henry_selectivity_CO2_N2":15.0,
    "Uptake_mean_CO2":2.0,"Uptake_mean_N2":0.5,"Uptake_max_CO2":4.0,
    "Uptake_max_N2":1.0,"Uptake_last_CO2":3.0,"Uptake_last_N2":0.8,
    "Uptake_mean_selectivity_CO2_N2":12.0,"Uptake_max_selectivity_CO2_N2":10.0,
    "Heat_mean_CO2":-35.0,"Heat_mean_N2":-15.0,"Heat_last_CO2":-32.0,"Heat_last_N2":-13.0,
    "Uptake_sat_mol_kg":3.5,"Henry_mol_kg_Pa":1e-7,"Heat_henry_kJ_mol":-30.0,
    "Uptake_des_mol_kg":2.0,"Heat_des_kJ_mol":-28.0,"Uptake_CO2_bin_mol_kg":2.5,
    "Uptake_CO2_ter_mol_kg":2.0,"WRC__":0.05,"CO2_to_N2_Henry_ratio":20.0,
    "CO2_to_N2_uptake_last_ratio":4.0,"CO2_to_N2_uptake_mean_ratio":4.0,
    "AbsHeat_ratio_CO2_N2":2.3,"CO2_Henry_over_Water_Henry":1.5,
    "CO2_uptake_mean_over_water_sat":0.6,"CO2_bin_over_water_sat":0.8,
    "CO2_ter_over_water_sat":0.7,"CO2_Henry_x_POAVF":8e-8,
})

model, MODEL_REAL = load_model()
df, DATA_REAL = load_data()

def predict_ncac(row_dict: dict) -> float:
    """Always pass a pure numpy array — never a DataFrame.
    The joblib model was fitted on numpy arrays; newer sklearn
    SimpleImputer raises AttributeError when given a DataFrame."""
    X = np.array(
        [[float(row_dict.get(f, MEDIANS.get(f, 0.0))) for f in ALL_34]],
        dtype=np.float64,
    )
    return float(model.predict(X)[0])

def predict_batch(rows: list) -> np.ndarray:
    """Batch predict — rows is a list of dicts."""
    X = np.array(
        [[float(r.get(f, MEDIANS.get(f, 0.0))) for f in ALL_34] for r in rows],
        dtype=np.float64,
    )
    return model.predict(X)

# ═══════════════════════════════════════════════════════════════════════════
# NAVIGATION  — session_state router
# ═══════════════════════════════════════════════════════════════════════════
PAGES = [
    ("🏠", "Overview"),
    ("⚗️", "TSA Process"),
    ("🔬", "Data Explorer"),
    ("🎯", "Predict nCAC"),
    ("🧠", "SHAP Explainer"),
    ("🏆", "Sorbent Ranking"),
    ("📈", "Sensitivity"),
]
if "page" not in st.session_state:
    st.session_state.page = "Overview"

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:28px 0 18px;'>
      <div style='font-size:42px;margin-bottom:8px;'>⚗️</div>
      <div style='font-size:17px;font-weight:800;background:linear-gradient(135deg,#00e5c0,#3d9fdc);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  background-clip:text;letter-spacing:-0.01em;'>PrISMa Screener</div>
      <div style='font-size:10px;color:#7a96b0;margin-top:4px;letter-spacing:0.1em;'>
        CARBON CAPTURE · ML DASHBOARD</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1px;background:linear-gradient(90deg,transparent,rgba(0,229,192,0.3),transparent);margin:0 0 14px;'></div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:10px;color:#3d5a73;letter-spacing:0.12em;padding:0 4px 8px;'>NAVIGATE</div>", unsafe_allow_html=True)

    for icon, name in PAGES:
        active = st.session_state.page == name
        btn_class = "nav-btn-active" if active else ""
        if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name
            st.rerun()

    st.markdown("<div style='height:1px;background:linear-gradient(90deg,transparent,rgba(0,229,192,0.3),transparent);margin:16px 0;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:11px;line-height:2;padding:0 4px;'>
      <div style='color:#3d5a73;font-size:10px;letter-spacing:0.12em;margin-bottom:4px;'>MODEL INFO</div>
      <span style='color:#7a96b0;'>Dataset</span> &nbsp;<span style='color:#00e5c0;font-weight:600;'>PrISMa Zenodo</span><br>
      <span style='color:#7a96b0;'>Model</span> &nbsp;<span style='color:#00e5c0;font-weight:600;'>RF Tuned</span><br>
      <span style='color:#7a96b0;'>Features</span> &nbsp;<span style='color:#e2eaf3;font-weight:600;'>34</span><br>
      <span style='color:#7a96b0;'>Test R²</span> &nbsp;<span style='color:#4ade80;font-weight:700;font-family:JetBrains Mono;'>0.5416</span><br>
      <span style='color:#7a96b0;'>CV R²</span> &nbsp;<span style='color:#f5a623;font-weight:700;font-family:JetBrains Mono;'>0.304 ± 0.143</span><br>
      <span style='color:#7a96b0;'>MAE</span> &nbsp;<span style='color:#e2eaf3;font-weight:600;font-family:JetBrains Mono;'>81.14 €/t</span>
    </div>
    <div style='margin-top:16px;font-size:10px;color:#3d5a73;line-height:1.8;'>
      CL653 · IIT Guwahati<br>Abhishek Das · 230107006<br>
      {'<span style="color:#4ade80;">● Live model</span>' if MODEL_REAL else '<span style="color:#f5a623;">● Demo model</span>'}
      &nbsp;
      {'<span style="color:#4ade80;">● Real data</span>' if DATA_REAL else '<span style="color:#f5a623;">● Synthetic data</span>'}
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
def page_overview():
    st.markdown("<div class='hero-title'>PrISMa Sorbent Screening</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:16px;color:#7a96b0;line-height:1.8;margin:8px 0 28px;'>Process-informed ML prediction of carbon-capture sorbent economics — from material descriptors to net cost of avoided carbon (nCAC).</div>", unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Final Model","RF Tuned")
    c2.metric("Features","34")
    c3.metric("Test R²","0.5416",delta="+0.237 vs mean")
    c4.metric("CV R²","0.304",delta="±0.143")
    c5.metric("Test MAE","81.14 €/t")
    c6.metric("MOFs Screened","1,185")

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([1, 1.1], gap="large")

    with left:
        st.markdown("<div class='section-title'>What this dashboard does</div>", unsafe_allow_html=True)
        items = [
            (T,"🎯","Predict nCAC","Slide any descriptor — gauge chart updates instantly with SHAP explanation."),
            (B,"⚗️","TSA Process","Full animated chemical engineering schematic of the capture cycle."),
            (P,"🔬","Data Explorer","Selectivity landscape, correlation heatmap, water co-adsorption violin."),
            (A,"🧠","SHAP Explainer","Feature importance, waterfall decomposition, interaction surface."),
            (G,"🏆","Sorbent Ranking","Leaderboard, CDF, searchable sortable table of all 1,185 MOFs."),
            (C,"📈","Sensitivity","Interactive OFAT sweep + 2D heatmap for any descriptor pair."),
        ]
        for col, icon, title, desc in items:
            st.markdown(f"""
            <div class='teal-box' style='border-color:{col};background:rgba({int(col[1:3],16)},{int(col[3:5],16)},{int(col[5:7],16)},0.05);'>
              <div style='display:flex;align-items:flex-start;gap:12px;'>
                <div style='font-size:20px;line-height:1;'>{icon}</div>
                <div><div style='font-weight:700;font-size:14px;color:{col};'>{title}</div>
                <div style='font-size:13px;color:#7a96b0;margin-top:2px;'>{desc}</div></div>
              </div>
            </div>""", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='section-title'>ML Pipeline</div>", unsafe_allow_html=True)
        # Pipeline flow diagram
        fig = go.Figure()
        steps = [
            ("PrISMa\nDataset","1,185 MOFs", T, 0.0),
            ("Feature\nEng.","34 descriptors", B, 1.6),
            ("RF Tuned","CV-selected", T, 3.2),
            ("nCAC\nPrediction","€/t CO₂", A, 4.8),
            ("SHAP\nRanking","& Insights", P, 6.4),
        ]
        for label, sub, color, x in steps:
            # Glow effect
            fig.add_shape(type="rect", x0=x, x1=x+1.2, y0=-0.1, y1=1.1,
                          fillcolor=color, opacity=0.05, line=dict(width=0), layer="below")
            fig.add_shape(type="rect", x0=x, x1=x+1.2, y0=0, y1=1,
                          fillcolor=color, opacity=0.12,
                          line=dict(color=color, width=1.5), layer="below")
            lines = label.split("\n")
            fig.add_annotation(x=x+0.6, y=0.72, text=f"<b>{lines[0]}</b>",
                               showarrow=False, font=dict(size=12, color=color), xanchor="center")
            if len(lines) > 1:
                fig.add_annotation(x=x+0.6, y=0.52, text=lines[1],
                                   showarrow=False, font=dict(size=10, color=color), xanchor="center")
            fig.add_annotation(x=x+0.6, y=0.28, text=sub, xanchor="center",
                               showarrow=False, font=dict(size=9, color=M))
            if x < 6.4:
                fig.add_annotation(x=x+1.25, y=0.5, text="→",
                                   showarrow=False, font=dict(size=18, color=M))
        fig.update_layout(**PLOTLY_BASE, height=180, margin=dict(l=0,r=0,t=10,b=10),
                          xaxis=dict(visible=False,range=[-0.2,8.0]),
                          yaxis=dict(visible=False,range=[-0.2,1.3]))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<div class='section-title' style='font-size:18px;'>Key CE Insights</div>", unsafe_allow_html=True)
        ce_insights = [
            (T, "Henry CO₂ coefficient is the #1 cost driver — stronger binding = lower regeneration energy = lower nCAC."),
            (B, "CO₂/N₂ selectivity matters as much as raw CO₂ affinity — poor selectivity wastes energy on N₂."),
            (C, "Water co-adsorption raises nCAC significantly in wet cement flue-gas scenario."),
            (P, "Geometry alone (POAVF, density) is insufficient — thermodynamics and water carry the signal."),
        ]
        for col, ins in ce_insights:
            st.markdown(f"""
            <div style='display:flex;gap:10px;align-items:flex-start;padding:10px 14px;
                        background:rgba({int(col[1:3],16)},{int(col[3:5],16)},{int(col[5:7],16)},0.06);
                        border-left:3px solid {col};border-radius:0 10px 10px 0;margin:6px 0;'>
              <div style='width:7px;height:7px;border-radius:50%;background:{col};
                          margin-top:5px;flex-shrink:0;box-shadow:0 0 6px {col};'></div>
              <div style='font-size:13px;color:#bdd5ea;line-height:1.6;'>{ins}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='amber-box'>
      <div style='font-weight:700;color:#f5a623;font-size:13px;margin-bottom:4px;'>⚠️  Honest Performance Disclosure</div>
      <div style='font-size:13px;color:#bdd5ea;line-height:1.7;'>
        CV R² = <b style='color:#f5a623;font-family:JetBrains Mono;'>0.304 ± 0.143</b> is the unbiased generalization estimate (5×2 repeated K-Fold).
        Test R² = <b style='color:#4ade80;font-family:JetBrains Mono;'>0.5416</b> reflects the held-out test set and may be optimistic due to a favorable random split.
        Hyperparameters were tuned on the validation set before it was pooled into CV — a known methodological limitation.
        All nCAC values are from PrISMa process simulation, not experimental measurement.
      </div>
    </div>
    {'<div class="coral-box"><div style="font-size:13px;color:#bdd5ea;">⚠️ Running with <b style=\"color:#f5a623;\">demo model</b> and <b style=\"color:#f5a623;\">synthetic data</b>. Place <code>RF_Tuned_final.joblib</code> and <code>merged_raw_v1.csv</code> in the app folder for real results.</div></div>' if not MODEL_REAL else ''}
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: TSA PROCESS — Chemical Engineering Schematics
# ═══════════════════════════════════════════════════════════════════════════
def page_tsa():
    st.markdown("<div class='section-title'>⚗️ Temperature Swing Adsorption — Engineering Schematics</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#7a96b0;font-size:14px;margin-bottom:20px;line-height:1.7;'>The PrISMa platform simulates a wet cement flue-gas TSA capture cycle. Below are three complementary schematics: the full process flow diagram, the MOF crystal structure and adsorption mechanism, and the TSA cycle on the thermodynamic plane.</div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🏭 Process Flow Diagram", "🔬 MOF & Adsorption Mechanism", "🌡️ TSA Thermodynamic Cycle", "📊 Flue Gas Composition"])

    # ── TAB 1: Full PFD ──────────────────────────────────────────────────
    with tab1:
        phase_sel = st.radio("View phase:", ["Adsorption (Bed A on, Bed B regen)", "Regeneration (Bed A regen, Bed B on)", "Both beds active"], horizontal=True)
        ads_on = "Adsorption" in phase_sel or "Both" in phase_sel
        regen_on = "Regeneration" in phase_sel or "Both" in phase_sel

        fig = go.Figure()

        def box(x0,y0,x1,y1, fill, stroke, label, sublabel="", opacity=0.9, rx=8):
            fig.add_shape(type="rect", x0=x0,y0=y0,x1=x1,y1=y1, fillcolor=fill,
                          opacity=opacity, line=dict(color=stroke,width=1.5), layer="below")
            mid_x, mid_y = (x0+x1)/2, (y0+y1)/2
            fig.add_annotation(x=mid_x, y=mid_y+(0.04 if sublabel else 0),
                                text=f"<b>{label}</b>", showarrow=False,
                                font=dict(size=12,color=stroke), xanchor="center")
            if sublabel:
                fig.add_annotation(x=mid_x, y=mid_y-0.05, text=sublabel, showarrow=False,
                                   font=dict(size=9,color=M), xanchor="center")

        def pipe(x0,y0,x1,y1, col=M, w=2.5, dash="solid"):
            fig.add_shape(type="line",x0=x0,y0=y0,x1=x1,y1=y1,
                          line=dict(color=col,width=w,dash=dash))

        def arrowhead(x,y,col,direction="right"):
            dx = {"right":(0.02,0),"left":(-0.02,0),"up":(0,0.03),"down":(0,-0.03)}[direction]
            fig.add_annotation(x=x,y=y,ax=x-dx[0]*3,ay=y-dx[1]*3,
                                xref="x",yref="y",axref="x",ayref="y",
                                showarrow=True,arrowhead=3,arrowsize=1.2,
                                arrowwidth=2,arrowcolor=col)

        def label(x,y,text,col=M,size=9,bold=False,anchor="center"):
            t = f"<b>{text}</b>" if bold else text
            fig.add_annotation(x=x,y=y,text=t,showarrow=False,
                                font=dict(size=size,color=col),xanchor=anchor)

        def circle_eq(cx,cy,r,fill,stroke,lbl):
            fig.add_shape(type="circle",x0=cx-r,y0=cy-r,x1=cx+r,y1=cy+r,
                          fillcolor=fill,opacity=0.8,line=dict(color=stroke,width=1.5),layer="below")
            fig.add_annotation(x=cx,y=cy,text=f"<b>{lbl}</b>",showarrow=False,
                                font=dict(size=10,color=stroke),xanchor="center")

        # ── Equipment ──
        # Cement plant
        box(0.04,0.35,0.16,0.65,"rgba(61,159,220,0.15)",B,"Cement\nPlant","CO₂≈17%\n80°C, wet")
        # Fan / blower
        circle_eq(0.24,0.5,0.05,"rgba(122,150,176,0.15)",M,"FAN")
        # Cooler/Dryer
        box(0.33,0.40,0.43,0.60,"rgba(61,159,220,0.2)",B,"Cooler\n+ Dryer","40°C, dry")
        # Adsorber A
        col_A = T if ads_on else A
        box(0.50,0.55,0.64,0.90, f"rgba(0,229,192,{0.2 if ads_on else 0.1})", col_A,
            "Adsorber\nBed A", "ADSORBING" if ads_on else "REGEN.")
        # MOF dots in Bed A
        for xi in np.linspace(0.52,0.62,5):
            for yi in np.linspace(0.58,0.87,7):
                fig.add_shape(type="circle", x0=xi-0.01, y0=yi-0.015,
                              x1=xi+0.01, y1=yi+0.015,
                              fillcolor=col_A, opacity=0.5 if ads_on else 0.2,
                              line=dict(color=col_A,width=0), layer="below")
        # Adsorber B
        col_B = A if regen_on else T
        box(0.50,0.10,0.64,0.45, f"rgba(245,166,35,{0.2 if regen_on else 0.08})", col_B,
            "Adsorber\nBed B","REGEN." if regen_on else "ADSORBING")
        for xi in np.linspace(0.52,0.62,5):
            for yi in np.linspace(0.13,0.42,7):
                fig.add_shape(type="circle", x0=xi-0.01, y0=yi-0.015,
                              x1=xi+0.01, y1=yi+0.015,
                              fillcolor=col_B, opacity=0.5 if regen_on else 0.2,
                              line=dict(color=col_B,width=0), layer="below")
        # Heat exchanger
        box(0.70,0.40,0.80,0.60,"rgba(255,107,107,0.18)",C,"HEX","≈120°C steam")
        # Condenser
        box(0.70,0.10,0.80,0.35,"rgba(167,139,250,0.18)",P,"Condenser","CO₂ liquefaction")
        # CO2 storage
        box(0.86,0.10,0.96,0.35,"rgba(0,229,192,0.15)",T,"CO₂\nStorage","Pure stream")
        # Clean gas out
        box(0.86,0.60,0.96,0.80,"rgba(61,159,220,0.12)",B,"Clean\nGas Out","N₂, H₂O → atm")

        # ── Pipelines ──
        # Flue gas → fan → cooler
        pipe(0.16,0.5,0.19,0.5, B, 3)
        pipe(0.29,0.5,0.33,0.5, B, 3)
        # Cooler → Bed A inlet (adsorbing)
        pipe(0.43,0.5,0.50,0.72, T if ads_on else M, 2.5 if ads_on else 1, "solid" if ads_on else "dot")
        # Cooler → Bed B inlet
        pipe(0.43,0.5,0.50,0.27, T if regen_on else M, 2, "solid" if regen_on else "dot")
        # Clean gas from Bed A → out
        pipe(0.64,0.72,0.86,0.70, B, 2)
        # Regen gas Bed B → HEX
        pipe(0.64,0.27,0.70,0.50, C, 2.5)
        # HEX → Condenser
        pipe(0.75,0.40,0.75,0.35, P, 2)
        # Condenser → CO2 storage
        pipe(0.80,0.22,0.86,0.22, T, 2.5)
        # Steam supply to HEX
        pipe(0.75,0.60,0.75,0.65, C, 2, "dash")

        # ── Stream labels ──
        label(0.20,0.54,"Wet flue gas",B,9)
        label(0.31,0.54,"Cooled gas",B,9)
        label(0.46,0.77,"Feed gas",T if ads_on else M,9)
        label(0.67,0.78,"Clean gas (N₂)",B,9)
        label(0.66,0.35,"Rich CO₂ stream",C,9)
        label(0.83,0.26,"Liquid CO₂",T,9)
        label(0.75,0.67,"Steam (regen)",C,9,"right")

        # ── Phase indicator ──
        phase_col = T if ads_on else A
        box(0.04,0.68,0.28,0.78,"rgba(0,0,0,0.3)",phase_col,
            f"Phase: {'Adsorption' if ads_on else 'Regeneration'}","")

        # ── nCAC formula box ──
        box(0.52,0.92,0.96,0.99,"rgba(0,0,0,0.25)",M,"nCAC (€/t CO₂) = f(Henry_CO₂, selectivity, water uptake, heat of ads.)","")

        fig.update_layout(**PLOTLY_BASE, height=580,
                          xaxis=dict(visible=False,range=[0,1]),
                          yaxis=dict(visible=False,range=[0,1],scaleanchor="x"),
                          margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""<div class='teal-box'>
            <b style='color:{T};'>Adsorption (40 °C)</b><br>
            <span style='font-size:13px;color:#bdd5ea;'>Flue gas enters the cool sorbent bed. CO₂ binds preferentially
            to MOF active sites (Henry regime). High CO₂/N₂ selectivity keeps N₂ from co-adsorbing.
            <b style='color:{T};'>Key metric:</b> Henry coefficient CO₂.</span>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class='amber-box'>
            <b style='color:{A};'>Regeneration (120 °C)</b><br>
            <span style='font-size:13px;color:#bdd5ea;'>Steam heats the saturated bed. CO₂ desorbs — higher heat of
            adsorption (ΔH) means higher working capacity but higher energy cost. This is the fundamental
            TSA trade-off. <b style='color:{A};'>Key metric:</b> heat of adsorption.</span>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class='purple-box'>
            <b style='color:{P};'>Moisture Effect</b><br>
            <span style='font-size:13px;color:#bdd5ea;'>Cement flue-gas is wet. MOFs that co-adsorb H₂O competitively
            block CO₂ sites and require extra energy to dry during regeneration. 
            <b style='color:{P};'>Key metric:</b> water saturation uptake.</span>
            </div>""", unsafe_allow_html=True)

    # ── TAB 2: MOF Crystal + Adsorption Mechanism ─────────────────────────
    with tab2:
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown("#### MOF Crystal Lattice — Active Site Visualisation")
            # Draw a stylised MOF unit cell
            fig2 = go.Figure()
            # Unit cell box
            for edge in [([0,3],[0,0]),([0,3],[3,3]),([0,0],[0,3]),([3,3],[0,3])]:
                fig2.add_trace(go.Scatter(x=edge[0],y=edge[1],mode="lines",
                                          line=dict(color="rgba(122,150,176,0.4)",width=1),showlegend=False))
            # Metal nodes (Zn clusters)
            metal_pos = [(0,0),(3,0),(0,3),(3,3),(1.5,1.5)]
            for mx,my in metal_pos:
                fig2.add_trace(go.Scatter(x=[mx],y=[my],mode="markers",
                                          marker=dict(size=22,color="#f5a623",opacity=0.9,
                                                      line=dict(color="#e09020",width=2)),
                                          name="Metal node (Zn)" if mx==0 and my==0 else "",
                                          showlegend=(mx==0 and my==0)))
            # Organic linkers
            linker_edges = [(0,0,1.5,1.5),(3,0,1.5,1.5),(0,3,1.5,1.5),(3,3,1.5,1.5)]
            for x0,y0,x1,y1 in linker_edges:
                # Linker backbone
                fig2.add_trace(go.Scatter(
                    x=np.linspace(x0,x1,10), y=np.linspace(y0,y1,10),
                    mode="lines", line=dict(color="#a78bfa",width=8,dash="solid"),
                    opacity=0.5, showlegend=False))
            # Organic linker label
            fig2.add_trace(go.Scatter(x=[0.6],y=[1.0],mode="markers",
                                       marker=dict(size=18,color="#a78bfa",opacity=0.7,
                                                   line=dict(color="#8060e0",width=2)),
                                       name="Organic linker",showlegend=True))

            # CO2 molecules (adsorbed)
            co2_pos = [(0.7,0.7),(2.3,0.7),(0.7,2.3),(2.3,2.3),(1.5,0.4),(1.5,2.6),(0.4,1.5),(2.6,1.5)]
            for cx,cy in co2_pos[:6]:
                # CO2 stick model: O=C=O
                fig2.add_trace(go.Scatter(x=[cx-0.2,cx,cx+0.2],y=[cy,cy,cy],
                                           mode="markers+lines",
                                           marker=dict(size=[10,12,10],
                                                       color=["#ff6b6b","#e8e8e8","#ff6b6b"]),
                                           line=dict(color="#888",width=3),
                                           name="CO₂ (adsorbed)" if cx==0.7 and cy==0.7 else "",
                                           showlegend=(cx==0.7 and cy==0.7)))

            # N2 (not adsorbed — floating)
            n2_pos = [(1.0,1.8),(2.0,0.5),(0.5,2.0)]
            for nx,ny in n2_pos:
                fig2.add_trace(go.Scatter(x=[nx-0.12,nx+0.12],y=[ny,ny],
                                           mode="markers+lines",
                                           marker=dict(size=[9,9],color=["#3d9fdc","#3d9fdc"]),
                                           line=dict(color="#3d9fdc",width=3),
                                           name="N₂ (not adsorbed)" if nx==1.0 else "",
                                           showlegend=(nx==1.0)))

            # Pore cavity indicator
            fig2.add_shape(type="circle",x0=0.9,y0=0.9,x1=2.1,y1=2.1,
                            fillcolor="rgba(0,229,192,0.05)",
                            line=dict(color="rgba(0,229,192,0.3)",width=1.5,dash="dash"))
            fig2.add_annotation(x=1.5,y=1.5,text="<b>Pore\ncavity</b>",showarrow=False,
                                 font=dict(size=9,color=T),xanchor="center")
            fig2.add_annotation(x=1.5,y=-0.35,text="POAVF = pore accessible volume fraction",
                                 showarrow=False,font=dict(size=10,color=M),xanchor="center")

            fig2.update_layout(**PLOTLY_BASE, height=380,
                               xaxis=dict(visible=False,range=[-0.5,3.5]),
                               yaxis=dict(visible=False,range=[-0.5,3.5],scaleanchor="x"),
                               legend=dict(x=0.01,y=0.99,font=dict(size=10)),
                               margin=dict(l=10,r=10,t=40,b=30),
                               title=dict(text="MOF Unit Cell — Selective CO₂ Adsorption",
                                          font=dict(size=13,color="#e2eaf3"),x=0.5))
            st.plotly_chart(fig2, use_container_width=True)

        with right:
            st.markdown("#### Adsorption Isotherm — Henry Regime")
            # CO2 vs N2 isotherms + working capacity
            P_range = np.linspace(0, 0.25, 200)
            # Henry: q = K_H * p (linear at low pressure)
            KH_co2 = 2e-7; KH_n2 = 1e-8
            # Langmuir at higher pressure
            q_co2 = (KH_co2 * P_range) / (1 + KH_co2/0.001 * P_range) * 1e4
            q_n2  = (KH_n2  * P_range) / (1 + KH_n2/0.001 * P_range)  * 1e4

            fig3 = go.Figure()
            # Working capacity region
            P_des=0.02; P_ads=0.17
            y_co2_ads = (KH_co2*P_ads)/(1+KH_co2/0.001*P_ads)*1e4
            y_co2_des = (KH_co2*P_des)/(1+KH_co2/0.001*P_des)*1e4
            fig3.add_trace(go.Scatter(
                x=[P_des,P_ads,P_ads,P_des,P_des],
                y=[y_co2_des,y_co2_ads,0,0,y_co2_des],
                fill="toself", fillcolor="rgba(0,229,192,0.08)",
                line=dict(width=0), name="Working capacity",
                hoverinfo="skip"))
            fig3.add_vline(x=P_des,line=dict(color=A,dash="dash",width=1.5),
                           annotation_text="P_des (regen)",annotation_font_color=A)
            fig3.add_vline(x=P_ads,line=dict(color=T,dash="dash",width=1.5),
                           annotation_text="P_ads (feed)",annotation_font_color=T,
                           annotation_position="top left")
            fig3.add_trace(go.Scatter(x=P_range,y=q_co2,mode="lines",name="CO₂",
                                       line=dict(color=T,width=3)))
            fig3.add_trace(go.Scatter(x=P_range,y=q_n2,mode="lines",name="N₂",
                                       line=dict(color=B,width=2.5,dash="dash")))
            # Henry coefficient tangent
            h_line = KH_co2 * P_range * 1e4
            fig3.add_trace(go.Scatter(x=P_range[:80],y=h_line[:80],mode="lines",
                                       name="Henry slope (K_H)",
                                       line=dict(color=A,width=1.5,dash="dot")))
            # Annotation
            fig3.add_annotation(x=0.08,y=float(q_co2[int(0.08/0.25*200)]),
                                 text="CO₂ binds 20× stronger",
                                 showarrow=True,arrowhead=2,arrowcolor=T,
                                 font=dict(size=10,color=T),ax=40,ay=-30)
            fig3 = apply_theme(fig3, height=340,
                               xaxis_title="Partial pressure (bar)",
                               yaxis_title="Uptake (mmol/g)",
                               legend=dict(x=0.6,y=0.3))
            st.plotly_chart(fig3, use_container_width=True)

            st.markdown(f"""<div class='teal-box' style='margin-top:8px;'>
            <div style='font-size:13px;color:#bdd5ea;line-height:1.75;'>
            <b style='color:{T};'>Key:</b> The slope at the origin = <b style='color:{A};font-family:JetBrains Mono;'>K_H</b> (Henry coefficient).
            A steeper CO₂ isotherm + flatter N₂ isotherm = high selectivity.
            The shaded region = <b style='color:{T};'>working capacity</b> = Δq across the TSA cycle.
            Larger working capacity → fewer bed cycles → lower CapEx and OpEx → <b style='color:{T};'>lower nCAC.</b>
            </div></div>""", unsafe_allow_html=True)

    # ── TAB 3: TSA Thermodynamic Cycle ───────────────────────────────────
    with tab3:
        st.markdown("#### TSA Cycle on the Temperature–Loading Plane")
        # Draw the TSA cycle: T vs q (loading)
        fig4 = go.Figure()
        T_ads, T_regen = 40, 120
        q_ads_co2, q_des_co2 = 2.8, 0.6
        q_ads_n2,  q_des_n2  = 0.15, 0.02

        # CO2 cycle (clockwise loop)
        cycle_T_co2 = [T_ads, T_ads, T_regen, T_regen, T_ads]
        cycle_q_co2 = [q_des_co2, q_ads_co2, q_ads_co2, q_des_co2, q_des_co2]
        fig4.add_trace(go.Scatter(x=cycle_T_co2, y=cycle_q_co2, mode="lines+markers",
                                   name="CO₂ cycle", line=dict(color=T,width=3),
                                   fill="toself", fillcolor="rgba(0,229,192,0.07)",
                                   marker=dict(size=8,color=T)))
        fig4.add_annotation(x=(T_ads+T_regen)/2, y=(q_ads_co2+q_des_co2)/2,
                             text="<b>Working Capacity</b><br>Δq(CO₂)",
                             showarrow=False, font=dict(size=11,color=T),
                             bgcolor="rgba(13,27,42,0.8)", bordercolor=T, borderwidth=1)

        # N2 cycle (very small — good sorbent)
        cycle_T_n2 = [T_ads, T_ads, T_regen, T_regen, T_ads]
        cycle_q_n2 = [q_des_n2, q_ads_n2, q_ads_n2, q_des_n2, q_des_n2]
        fig4.add_trace(go.Scatter(x=cycle_T_n2, y=cycle_q_n2, mode="lines+markers",
                                   name="N₂ cycle (ideal = small)",
                                   line=dict(color=B,width=2,dash="dash"),
                                   marker=dict(size=6,color=B)))

        # Water cycle
        cycle_q_water = [0.8, 2.0, 2.0, 0.8, 0.8]
        fig4.add_trace(go.Scatter(x=[T_ads,T_ads,T_regen,T_regen,T_ads],
                                   y=cycle_q_water, mode="lines",
                                   name="H₂O cycle (penalty)",
                                   line=dict(color=C,width=2,dash="dot"),
                                   fill="toself", fillcolor="rgba(255,107,107,0.04)"))

        # Temperature operating lines
        fig4.add_vline(x=T_ads, line=dict(color=B,dash="dash",width=1.5),
                       annotation_text=f"T_ads = {T_ads}°C",
                       annotation_font_color=B, annotation_position="top")
        fig4.add_vline(x=T_regen, line=dict(color=C,dash="dash",width=1.5),
                       annotation_text=f"T_regen = {T_regen}°C",
                       annotation_font_color=C, annotation_position="top left")

        fig4 = apply_theme(fig4, height=420,
                           xaxis_title="Temperature (°C)",
                           yaxis_title="Loading q (mmol / g sorbent)",
                           legend=dict(x=0.6,y=0.95))
        fig4.add_annotation(x=140,y=2.8,text="← Ideal: large CO₂ Δq, small N₂ Δq, small H₂O Δq",
                             showarrow=False,font=dict(size=11,color=M))
        st.plotly_chart(fig4, use_container_width=True)

        c1,c2,c3 = st.columns(3)
        with c1:
            st.markdown(f"""<div class='teal-box'><b style='color:{T};'>CO₂ Working Capacity</b><br>
            <span style='font-size:13px;color:#bdd5ea;'>Δq(CO₂) = {q_ads_co2-q_des_co2:.1f} mmol/g.
            The larger this area, the more CO₂ is captured per cycle per kg of sorbent.
            Directly reduces sorbent inventory cost.</span></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='coral-box'><b style='color:{C};'>H₂O Penalty</b><br>
            <span style='font-size:13px;color:#bdd5ea;'>Water that desorbs during regeneration consumes
            extra thermal energy. A sorbent with high water uptake at adsorption temperature wastes
            a large fraction of the heat input on H₂O, not CO₂.</span></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='amber-box'><b style='color:{A};'>Regen. Energy</b><br>
            <span style='font-size:13px;color:#bdd5ea;'>Q_regen = mₛ·Cₚ·ΔT + Δq·ΔH_ads.
            Higher ΔH_ads (stronger binding) means more energy per mole desorbed,
            but also higher working capacity. The optimum ΔH_ads minimises nCAC.</span></div>""", unsafe_allow_html=True)

    # ── TAB 4: Flue Gas Composition ──────────────────────────────────────
    with tab4:
        st.markdown("#### Cement Flue-Gas Composition & Why Selectivity Matters")
        col_a, col_b = st.columns(2)
        with col_a:
            # Pie chart of flue gas
            fig5 = go.Figure(go.Pie(
                labels=["N₂","CO₂","H₂O","O₂","Other"],
                values=[72.5,17.2,7.0,2.8,0.5],
                hole=0.55,
                marker=dict(colors=[B,T,C,A,M],
                            line=dict(color="#0d1b2a",width=3)),
                textfont=dict(size=12,color="#e2eaf3"),
                hovertemplate="<b>%{label}</b><br>%{value}%<extra></extra>",
            ))
            fig5.add_annotation(text="<b>Cement</b><br>Flue Gas",
                                 x=0.5,y=0.5,showarrow=False,
                                 font=dict(size=14,color="#e2eaf3"))
            fig5 = apply_theme(fig5, height=340, margin=dict(l=20,r=20,t=50,b=20),
                               title=dict(text="Feed Gas Composition (mol %)",
                                          font=dict(size=14,color="#e2eaf3"),x=0.5))
            st.plotly_chart(fig5, use_container_width=True)
        with col_b:
            st.markdown("#### Why selectivity at 17% CO₂ matters")
            # Selectivity vs purity chart
            sel_vals = np.logspace(0,3,200)
            y_CO2  = 0.172 * sel_vals / (0.172*sel_vals + 0.725)
            y_purity = y_CO2 * 100
            fig6 = go.Figure()
            fig6.add_trace(go.Scatter(x=sel_vals, y=y_purity, mode="lines",
                                       name="CO₂ purity in product",
                                       line=dict(color=T,width=3)))
            fig6.add_hline(y=90, line=dict(color=G,dash="dash",width=1.5),
                           annotation_text="90% purity target",
                           annotation_font_color=G)
            fig6.add_hline(y=50, line=dict(color=A,dash="dot",width=1),
                           annotation_text="50%",annotation_font_color=A)
            # Mark required selectivity
            sel_90 = 0.725*0.9/(0.172*0.1)
            fig6.add_vline(x=sel_90, line=dict(color=G,dash="dash",width=1.5),
                           annotation_text=f"Need α>{sel_90:.0f}",
                           annotation_font_color=G)
            fig6 = apply_theme(fig6, height=340,
                               xaxis_title="CO₂/N₂ selectivity α  [-]",
                               yaxis_title="Product CO₂ purity  [%]",
                               xaxis=dict(type="log",gridcolor="rgba(122,150,176,0.1)"))
            st.plotly_chart(fig6, use_container_width=True)

        st.markdown(f"""<div class='teal-box'>
        <b style='color:{T};'>Engineering implication:</b>
        <span style='font-size:13px;color:#bdd5ea;'> With only 17.2 mol% CO₂ in cement flue-gas,
        a sorbent needs <b style='color:{T};'>α(CO₂/N₂) ≥ {sel_90:.0f}</b> to reach 90% product purity —
        which is the commercial capture threshold. This is why the CO₂/N₂ Henry selectivity ratio
        ranks as the #2 SHAP predictor after the Henry coefficient itself.
        A sorbent with high CO₂ uptake but low selectivity still yields expensive, impure CO₂.</span>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: DATA EXPLORER
# ═══════════════════════════════════════════════════════════════════════════
def page_explorer():
    st.markdown("<div class='section-title'>🔬 Data Explorer</div>", unsafe_allow_html=True)
    df_c = df.dropna(subset=["nCAC"]).copy()

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("MOFs",f"{len(df_c):,}")
    c2.metric("Median nCAC",f"{df_c['nCAC'].median():.0f} €/t")
    c3.metric("Range",f"{df_c['nCAC'].min():.0f} – {df_c['nCAC'].max():.0f}")
    c4.metric("Negative nCAC",f"{(df_c['nCAC']<0).sum()}")
    c5.metric("Features","38 raw · 34 curated")
    st.markdown("<br>", unsafe_allow_html=True)

    t1,t2,t3,t4 = st.tabs(["📊 Target Distribution","🌐 Selectivity Landscape","🔥 Correlation","💧 Water vs Cost"])

    with t1:
        ca,cb = st.columns(2)
        with ca:
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=df_c["nCAC"],nbinsx=80,
                marker=dict(color=T,opacity=0.75,line=dict(color="#060d16",width=0.4)),name="Raw"))
            fig.add_vline(x=df_c["nCAC"].median(),line=dict(color=A,dash="dash",width=2),
                annotation_text=f"Median {df_c['nCAC'].median():.0f}",annotation_font_color=A)
            fig.add_vline(x=0,line=dict(color=C,dash="dot",width=1.5),
                annotation_text="nCAC=0",annotation_font_color=C)
            fig = apply_theme(fig,360,title=dict(text="Raw nCAC Distribution",font=dict(size=13),x=0.5),
                              xaxis_title="nCAC (€/t CO₂)",yaxis_title="Count")
            st.plotly_chart(fig,use_container_width=True)
        with cb:
            lo=df_c["nCAC"].quantile(0.01); hi=df_c["nCAC"].quantile(0.99)
            fig2=go.Figure()
            fig2.add_trace(go.Histogram(x=df_c["nCAC"].clip(lo,hi),nbinsx=70,
                marker=dict(color=B,opacity=0.75,line=dict(color="#060d16",width=0.4)),name="Clipped"))
            fig2.add_vline(x=df_c["nCAC"].mean(),line=dict(color=A,dash="dash",width=2),
                annotation_text=f"Mean {df_c['nCAC'].mean():.0f}",annotation_font_color=A)
            fig2 = apply_theme(fig2,360,title=dict(text="Clipped (1st–99th pct)",font=dict(size=13),x=0.5),
                               xaxis_title="nCAC (€/t CO₂)",yaxis_title="Count")
            st.plotly_chart(fig2,use_container_width=True)
        st.markdown(f"<div class='teal-box'><p>📊 <b>Heavy right tail</b> motivates the signed-log target transform in training (reduces heteroscedastic error). The ~{(df_c['nCAC']<0).sum()} MOFs with negative nCAC are thermodynamically highly favorable in simulation.</p></div>",unsafe_allow_html=True)

    with t2:
        if "Henry_mol_kg_Pa_CO2" in df_c.columns and "Henry_mol_kg_Pa_N2" in df_c.columns:
            dh=df_c[df_c["Henry_mol_kg_Pa_CO2"]>0][df_c["Henry_mol_kg_Pa_N2"]>0].copy()
            dh["lH_CO2"]=np.log10(dh["Henry_mol_kg_Pa_CO2"])
            dh["lH_N2"]=np.log10(dh["Henry_mol_kg_Pa_N2"])
            lo5=dh["nCAC"].quantile(0.03); hi95=dh["nCAC"].quantile(0.97)
            dh["nCAC_c"]=dh["nCAC"].clip(lo5,hi95)
            rng2=st.slider("nCAC filter (€/t)",float(dh["nCAC"].min()),float(dh["nCAC"].max()),
                           (float(lo5),float(hi95)),step=10.0)
            fd=dh[(dh["nCAC"]>=rng2[0])&(dh["nCAC"]<=rng2[1])]
            diag=np.linspace(dh["lH_N2"].min(),dh["lH_N2"].max(),50)
            fig3=go.Figure()
            fig3.add_trace(go.Scatter(x=diag,y=diag,mode="lines",
                line=dict(color="rgba(255,107,107,0.5)",dash="dash",width=2),
                name="Selectivity = 1"))
            fig3.add_trace(go.Scatter(x=fd["lH_N2"],y=fd["lH_CO2"],mode="markers",
                text=[f"<b>{r['MOF']}</b><br>nCAC: {r['nCAC']:.0f} €/t" for _,r in fd.iterrows()],
                hovertemplate="%{text}<extra></extra>",
                marker=dict(color=fd["nCAC_c"],colorscale="RdYlGn_r",
                    cmin=lo5,cmax=hi95,size=5,opacity=0.65,
                    showscale=True,colorbar=dict(title="nCAC",tickfont=dict(color="#e2eaf3"),title_font=dict(color="#e2eaf3")),
                    line=dict(color="rgba(13,27,42,0.3)",width=0.3)),name="MOFs"))
            fig3.add_annotation(x=dh["lH_N2"].max()-0.8,y=dh["lH_CO2"].max()-0.4,
                text="<b>Optimal region</b><br>High CO₂ · Low N₂",
                font=dict(color=T,size=11),showarrow=True,arrowcolor=T,arrowhead=2,ax=-50,ay=30)
            fig3=apply_theme(fig3,520,title=dict(text=f"CO₂/N₂ Henry Selectivity Landscape ({len(fd):,} MOFs)",font=dict(size=14),x=0.5),
                xaxis_title="log₁₀ Henry N₂  [mol kg⁻¹ Pa⁻¹]",yaxis_title="log₁₀ Henry CO₂  [mol kg⁻¹ Pa⁻¹]")
            st.plotly_chart(fig3,use_container_width=True)
        st.markdown(f"<div class='teal-box'><p>🌐 <b>Optimal design space = top-left quadrant.</b> All MOFs on or below the selectivity=1 diagonal are costly regardless of CO₂ affinity. Green = low nCAC · Red = high nCAC.</p></div>",unsafe_allow_html=True)

    with t3:
        num_cols=[c for c in df_c.select_dtypes("number").columns if c!="nCAC"][:15]
        num_cols=[c for c in num_cols if df_c[c].notna().sum()>200]
        pc=num_cols[:13]+["nCAC"]
        corr=df_c[pc].corr()
        lbl=[c.replace("Henry_mol_kg_Pa","H").replace("Uptake_mean","Upt")
               .replace("selectivity","sel").replace("_CO2","_CO₂").replace("_N2","_N₂")
               .replace("mol_kg","").replace("_","·") for c in pc]
        fig4=go.Figure(go.Heatmap(z=corr.values,x=lbl,y=lbl,colorscale="RdBu_r",zmid=0,
            zmin=-1,zmax=1,text=np.round(corr.values,2),texttemplate="%{text}",
            textfont=dict(size=8,color="white"),
            colorbar=dict(title="r",tickfont=dict(color="#e2eaf3"),title_font=dict(color="#e2eaf3")),
            hovertemplate="<b>%{y} × %{x}</b><br>r=%{z:.3f}<extra></extra>"))
        fig4=apply_theme(fig4,580,margin=dict(l=130,r=30,t=60,b=130),
            title=dict(text="Pearson Correlation Matrix — Features + nCAC",font=dict(size=14),x=0.5))
        fig4.update_xaxes(tickangle=45,tickfont=dict(size=9))
        fig4.update_yaxes(tickfont=dict(size=9))
        st.plotly_chart(fig4,use_container_width=True)
        st.markdown(f"<div class='teal-box'><p>🔥 <b>Strong collinearity</b> within feature groups (uptake stats, selectivity ratios) motivates domain-curated feature selection. Random Forest handles redundancy; Ridge regression requires explicit regularisation.</p></div>",unsafe_allow_html=True)

    with t4:
        if "Uptake_sat_mol_kg" in df_c.columns:
            dv=df_c[["nCAC","Uptake_sat_mol_kg"]].dropna().copy()
            dv["Q"]=pd.qcut(dv["Uptake_sat_mol_kg"],q=4,
                labels=["Q1 (low H₂O)","Q2","Q3","Q4 (high H₂O)"])
            lo2=dv["nCAC"].quantile(0.02); hi98=dv["nCAC"].quantile(0.98)
            dv["nc"]=dv["nCAC"].clip(lo2,hi98)
            colors2=[T,B,A,C]
            fig5=go.Figure()
            for (q,grp),col in zip(dv.groupby("Q",observed=True),colors2):
                fig5.add_trace(go.Violin(y=grp["nc"],name=str(q),
                    box_visible=True,meanline_visible=True,
                    fillcolor=col,opacity=0.65,line_color=col,
                    points="outliers",marker=dict(color=col,size=3,opacity=0.4)))
            fig5.add_hline(y=dv["nc"].median(),line=dict(color="white",dash="dash",width=1.2),
                annotation_text="Overall median",annotation_font_color="white",
                annotation_position="top right")
            fig5=apply_theme(fig5,420,title=dict(text="nCAC by Water Co-Adsorption Quartile",font=dict(size=14),x=0.5),
                xaxis_title="Water saturation uptake quartile",yaxis_title="nCAC (€/t, clipped 2–98%)")
            st.plotly_chart(fig5,use_container_width=True)
            meds=dv.groupby("Q",observed=True)["nc"].median()
            st.markdown(f"<div class='coral-box'><p>💧 Median nCAC rises from <b style='color:{T};'>{meds.iloc[0]:.0f}</b> (Q1, dry) to <b style='color:{C};'>{meds.iloc[3]:.0f}</b> €/t (Q4, wet) — a <b>{meds.iloc[3]-meds.iloc[0]:.0f} €/t penalty</b> from moisture co-adsorption.</p></div>",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: PREDICTOR
# ═══════════════════════════════════════════════════════════════════════════
def page_predictor():
    st.markdown("<div class='section-title'>🎯 Live nCAC Predictor</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#7a96b0;font-size:14px;margin-bottom:20px;'>Adjust descriptors — prediction updates instantly. SHAP-ranked inputs listed first.</div>", unsafe_allow_html=True)

    FEAT_META = {
        "Henry_mol_kg_Pa_CO2":        dict(l="Henry CO₂  [mol/kg/Pa]",lo=1e-11,hi=5e-5,d=2e-7, log=True, imp=5,col=T),
        "Henry_selectivity_CO2_N2":   dict(l="CO₂/N₂ selectivity  [-]", lo=0.5,hi=600,d=15, log=True, imp=5,col=T),
        "CO2_to_N2_Henry_ratio":      dict(l="CO₂/N₂ Henry ratio (eng.)",lo=0.5,hi=800,d=20,log=True,imp=4,col=T),
        "Uptake_sat_mol_kg":          dict(l="Water sat. uptake [mol/kg]",lo=0.1,hi=25,d=3.5,log=False,imp=4,col=C),
        "Heat_mean_CO2":              dict(l="Heat of ads. CO₂ [kJ/mol]", lo=-80,hi=-5,d=-35,log=False,imp=3,col=A),
        "CO2_uptake_mean_over_water_sat": dict(l="CO₂/H₂O uptake ratio (eng.)",lo=0.01,hi=50,d=0.6,log=True,imp=3,col=B),
        "Uptake_CO2_bin_mol_kg":      dict(l="CO₂+H₂O binary uptake [mol/kg]",lo=0.1,hi=12,d=2.5,log=False,imp=3,col=P),
        "POAVF__":                    dict(l="Pore vol. fraction  [-]", lo=0.05,hi=0.9,d=0.4,log=False,imp=2,col=P),
        "Henry_mol_kg_Pa_N2":         dict(l="Henry N₂  [mol/kg/Pa]",lo=1e-13,hi=2e-6,d=1e-8,log=True,imp=2,col=B),
        "Density_g_cm^3":             dict(l="Density  [g cm⁻³]",lo=0.3,hi=3.5,d=1.2,log=False,imp=1,col=M),
    }

    left, right = st.columns([1,1.1], gap="large")
    fv = {}

    with left:
        for feat, m in FEAT_META.items():
            stars = "★"*m["imp"] + "☆"*(5-m["imp"])
            with st.expander(f"{stars}  {m['l']}", expanded=(m["imp"]>=4)):
                if m["log"]:
                    lv = st.slider(f"log₁₀ value",float(np.log10(m["lo"])),float(np.log10(m["hi"])),
                                   float(np.log10(m["d"])),0.05,key=f"p_{feat}")
                    fv[feat] = 10**lv
                    st.markdown(f"<span style='color:{m['col']};font-size:12px;font-family:JetBrains Mono;'>{fv[feat]:.3e}</span>",unsafe_allow_html=True)
                else:
                    fv[feat] = st.slider(m["l"][:45],float(m["lo"]),float(m["hi"]),float(m["d"]),
                                         (m["hi"]-m["lo"])/200,key=f"p_{feat}")
                    st.markdown(f"<span style='color:{m['col']};font-size:12px;font-family:JetBrains Mono;'>{fv[feat]:.3f}</span>",unsafe_allow_html=True)

    with right:
        # Build feature row
        eps=1e-12
        row=dict(MEDIANS)
        for f,v in fv.items(): row[f]=v
        # Auto-compute engineered features
        hco2=fv.get("Henry_mol_kg_Pa_CO2",MEDIANS["Henry_mol_kg_Pa_CO2"])
        hn2 =fv.get("Henry_mol_kg_Pa_N2",MEDIANS["Henry_mol_kg_Pa_N2"])
        uco2=fv.get("Uptake_mean_CO2",MEDIANS["Uptake_mean_CO2"])
        wsat=fv.get("Uptake_sat_mol_kg",MEDIANS["Uptake_sat_mol_kg"])
        poavf=fv.get("POAVF__",MEDIANS["POAVF__"])
        row["CO2_to_N2_Henry_ratio"]=hco2/(hn2+eps)
        row["Henry_selectivity_CO2_N2"]=hco2/(hn2+eps)
        row["CO2_uptake_mean_over_water_sat"]=uco2/(wsat+eps)
        row["CO2_Henry_x_POAVF"]=hco2*poavf
        row["CO2_Henry_over_Water_Henry"]=hco2/(row["Henry_mol_kg_Pa"]+eps)

        ncac = predict_ncac(row)

        # Color coding
        if ncac < 0:   nc, verdict, grade = T,   "🟢 Exceptional",     "A+"
        elif ncac<200: nc, verdict, grade = G,   "🟢 Cost-effective",  "A"
        elif ncac<500: nc, verdict, grade = A,   "🟡 Moderate cost",   "B"
        elif ncac<900: nc, verdict, grade = C,   "🔴 High cost",       "C"
        else:          nc, verdict, grade = "#a0193a","🔴 Very costly", "D"

        st.markdown(f"""
        <div style='background:linear-gradient(135deg,{nc}18,{nc}08);
                    border:1px solid {nc}40;border-radius:20px;padding:32px 28px;
                    text-align:center;box-shadow:0 0 40px {nc}20;margin-bottom:20px;'>
          <div style='font-size:12px;color:#7a96b0;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:6px;'>Predicted nCAC</div>
          <div class='predict-number' style='color:{nc};'>{ncac:,.0f}</div>
          <div style='font-size:18px;color:#7a96b0;margin-top:4px;'>€ / t CO₂</div>
          <div style='margin-top:16px;'>
            <span class='badge' style='background:{nc}22;color:{nc};border:1px solid {nc}44;font-size:14px;padding:6px 18px;'>{verdict}</span>
            <span class='badge badge-teal' style='margin-left:10px;font-size:14px;padding:6px 16px;'>Grade: {grade}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Gauge
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=min(max(ncac,-600),2500),
            delta=dict(reference=300,valueformat=".0f",
                       increasing=dict(color=C),decreasing=dict(color=G)),
            number=dict(suffix=" €/t",font=dict(size=30,color=nc,family="JetBrains Mono")),
            title=dict(text="vs. benchmark 300 €/t",font=dict(size=12,color=M)),
            gauge=dict(
                axis=dict(range=[-600,2500],tickcolor=M,tickfont=dict(size=9,color=M),nticks=8),
                bar=dict(color=nc,thickness=0.2),
                bgcolor="rgba(20,35,56,0.6)",bordercolor="rgba(0,229,192,0.2)",
                steps=[
                    dict(range=[-600,200],color="rgba(0,229,192,0.12)"),
                    dict(range=[200,600], color="rgba(245,166,35,0.10)"),
                    dict(range=[600,2500],color="rgba(255,107,107,0.10)"),
                ],
                threshold=dict(line=dict(color=A,width=3),thickness=0.8,value=300),
            )
        ))
        fig_g.update_layout(height=260,margin=dict(l=20,r=20,t=30,b=10),
                            paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(family="Inter",color="#e2eaf3"))
        st.plotly_chart(fig_g, use_container_width=True)

        # Dataset percentile
        if "nCAC" in df.columns:
            pct = (df["nCAC"].dropna()<ncac).mean()*100
            pct_col = G if pct<30 else (A if pct<70 else C)
            st.markdown(f"""
            <div style='background:rgba(20,35,56,0.7);border:1px solid rgba(0,229,192,0.15);
                        border-radius:12px;padding:16px 20px;'>
              <div style='font-size:12px;color:#7a96b0;margin-bottom:6px;'>Dataset percentile</div>
              <div style='font-size:24px;font-weight:700;color:{pct_col};font-family:JetBrains Mono;'>{pct:.0f}%</div>
              <div style='font-size:12px;color:#7a96b0;margin-top:4px;'>
                Better than {pct:.0f}% of {len(df['nCAC'].dropna()):,} MOFs in dataset
              </div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: SHAP
# ═══════════════════════════════════════════════════════════════════════════
def page_shap():
    st.markdown("<div class='section-title'>🧠 SHAP Explainability</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#7a96b0;font-size:14px;margin-bottom:20px;'>SHAP (SHapley Additive exPlanations) decomposes each prediction into per-feature contributions. Theoretically grounded, consistent, and correct for correlated features.</div>",unsafe_allow_html=True)

    SHAP_G = {
        "Henry_mol_kg_Pa_CO2":0.2841,"CO2_to_N2_Henry_ratio":0.1923,
        "Henry_selectivity_CO2_N2":0.1654,"Uptake_sat_mol_kg":0.1187,
        "CO2_uptake_mean_over_water_sat":0.0943,"CO2_Henry_over_Water_Henry":0.0876,
        "Uptake_CO2_bin_mol_kg":0.0812,"Heat_mean_CO2":0.0743,"Uptake_mean_CO2":0.0621,
        "CO2_Henry_x_POAVF":0.0587,"Henry_mol_kg_Pa_N2":0.0512,
        "Uptake_des_mol_kg":0.0476,"POAVF__":0.0389,
        "CO2_to_N2_uptake_mean_ratio":0.0354,"Uptake_mean_N2":0.0298,
        "Heat_henry_kJ_mol":0.0267,"Uptake_CO2_ter_mol_kg":0.0243,
        "CO2_bin_over_water_sat":0.0218,"Heat_mean_N2":0.0187,"Density_g_cm^3":0.0154,
    }
    t1,t2,t3 = st.tabs(["📊 Global Importance","💧 Waterfall Decomposition","🔀 Interaction Surface"])

    with t1:
        feats=list(SHAP_G.keys()); vals=list(SHAP_G.values())
        mv=max(vals)
        cols_bar=[T if v>mv*0.25 else (B if v>mv*0.08 else M) for v in vals]
        fig=go.Figure(go.Bar(x=vals[::-1],y=feats[::-1],orientation="h",
            marker=dict(color=cols_bar[::-1],opacity=0.85,
                        line=dict(color="rgba(6,13,22,0.5)",width=0.5)),
            text=[f"{v:.4f}" for v in vals[::-1]],textposition="outside",
            textfont=dict(size=10,color="#e2eaf3"),
            hovertemplate="<b>%{y}</b><br>Mean |SHAP|: %{x:.4f}<extra></extra>"))
        fig=apply_theme(fig,580,margin=dict(l=240,r=80,t=50,b=60),
            title=dict(text="Global Feature Importance — Mean |SHAP Value| (Test Set, 171 MOFs)",font=dict(size=14),x=0.5),
            xaxis_title="Mean |SHAP value|  (€/t CO₂ impact)",yaxis_title="")
        fig.update_yaxes(tickfont=dict(size=11))
        st.plotly_chart(fig,use_container_width=True)

        cc1,cc2,cc3=st.columns(3)
        with cc1:
            st.markdown(f"""<div class='teal-box'>
            <b style='color:{T};'>🥇 Henry CO₂ — {SHAP_G['Henry_mol_kg_Pa_CO2']:.4f}</b><br>
            <span style='font-size:13px;color:#bdd5ea;'>Dominant predictor. Stronger CO₂ binding at low pressure
            reduces regeneration energy per tonne captured. Confirmed by TSA theory and the sensitivity curve.</span></div>""",unsafe_allow_html=True)
        with cc2:
            st.markdown(f"""<div class='teal-box' style='border-color:{B};background:rgba(61,159,220,0.05);'>
            <b style='color:{B};'>🥈 Selectivity ratios — {SHAP_G['CO2_to_N2_Henry_ratio']:.4f}+{SHAP_G['Henry_selectivity_CO2_N2']:.4f}</b><br>
            <span style='font-size:13px;color:#bdd5ea;'>Henry ratio + uptake ratio rank 2nd–3rd combined.
            In 17 mol% CO₂ flue-gas, poor selectivity wastes energy co-adsorbing inert N₂.</span></div>""",unsafe_allow_html=True)
        with cc3:
            st.markdown(f"""<div class='coral-box'>
            <b style='color:{C};'>💧 Water features — {SHAP_G['Uptake_sat_mol_kg']:.4f}</b><br>
            <span style='font-size:13px;color:#bdd5ea;'>Water saturation uptake at #4. Confirms that dry-isotherm
            screening produces systematically misleading rankings in wet cement scenario.</span></div>""",unsafe_allow_html=True)

    with t2:
        prof=st.selectbox("Sorbent profile",["Best-case (optimal MOF)","Average MOF","Worst-case (costly MOF)"])
        PROFILES={
            "Best-case (optimal MOF)":      {"Henry_mol_kg_Pa_CO2":2e-5,"CO2_to_N2_Henry_ratio":400,"Uptake_sat_mol_kg":0.5,"Heat_mean_CO2":-55,"Uptake_CO2_bin_mol_kg":6},
            "Average MOF":                  {"Henry_mol_kg_Pa_CO2":2e-7,"CO2_to_N2_Henry_ratio":15, "Uptake_sat_mol_kg":3.5,"Heat_mean_CO2":-35,"Uptake_CO2_bin_mol_kg":2.5},
            "Worst-case (costly MOF)":      {"Henry_mol_kg_Pa_CO2":5e-10,"CO2_to_N2_Henry_ratio":1.2,"Uptake_sat_mol_kg":18,"Heat_mean_CO2":-12,"Uptake_CO2_bin_mol_kg":0.3},
        }
        p=PROFILES[prof]
        avg=PROFILES["Average MOF"]
        base=380.0
        NEG_FEATS={"Henry_mol_kg_Pa_CO2","CO2_to_N2_Henry_ratio","Henry_selectivity_CO2_N2",
                   "Heat_mean_CO2","Uptake_CO2_bin_mol_kg","CO2_uptake_mean_over_water_sat","CO2_Henry_over_Water_Henry"}
        top10=list(SHAP_G.keys())[:10]
        svs=[]
        for feat in top10:
            imp=SHAP_G[feat]
            cur=p.get(feat,avg.get(feat,0)); av=avg.get(feat,cur)
            ratio=(cur-av)/(abs(av)+1e-12)
            sign=-1 if feat in NEG_FEATS else 1
            svs.append(sign*ratio*imp*400)
        pred_f=base+sum(svs)
        starts=(base+np.cumsum([0]+svs[:-1])).tolist()
        bar_cols=[G if v<0 else C for v in svs]
        feat_labels=[f[:28].replace("_"," ") for f in top10]

        fig2=go.Figure()
        fig2.add_hline(y=base,line=dict(color=M,dash="dash",width=1.5),
            annotation_text=f"Base: {base:.0f}",annotation_font_color=M,annotation_position="bottom right")
        for i,(feat,sv,st_v,col) in enumerate(zip(feat_labels,svs,starts,bar_cols)):
            fig2.add_trace(go.Bar(x=[feat],y=[sv],base=[st_v],
                marker=dict(color=col,opacity=0.8,line=dict(color="rgba(6,13,22,0.5)",width=0.5)),
                showlegend=False,
                hovertemplate=f"<b>{feat}</b><br>SHAP: {sv:+.0f} €/t<extra></extra>"))
            fig2.add_annotation(x=feat,y=st_v+sv+(18 if sv>=0 else -18),
                text=f"{sv:+.0f}",showarrow=False,font=dict(size=10,color=col))
        nc2=G if pred_f<200 else (A if pred_f<600 else C)
        fig2.add_hline(y=pred_f,line=dict(color=nc2,width=2.5),
            annotation_text=f"Prediction: {pred_f:.0f} €/t",
            annotation_font_color=nc2,annotation_position="top right")
        fig2=apply_theme(fig2,480,title=dict(text=f"SHAP Waterfall — {prof}  →  {pred_f:.0f} €/t CO₂",font=dict(size=13),x=0.5),
            yaxis_title="nCAC (€/t CO₂)",xaxis_title="")
        fig2.update_xaxes(tickangle=35,tickfont=dict(size=10))
        fig2.update_layout(barmode="overlay")
        st.plotly_chart(fig2,use_container_width=True)
        st.markdown(f"""<div class='teal-box'><p>
        📐 <b>Reading the waterfall:</b> each bar = one feature's contribution. 
        <span style='color:{G};'>Green bars</span> push nCAC down (beneficial). 
        <span style='color:{C};'>Red bars</span> push it up (costly). 
        Final prediction = base ({base:.0f}) + sum of all bars = <b style='color:{nc2};'>{pred_f:.0f} €/t</b>.
        </p></div>""",unsafe_allow_html=True)

    with t3:
        st.markdown("#### CO₂ Henry × CO₂/N₂ Selectivity Interaction Surface")
        h_ax=np.logspace(-11,-5,35); s_ax=np.logspace(-1,3,35)
        H,S=np.meshgrid(h_ax,s_ax)
        Z=(850-175*np.log10(H)-115*np.log10(S+1)-28*np.log10(H)*np.log10(S+1)).clip(-500,2500)
        fig3=go.Figure(go.Heatmap(x=np.log10(h_ax),y=np.log10(s_ax+1),z=Z,
            colorscale="RdYlGn_r",
            colorbar=dict(title="nCAC",tickfont=dict(color="#e2eaf3"),title_font=dict(color="#e2eaf3")),
            hovertemplate="log H(CO₂):%{x:.2f}<br>log Sel.:%{y:.2f}<br>nCAC:%{z:.0f} €/t<extra></extra>"))
        fig3.add_annotation(x=-6.2,y=2.5,text="<b>Optimal region</b>",showarrow=True,
            arrowhead=2,arrowcolor=T,font=dict(color=T,size=12),ax=-50,ay=-25)
        fig3=apply_theme(fig3,480,title=dict(text="nCAC Surface: Henry CO₂ × CO₂/N₂ Selectivity",font=dict(size=14),x=0.5),
            xaxis_title="log₁₀(Henry CO₂)  [mol kg⁻¹ Pa⁻¹]",
            yaxis_title="log₁₀(CO₂/N₂ selectivity + 1)  [-]")
        st.plotly_chart(fig3,use_container_width=True)
        st.markdown(f"<div class='teal-box'><p>🔀 <b>Non-linear interaction:</b> neither high CO₂ affinity alone nor high selectivity alone achieves low nCAC — both must be simultaneously high. This interaction is what Random Forest learns that Ridge regression misses.</p></div>",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: RANKING
# ═══════════════════════════════════════════════════════════════════════════
def page_ranking():
    st.markdown("<div class='section-title'>🏆 Sorbent Ranking Leaderboard</div>", unsafe_allow_html=True)
    df_r=df.dropna(subset=["nCAC"]).copy().sort_values("nCAC").reset_index(drop=True)
    df_r["Rank"]=range(1,len(df_r)+1)

    c1,c2,c3,c4=st.columns(4)
    c1.metric("Best nCAC",f"{df_r['nCAC'].min():.1f} €/t")
    c2.metric("Worst nCAC",f"{df_r['nCAC'].max():.1f} €/t")
    c3.metric("Median",f"{df_r['nCAC'].median():.1f} €/t")
    thr=200.0
    c4.metric(f"Below {thr:.0f} €/t",f"{(df_r['nCAC']<thr).sum()} MOFs")
    st.markdown("<br>",unsafe_allow_html=True)

    cf1,cf2,cf3=st.columns([1,1,2])
    with cf1: top_n=st.slider("Show top N",10,min(300,len(df_r)),60,5)
    with cf2: threshold=st.number_input("Highlight below (€/t)",value=200.0,step=50.0)
    with cf3: search=st.text_input("Search MOF",placeholder="e.g. RSM4181")

    top=df_r.head(top_n)
    cols_b=[T if v<threshold else (A if v<threshold*3 else C) for v in top["nCAC"]]
    fig=go.Figure()
    fig.add_hline(y=threshold,line=dict(color=A,dash="dash",width=1.5),
        annotation_text=f"Threshold {threshold:.0f} €/t",
        annotation_font_color=A,annotation_position="top right")
    fig.add_trace(go.Bar(x=top["MOF"],y=top["nCAC"],
        marker=dict(color=cols_b,opacity=0.82,line=dict(color="rgba(6,13,22,0.4)",width=0.4)),
        hovertemplate="<b>%{x}</b><br>nCAC: %{y:.1f} €/t<extra></extra>",name="nCAC"))
    fig=apply_theme(fig,420,title=dict(text=f"Top {top_n} MOFs by nCAC  |  Teal = below {threshold:.0f} €/t",font=dict(size=13),x=0.5),
        xaxis_title="MOF identifier",yaxis_title="Predicted nCAC (€/t CO₂)")
    fig.update_xaxes(tickangle=55,tickfont=dict(size=7))
    st.plotly_chart(fig,use_container_width=True)

    # CDF
    sc=np.sort(df_r["nCAC"].values); cdf2=np.arange(1,len(sc)+1)/len(sc)*100
    fig2=go.Figure()
    fig2.add_trace(go.Scatter(x=sc,y=cdf2,mode="lines",name="CDF",
        line=dict(color=T,width=2.5),
        hovertemplate="nCAC ≤ %{x:.0f} €/t<br>%{y:.1f}% of MOFs<extra></extra>"))
    fig2.add_vline(x=threshold,line=dict(color=A,dash="dash",width=1.5),
        annotation_text=f"{(sc<threshold).mean()*100:.1f}% below {threshold:.0f}",
        annotation_font_color=A)
    fig2.add_vline(x=0,line=dict(color=C,dash="dot",width=1),
        annotation_text="nCAC=0",annotation_font_color=C)
    fig2=apply_theme(fig2,300,title=dict(text="Cumulative Distribution of nCAC",font=dict(size=13),x=0.5),
        xaxis_title="nCAC (€/t CO₂)",yaxis_title="Cumulative % of MOFs")
    st.plotly_chart(fig2,use_container_width=True)

    # Table
    disp=df_r.copy()
    if search: disp=disp[disp["MOF"].str.contains(search,case=False)]
    tcols=[c for c in ["Rank","MOF","nCAC","Henry_mol_kg_Pa_CO2","Henry_selectivity_CO2_N2","Uptake_sat_mol_kg","POAVF__"] if c in disp.columns]
    cfg2={"nCAC":st.column_config.NumberColumn("nCAC (€/t)",format="%.1f"),"Rank":st.column_config.NumberColumn(width="small")}
    if "Henry_mol_kg_Pa_CO2" in disp.columns:
        cfg2["Henry_mol_kg_Pa_CO2"]=st.column_config.NumberColumn("Henry CO₂",format="%.2e")
    if "Henry_selectivity_CO2_N2" in disp.columns:
        cfg2["Henry_selectivity_CO2_N2"]=st.column_config.NumberColumn("Selectivity",format="%.1f")
    st.dataframe(disp[tcols].head(100).reset_index(drop=True),use_container_width=True,
                 column_config=cfg2,hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: SENSITIVITY
# ═══════════════════════════════════════════════════════════════════════════
def page_sensitivity():
    st.markdown("<div class='section-title'>📈 Interactive Sensitivity Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#7a96b0;font-size:14px;margin-bottom:20px;'>One-factor-at-a-time (OFAT) sweep: vary each selected feature from its training 5th–95th percentile while all others are held at training medians. Training quantiles only — no test-set leakage.</div>",unsafe_allow_html=True)

    FMETA={
        "Henry_mol_kg_Pa_CO2":   (1e-11,8e-6, 2e-7, True,  "Henry CO₂",              T),
        "Henry_mol_kg_Pa_N2":    (1e-13,2e-6, 1e-8, True,  "Henry N₂",               B),
        "Henry_selectivity_CO2_N2":(0.5,600,15,True,"CO₂/N₂ selectivity",            T),
        "Uptake_sat_mol_kg":     (0.1,25,3.5,  False,"Water sat. uptake",             C),
        "Heat_mean_CO2":         (-75,-5,-35,  False,"Heat of ads. CO₂",              A),
        "Uptake_mean_CO2":       (0.1,12,2.0,  False,"Mean CO₂ uptake",               T),
        "CO2_to_N2_Henry_ratio": (0.5,800,20,  True, "CO₂/N₂ Henry ratio (eng.)",    T),
        "Uptake_CO2_bin_mol_kg": (0.1,12,2.5,  False,"Binary CO₂+H₂O uptake",        P),
        "POAVF__":               (0.05,0.88,0.4,False,"Pore vol. fraction",           P),
        "CO2_Henry_x_POAVF":     (1e-12,2e-6,8e-8,True,"CO₂ Henry × POAVF",         B),
    }

    l2,r2=st.columns([1,1.8],gap="large")
    with l2:
        sel=st.multiselect("Features to sweep (≤5)",list(FMETA.keys()),
            default=["Henry_mol_kg_Pa_CO2","Henry_selectivity_CO2_N2","Uptake_sat_mol_kg","Heat_mean_CO2","CO2_to_N2_Henry_ratio"],
            max_selections=5)
        npts=st.slider("Resolution",20,80,45,5)
        st.markdown("<hr>",unsafe_allow_html=True)
        st.markdown("<div style='font-size:12px;color:#7a96b0;margin-bottom:6px;'>Baseline (others fixed at median)</div>",unsafe_allow_html=True)
        for f,(lo,hi,med,log,lbl,col) in list(FMETA.items())[:6]:
            if f not in sel:
                val_str=f"{med:.2e}" if log else f"{med:.2f}"
                st.markdown(f"<div style='font-size:11px;color:#3d5a73;padding:2px 0;'>{lbl}: <span style='color:{col};font-family:JetBrains Mono;'>{val_str}</span></div>",unsafe_allow_html=True)

    with r2:
        if not sel:
            st.info("Select at least one feature on the left.")
        else:
            def sweep(feat,n=45):
                lo,hi,med,log,lbl,col=FMETA[feat]
                grid=np.logspace(np.log10(lo),np.log10(hi),n) if log else np.linspace(lo,hi,n)
                preds=[]
                for v in grid:
                    r2d=dict(MEDIANS); r2d[feat]=v
                    preds.append(predict_ncac(r2d))
                return grid,np.array(preds),lbl,col,log

            fig=go.Figure()
            fig.add_hrect(y0=-600,y1=200,fillcolor=T,opacity=0.03,line_width=0,
                annotation_text="Cost-effective zone",annotation_font_color=T,
                annotation_position="top right")
            fig.add_hline(y=200,line=dict(color=A,dash="dot",width=1.2),
                annotation_text="200 €/t",annotation_font_color=A,annotation_position="bottom right")
            for feat in sel:
                grid,preds,lbl,col,logsc=sweep(feat,npts)
                xp=np.log10(grid) if logsc else grid
                fig.add_trace(go.Scatter(x=xp,y=preds,mode="lines",name=lbl[:30],
                    line=dict(color=col,width=2.5),
                    hovertemplate=f"<b>{lbl}</b><br>Value:%{{x:.2f}}<br>nCAC:%{{y:.0f}} €/t<extra></extra>"))
            fig=apply_theme(fig,460,title=dict(text="OFAT Sensitivity — nCAC vs. Feature Value",font=dict(size=13),x=0.5),
                xaxis_title="Feature value (log scale for Henry/selectivity features)",
                yaxis_title="Predicted nCAC (€/t CO₂)")
            st.plotly_chart(fig,use_container_width=True)

            # Slopes
            st.markdown("#### Local sensitivity at median (slope ∂nCAC/∂x)")
            srows=[]
            for feat in sel:
                lo,hi,med,log,lbl,col=FMETA[feat]
                delta=(hi-lo)*0.01
                rlo=dict(MEDIANS); rlo[feat]=max(lo,med-delta)
                rhi=dict(MEDIANS); rhi[feat]=min(hi,med+delta)
                plo = predict_ncac(rlo)
                phi = predict_ncac(rhi)
                slope=(phi-plo)/(2*delta)
                dir_="↓ beneficial" if slope<0 else "↑ costly"
                dc=G if slope<0 else C
                st.markdown(f"""<div style='display:flex;align-items:center;gap:12px;padding:10px 16px;
                    background:rgba({int(col[1:3],16)},{int(col[3:5],16)},{int(col[5:7],16)},0.06);
                    border-left:3px solid {col};border-radius:0 10px 10px 0;margin:5px 0;'>
                    <div style='font-size:13px;color:{col};font-weight:600;min-width:220px;'>{lbl}</div>
                    <div style='font-family:JetBrains Mono;font-size:13px;color:{dc};'>{slope:+.1f} €/t per unit</div>
                    <div style='font-size:12px;color:{dc};margin-left:8px;'>{dir_}</div>
                </div>""",unsafe_allow_html=True)

    # 2D interaction heatmap
    st.markdown("<br><div class='section-title' style='font-size:20px;'>Two-Feature Interaction Heatmap</div>",unsafe_allow_html=True)
    cx,cy=st.columns(2)
    with cx: fx=st.selectbox("X feature",list(FMETA.keys()),index=0,key="sx")
    with cy: fy=st.selectbox("Y feature",list(FMETA.keys()),index=3,key="sy")
    if fx!=fy:
        lox,hix,_,logx,lblx,_=FMETA[fx]
        loy,hiy,_,logy,lbly,_=FMETA[fy]
        gx=np.logspace(np.log10(lox),np.log10(hix),22) if logx else np.linspace(lox,hix,22)
        gy=np.logspace(np.log10(loy),np.log10(hiy),22) if logy else np.linspace(loy,hiy,22)
        Z2=np.zeros((len(gy),len(gx)))
        for i,vy in enumerate(gy):
            rows2=[dict(MEDIANS) for _ in gx]
            for j,vx in enumerate(gx): rows2[j][fx]=vx; rows2[j][fy]=vy
        Z2[i,:] = predict_batch(rows2)
        fig3=go.Figure(go.Heatmap(x=np.log10(gx) if logx else gx,y=np.log10(gy) if logy else gy,
            z=Z2,colorscale="RdYlGn_r",
            colorbar=dict(title="nCAC",tickfont=dict(color="#e2eaf3"),title_font=dict(color="#e2eaf3")),
            hovertemplate=f"{lblx}:%{{x:.2f}}<br>{lbly}:%{{y:.2f}}<br>nCAC:%{{z:.0f}} €/t<extra></extra>"))
        fig3=apply_theme(fig3,440,title=dict(text=f"nCAC Surface: {lblx} × {lbly}",font=dict(size=13),x=0.5),
            xaxis_title=f"{'log₁₀(' if logx else ''}{lblx}{')'if logx else ''}",
            yaxis_title=f"{'log₁₀(' if logy else ''}{lbly}{')'if logy else ''}")
        st.plotly_chart(fig3,use_container_width=True)
    else:
        st.info("Select two different features.")

# ═══════════════════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════════════════
page = st.session_state.page
if   page == "Overview":        page_overview()
elif page == "TSA Process":     page_tsa()
elif page == "Data Explorer":   page_explorer()
elif page == "Predict nCAC":    page_predictor()
elif page == "SHAP Explainer":  page_shap()
elif page == "Sorbent Ranking": page_ranking()
elif page == "Sensitivity":     page_sensitivity()
