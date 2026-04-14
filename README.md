# PrISMa Carbon-Capture Sorbent Screening Dashboard
**CL653 — IIT Guwahati | Abhishek Das 230107006**

## Quick Start (3 steps)

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Add your model & data files
Copy these files into the `dashboard/` folder (same level as `app.py`):

| File | Source | Required? |
|------|--------|-----------|
| `RF_Tuned_final.joblib` | Google Drive → CL653_Final_Project.../04_models/ | Optional* |
| `merged_raw_v1.csv` | Google Drive → CL653_Final_Project.../02_processed_data/ | Optional* |

> *If these files are missing, the dashboard runs with a demo model and synthetic data
> that mirrors the real statistical properties. All visualisations still work.

### Step 3 — Launch
```bash
cd dashboard/
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## Dashboard Pages

| Page | Description |
|------|-------------|
| 🏠 Overview | Key metrics, pipeline diagram, CE insights |
| ⚗️ TSA Process | Animated Temperature Swing Adsorption schematic |
| 🔬 Data Explorer | EDA: selectivity landscape, heatmap, violin plots |
| 🎯 Predict nCAC | Live prediction with sliders + gauge chart |
| 🧠 SHAP Explainer | Global importance, waterfall, interaction surface |
| 🏆 Sorbent Ranking | Leaderboard, CDF, searchable table |
| 📈 Sensitivity | Interactive OFAT sweeps + 2D interaction heatmap |

---

## File Structure

```
dashboard/
├── app.py                  ← Main entry point (home page)
├── requirements.txt
├── README.md
├── assets/
│   └── style_inject.html   ← Global CSS (dark theme)
├── pages/
│   ├── 1_process.py        ← TSA schematic
│   ├── 2_explorer.py       ← Data explorer
│   ├── 3_predictor.py      ← Live predictor
│   ├── 4_shap.py           ← SHAP explainer
│   ├── 5_ranking.py        ← Sorbent leaderboard
│   └── 6_sensitivity.py    ← Sensitivity analysis
└── utils/
    └── helpers.py          ← Model loader, plot config, shared utils
```

---

## Deploying to Streamlit Community Cloud (free hosting)

1. Push the `dashboard/` folder to a public GitHub repo
2. Go to https://share.streamlit.io → New app
3. Set **Main file path** → `app.py`
4. Add secrets if needed (none required for demo mode)
5. Deploy → get a public URL for your submission Auxiliaries section

---

## References

- Charalambous et al., Nature 632 (2024) 89–94 — PrISMa platform
- Zenodo DOI: 10.5281/zenodo.12793408 — dataset
