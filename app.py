import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# ============================================================
# CONFIGURATION
# ============================================================
st.set_page_config(
    page_title=" Market Pulse",
    layout="wide",
    initial_sidebar_state="collapsed",   # collapsed par défaut sur mobile
    page_icon="📊"
)

# ============================================================
# CSS  — style original + couche responsive mobile
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=DM+Mono:wght@400;500&display=swap');

/* ── Breakpoint helper (à lire dans les règles ci-dessous)
   Mobile  : max-width 768px
   Tablette: 769px – 1024px
   Desktop : 1025px+
──────────────────────────────────────────────────────── */

:root {
    --bg:        #F4F6F9;
    --surface:   #FFFFFF;
    --border:    #DDE2EC;
    --navy:      #1A2B45;
    --navy-mid:  #243D62;
    --blue:      #2563EB;
    --blue-lt:   #3B82F6;
    --teal:      #0D9488;
    --gold:      #B45309;
    --gold-lt:   #D97706;
    --text:      #0F172A;
    --muted:     #64748B;
    --light:     #94A3B8;
    --green:     #15803D;
    --red:       #DC2626;
    --radius:    10px;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.07), 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.05);
}

/* ── Base ── */
html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
.main .block-container {
    background-color: var(--bg) !important;
    padding-top: 1.2rem !important;
    max-width: 1280px;
    /* Padding latéral adaptatif */
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: var(--navy) !important; }
[data-testid="stSidebar"] > div { padding: 1.4rem 1rem; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.88) !important; }
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'DM Serif Display', serif !important;
    color: #FCD34D !important;
    font-size: 1.05rem !important;
}
[data-testid="stSidebar"] label {
    font-size: 0.72rem !important; font-weight: 600 !important;
    letter-spacing: 0.09em !important; text-transform: uppercase !important;
    color: rgba(255,255,255,0.45) !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: rgba(253,211,77,0.2) !important;
    border: 1px solid rgba(253,211,77,0.5) !important;
    font-size: 0.75rem !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }

/* ── Banner ── */
.gmp-banner {
    background: linear-gradient(115deg, #1A2B45 0%, #243D62 55%, #1E3A5F 100%);
    border-radius: var(--radius);
    padding: 1.8rem 2.5rem;
    margin-bottom: 1.6rem;
    position: relative; overflow: hidden;
    box-shadow: var(--shadow-md);
}
.gmp-banner::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 85% 50%, rgba(253,211,77,0.12) 0%, transparent 60%);
}
.gmp-banner .eyebrow {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.22em;
    text-transform: uppercase; color: #FCD34D; margin-bottom: 0.4rem;
}
.gmp-banner h1 {
    font-family: 'DM Serif Display', serif; font-size: 1.75rem;
    color: #fff; margin: 0 0 0.75rem; line-height: 1.2;
}
.gmp-banner .badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 6px; padding: 0.28rem 0.85rem;
    font-size: 0.79rem; color: rgba(255,255,255,0.82);
    font-family: 'DM Mono', monospace;
}

/* ── KPI ── */
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem 1.3rem;
    box-shadow: var(--shadow-sm);
    position: relative; overflow: hidden;
}
.kpi-card::after {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--navy), var(--blue));
}
.kpi-card.kgreen::after { background: var(--green); }
.kpi-card.kred::after   { background: var(--red); }
.kpi-card.kgold::after  { background: linear-gradient(90deg, var(--gold), var(--gold-lt)); }
.kpi-card.kteal::after  { background: var(--teal); }
.kpi-label {
    font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--muted); margin-bottom: 0.4rem;
}
.kpi-value {
    font-family: 'DM Mono', monospace;
    font-size: 1.6rem; font-weight: 500; color: var(--navy); line-height: 1;
}
.kpi-value.vg { color: var(--green); }
.kpi-value.vr { color: var(--red); }
.kpi-value.vo { color: var(--gold); }
.kpi-value.vt { color: var(--teal); }
.kpi-sub { font-size: 0.76rem; color: var(--muted); margin-top: 0.35rem;
           white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* ── Section ── */
.sec-tag {
    display: inline-block;
    font-size: 0.63rem; font-weight: 700; letter-spacing: 0.16em;
    text-transform: uppercase; color: var(--blue);
    background: rgba(37,99,235,0.08); border-radius: 4px;
    padding: 0.14rem 0.5rem; margin-bottom: 0.3rem;
}
.sec-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem; color: var(--navy); margin: 0 0 0.25rem;
}
.sec-desc {
    font-size: 0.84rem; color: var(--muted);
    line-height: 1.6; max-width: 74ch; margin: 0 0 0.7rem;
}
.sec-divider { border: none; border-top: 1px solid var(--border); margin: 0.35rem 0 0.9rem; }

/* ── Glossaire ── */
.glos-row { display: flex; gap: 0.7rem; flex-wrap: wrap; margin-bottom: 0.9rem; }
.glos-item {
    flex: 1; min-width: 150px;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 0.65rem 0.9rem;
    font-size: 0.79rem; box-shadow: var(--shadow-sm);
}
.glos-term { font-weight: 600; color: var(--navy); margin-bottom: 0.18rem; }
.glos-def  { color: var(--muted); line-height: 1.4; }

/* ── Chart card ── */
.chart-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 0.75rem 0.3rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1rem;
}

/* ── Misc ── */
[data-testid="stCheckbox"] label { font-size: 0.84rem !important; font-weight: 500 !important; }
.stMarkdown p { color: var(--text) !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }

/* ══════════════════════════════════════════════════════════
   RESPONSIVE — MOBILE  (≤ 768 px)
   ══════════════════════════════════════════════════════════ */
@media (max-width: 768px) {

    /* Padding réduit sur petit écran */
    .main .block-container {
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;
        padding-top: 0.8rem !important;
    }

    /* Banner plus compact */
    .gmp-banner {
        padding: 1.2rem 1.2rem 1rem;
        margin-bottom: 1rem;
    }
    .gmp-banner h1 { font-size: 1.35rem; margin-bottom: 0.5rem; }
    .gmp-banner .eyebrow { font-size: 0.6rem; }
    .gmp-banner .badge {
        font-size: 0.7rem;
        padding: 0.22rem 0.65rem;
        /* Wrap si trop long */
        white-space: normal;
        line-height: 1.4;
    }

    /* KPI : 2 colonnes sur mobile au lieu de 4 */
    .kpi-grid-mobile {
        display: grid !important;
        grid-template-columns: 1fr 1fr;
        gap: 0.6rem;
        margin-bottom: 1rem;
    }
    .kpi-value { font-size: 1.25rem; }
    .kpi-label { font-size: 0.65rem; }
    .kpi-sub   { font-size: 0.7rem; }

    /* Sections */
    .sec-title { font-size: 1.05rem; }
    .sec-desc  { font-size: 0.8rem; }

    /* Glossaire : une seule colonne */
    .glos-row { flex-direction: column; }
    .glos-item { min-width: unset; }

    /* Charts : hauteur réduite */
    .chart-card { padding: 0.6rem 0.4rem 0.2rem; }
}

/* ══════════════════════════════════════════════════════════
   RESPONSIVE — TABLETTE  (769 – 1024 px)
   ══════════════════════════════════════════════════════════ */
@media (min-width: 769px) and (max-width: 1024px) {
    .main .block-container {
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    .gmp-banner { padding: 1.5rem 1.8rem; }
    .gmp-banner h1 { font-size: 1.55rem; }
    .kpi-value { font-size: 1.4rem; }
}

/* ══════════════════════════════════════════════════════════
   STREAMLIT COLUMNS → override pour mobile
   Sur mobile Streamlit empile déjà les colonnes verticalement,
   on s'assure juste que l'espacement et la largeur sont corrects.
   ══════════════════════════════════════════════════════════ */
@media (max-width: 768px) {

    /* Streamlit column wrapper */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 0.5rem !important;
    }

    /* Chaque colonne prend 100% sur mobile sauf les KPI
       (gérés via kpi-grid-mobile en HTML natif ci-dessus) */
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        min-width: 100% !important;
        width: 100% !important;
        flex: 1 1 100% !important;
    }

    /* Exception : colonnes KPI → 50% chacune */
    .kpi-cols [data-testid="stColumn"] {
        min-width: 48% !important;
        width: 48% !important;
        flex: 1 1 48% !important;
    }

    /* Slider : épaisseur du thumb plus grande pour le touch */
    [data-testid="stSlider"] .st-bp { height: 6px !important; }
    [data-testid="stSlider"] [role="slider"] {
        width: 22px !important;
        height: 22px !important;
    }

    /* Multiselect : taille confortable au touch */
    [data-baseweb="input"] { min-height: 40px !important; }
    [data-testid="stMultiSelect"] [data-baseweb="select"] {
        min-height: 44px !important;
    }

    /* Toolbar Plotly : masquée sur mobile (trop encombrante) */
    .modebar { display: none !important; }

    /* DataFrame : scroll horizontal */
    [data-testid="stDataFrame"] { overflow-x: auto !important; }
    [data-testid="stDataFrame"] > div { min-width: 400px; }

    /* Sidebar toggle button : plus grand au touch */
    [data-testid="stSidebarCollapsedControl"] button {
        width: 44px !important;
        height: 44px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# PALETTE GRAPHIQUES
# ============================================================
PALETTE = [
    "#2563EB",  # bleu vif
    "#DC2626",  # rouge
    "#16A34A",  # vert
    "#D97706",  # orange-or
    "#7C3AED",  # violet
    "#0891B2",  # cyan
    "#DB2777",  # rose
    "#65A30D",  # vert olive
    "#EA580C",  # orange foncé
    "#0D9488",  # teal
    "#9333EA",  # violet clair
    "#1D4ED8",  # bleu marine
]

# ============================================================
# DONNÉES
# ============================================================
ASSET_NAMES = {
    "^GSPC":    "S&P 500 🇺🇸",
    "^FCHI":    "CAC 40 🇫🇷",
    "^N225":    "Nikkei 225 🇯🇵",
    "GC=F":     "Or 🟡",
    "W=F":      "Blé 🌾",
    "BTC-USD":  "Bitcoin ₿",
    "ETH-USD":  "Ethereum ⟠",
    "EURUSD=X": "EUR/USD 💶",
    "AAPL":     "Apple 🍎",
    "NVDA":     "Nvidia 🔌",
    "TSLA":     "Tesla 🚗",
}

@st.cache_data
def load_data():
    df = pd.read_parquet("data/market_data.parquet")
    df = df[~df.index.duplicated(keep='last')]
    df = df.sort_index()
    return df.rename(columns=ASSET_NAMES)

try:
    df = load_data()
except Exception as e:
    st.error(f" Impossible de charger les données — relancez l'ETL. Détail : {e}")
    st.stop()

# ── Helpers ──
def hex_to_rgba(h, alpha=0.15):
    h = h.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

def is_mobile():
    """Détecte si on est sur un petit écran via les query params Streamlit."""
    try:
        w = st.query_params.get("sw", None)
        return int(w) < 769 if w else False
    except Exception:
        return False

def base_layout(**kw):
    d = dict(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F8FAFC",
        font=dict(family="DM Sans, sans-serif", color="#334155", size=13),
        xaxis=dict(
            gridcolor="#E2E8F0", linecolor="#CBD5E1",
            tickfont=dict(size=12, color="#475569"),
            title_font=dict(size=13, color="#334155"),
            zeroline=False, showgrid=True, tickangle=0,
        ),
        yaxis=dict(
            gridcolor="#E2E8F0", linecolor="#CBD5E1",
            tickfont=dict(size=12, color="#475569"),
            title_font=dict(size=13, color="#334155"),
            zeroline=False, showgrid=True,
        ),
        margin=dict(l=15, r=20, t=35, b=40),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#1A2B45",
            bordercolor="#FCD34D",
            font=dict(color="#F1F5F9", size=12, family="DM Mono, monospace"),
            namelength=-1,
        ),
    )
    d.update(kw)
    return d

LEGEND_H = dict(
    orientation="h", yanchor="bottom", y=1.03,
    xanchor="left", x=0,
    bgcolor="rgba(255,255,255,0.95)",
    bordercolor="#DDE2EC", borderwidth=1,
    font=dict(size=11, color="#334155"),
    itemsizing="constant",
)

# Légende plus compacte pour mobile / tablette
LEGEND_H_MOBILE = dict(
    orientation="h", yanchor="bottom", y=1.02,
    xanchor="left", x=0,
    bgcolor="rgba(255,255,255,0.95)",
    bordercolor="#DDE2EC", borderwidth=1,
    font=dict(size=9, color="#334155"),
    itemsizing="constant",
    tracegroupgap=4,
)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="padding:.3rem 0 .9rem">
        <div style="font-family:'DM Serif Display',serif;font-size:1.2rem;color:#FCD34D">
            Market Pulse
        </div>
        <div style="font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;
                    color:rgba(255,255,255,.35);margin-top:.12rem">
            Tableau de bord financier
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Actifs à afficher")
    available = df.columns.tolist()
    selected = st.multiselect(
        "Sélectionnez un ou plusieurs actifs",
        options=available,
        default=[ASSET_NAMES["^GSPC"], ASSET_NAMES["BTC-USD"], ASSET_NAMES["GC=F"]]
    )

    st.markdown("---")
    st.markdown("### Période")
    min_d = df.index.min().to_pydatetime()
    max_d = df.index.max().to_pydatetime()
    date_range = st.slider(
        "Intervalle d'analyse",
        min_value=min_d, max_value=max_d,
        value=(min_d, max_d), format="MMM YYYY"
    )

    n_actifs = len(selected)
    n_jours  = (date_range[1] - date_range[0]).days
    st.markdown("---")
    st.markdown(f"""
    <div style="background:rgba(253,211,77,.09);border:1px solid rgba(253,211,77,.22);
                border-radius:8px;padding:.8rem 1rem;font-size:.77rem;color:rgba(255,255,255,.72)">
        <div style="color:#FCD34D;font-weight:600;font-size:.68rem;letter-spacing:.1em;
                    text-transform:uppercase;margin-bottom:.45rem">Sélection active</div>
        <div>📊 <b style="color:#fff">{n_actifs}</b> actif{'s' if n_actifs != 1 else ''}</div>
        <div>🗓️ <b style="color:#fff">{n_jours:,}</b> jours d'historique</div>
        <div style="margin-top:.4rem;font-size:.7rem;color:rgba(255,255,255,.36);
                    font-family:'DM Mono',monospace">
            {date_range[0].strftime('%d %b %Y')} → {date_range[1].strftime('%d %b %Y')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# GUARD
# ============================================================
if not selected:
    st.info("Sélectionnez au moins un actif dans le panneau de gauche pour commencer.")
    st.stop()

# ============================================================
# DONNÉES FILTRÉES & CALCULS
# ============================================================
df_f = df.loc[date_range[0]:date_range[1], selected].copy()
df_f = df_f.ffill()

ret = df_f.pct_change().replace([np.inf, -np.inf], np.nan)

ann_return = ret.mean() * 252 * 100
ann_vol    = ret.std().fillna(0) * np.sqrt(252) * 100
sharpe     = (ann_return / ann_vol.replace(0, np.nan)).fillna(0)

rolling_max = df_f.cummax()
drawdown    = ((df_f - rolling_max) / rolling_max).clip(upper=0)
max_dd      = drawdown.min() * 100

yearly_perf = df_f.resample('YE').last().pct_change() * 100

df_norm = pd.DataFrame(index=df_f.index)
for col in selected:
    series = df_f[col].dropna()
    series = series[series > 0]
    if series.empty:
        continue
    base = series.iloc[0]
    normed = (df_f[col] / base) * 100
    normed = normed.clip(upper=100_000)
    df_norm[col] = normed

best_ret_val = ann_return.max()
best_asset   = ann_return.idxmax()
worst_dd_val = max_dd.min()
avg_vol      = ann_vol.mean()
avg_sharpe   = sharpe.mean()

# ============================================================
# DÉTECTION LARGEUR — injecte un tag HTML + JS pour passer
# la largeur du viewport comme query param, sans rechargement forcé.
# Streamlit re-rend de toute façon lors d'une interaction ;
# ici on l'utilise juste pour adapter les hauteurs de graphiques.
# ============================================================
st.markdown("""
<script>
(function(){
    var w = window.innerWidth;
    var url = new URL(window.location.href);
    if(url.searchParams.get('sw') !== String(w)){
        url.searchParams.set('sw', w);
        window.history.replaceState({}, '', url.toString());
    }
})();
</script>
""", unsafe_allow_html=True)

# Hauteurs adaptatives selon la largeur de viewport
try:
    sw = int(st.query_params.get("sw", 1280))
except Exception:
    sw = 1280

MOBILE   = sw < 769
TABLET   = 769 <= sw <= 1024

def chart_h(desktop=430, tablet=370, mobile=300):
    if MOBILE:  return mobile
    if TABLET:  return tablet
    return desktop

def dd_h(n):
    base = max(280, n * 42 + 70)
    if MOBILE: return max(220, n * 36 + 50)
    return base

# ============================================================
# BANNIÈRE
# ============================================================
period_str = f"{date_range[0].strftime('%d %b %Y')} → {date_range[1].strftime('%d %b %Y')}"
st.markdown(f"""
<div class="gmp-banner">
    <div class="eyebrow">Tableau de bord · Marchés mondiaux</div>
    <h1> Market Pulse</h1>
    <span class="badge">
        {period_str}
        &nbsp;·&nbsp; {n_actifs} actif{'s' if n_actifs != 1 else ''}
    </span>
</div>
""", unsafe_allow_html=True)

# ============================================================
# KPI CARDS
# Sur mobile : grille 2×2 en HTML natif (échappe aux colonnes Streamlit).
# Sur desktop/tablette : 4 colonnes Streamlit classiques.
# ============================================================
sign = "+" if best_ret_val >= 0 else ""

KPI_DATA = [
    ("Meilleure performance", f"{sign}{best_ret_val:.1f}%/an", f"↑ {best_asset}", "kgreen", "vg" if best_ret_val >= 0 else "vr"),
    ("Pire chute enregistrée", f"{worst_dd_val:.1f}%", "Perte max sur la période", "kred", "vr"),
    ("Ratio Sharpe moyen", f"{avg_sharpe:.2f}", "Gain pour chaque % de risque pris", "kgold", "vo"),
    ("Volatilité moyenne", f"{avg_vol:.1f}%/an", "Amplitude annuelle des variations", "kteal", "vt"),
]

if MOBILE:
    # Grille HTML 2×2 — indépendante de Streamlit columns
    cards_html = '<div class="kpi-grid-mobile">'
    for label, value, sub, card_cls, val_cls in KPI_DATA:
        cards_html += f"""
        <div class="kpi-card {card_cls}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value {val_cls}">{value}</div>
            <div class="kpi-sub" title="{sub}">{sub}</div>
        </div>"""
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)
else:
    c1, c2, c3, c4 = st.columns(4)
    for col, (label, value, sub, card_cls, val_cls) in zip([c1, c2, c3, c4], KPI_DATA):
        col.markdown(f"""
        <div class="kpi-card {card_cls}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value {val_cls}">{value}</div>
            <div class="kpi-sub" title="{sub}">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:.5rem'></div>", unsafe_allow_html=True)

# ============================================================
# 01 — BASE 100
# ============================================================
st.markdown("""
<div style="margin:1.8rem 0 .35rem">
    <div class="sec-tag">01 · Performance globale</div>
    <div class="sec-title">Si vous aviez investi 100 € au départ…</div>
    <p class="sec-desc">
        Chaque actif est ramené à un point de départ commun de <b>100 €</b>,
        quelle que soit sa valeur réelle. Une courbe à <b>300</b> signifie que
        l'investissement a <b>triplé</b>. Cela permet de comparer des actifs très différents
        (Bitcoin à 67 000 $ vs EUR/USD à 1,08) sur un pied d'égalité.
    </p>
</div>
<hr class="sec-divider">
""", unsafe_allow_html=True)

fig1 = go.Figure()
for i, col in enumerate(df_norm.columns):
    s = df_norm[col].dropna()
    clr = PALETTE[i % len(PALETTE)]
    fig1.add_trace(go.Scatter(
        x=s.index, y=s.values, name=col,
        line=dict(width=2, color=clr),
        hovertemplate=(
            f"<b style='color:{clr}'>{col}</b><br>"
            "%{x|%d %b %Y}<br>"
            "<b>%{y:.1f} €</b> pour 100 € investis<extra></extra>"
        )
    ))

fig1.add_hline(
    y=100, line_dash="dot", line_color="#94A3B8", line_width=1.5,
    annotation_text="Point de départ : 100 €",
    annotation_font=dict(color="#64748B", size=11),
    annotation_position="bottom right",
)

y_max = df_norm.max().max() if not df_norm.empty else 500

fig1.update_layout(
    **base_layout(
        height=chart_h(430, 370, 300),
        yaxis=dict(
            type="linear",
            title="Valeur de votre investissement (€)" if not MOBILE else "Valeur (€)",
            title_font=dict(size=13 if not MOBILE else 11, color="#475569"),
            gridcolor="#E2E8F0", linecolor="#CBD5E1",
            tickfont=dict(size=12 if not MOBILE else 10, color="#475569"),
            zeroline=False,
            range=[0, min(y_max * 1.05, y_max + 200)],
        ),
        xaxis=dict(
            title=None,
            gridcolor="#E2E8F0", linecolor="#CBD5E1",
            tickfont=dict(size=12 if not MOBILE else 10, color="#475569"),
            zeroline=False,
            # Moins de ticks sur mobile
            nticks=6 if MOBILE else 10,
        ),
        legend=LEGEND_H_MOBILE if MOBILE else LEGEND_H,
        margin=dict(l=10, r=10, t=55 if MOBILE else 45, b=35),
    )
)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig1, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# 02 — RISQUE vs RENDEMENT
# ============================================================
st.markdown("""
<div style="margin:1.8rem 0 .35rem">
    <div class="sec-tag">02 · Efficacité</div>
    <div class="sec-title">Quel gain pour quel niveau de risque ?</div>
    <p class="sec-desc">
        Chaque bulle représente un actif. <b>En haut</b> = gain annuel élevé.
        <b>À droite</b> = prix très agités. Le meilleur actif se place <b>en haut à gauche</b>.
    </p>
</div>
<hr class="sec-divider">
""", unsafe_allow_html=True)

st.markdown("""
<div class="glos-row">
    <div class="glos-item">
        <div class="glos-term">Rendement annuel</div>
        <div class="glos-def">Gain ou perte moyen par an, exprimé en %.</div>
    </div>
    <div class="glos-item">
        <div class="glos-term">Volatilité (risque)</div>
        <div class="glos-def">À quel point le prix monte et descend. Plus c'est élevé, plus c'est instable.</div>
    </div>
    <div class="glos-item">
        <div class="glos-term">Ratio Sharpe</div>
        <div class="glos-def">Rendement obtenu pour chaque unité de risque. Plus c'est élevé, mieux c'est.</div>
    </div>
</div>
""", unsafe_allow_html=True)

risk_df = pd.DataFrame({
    "Rendement (%)":  ann_return,
    "Volatilité (%)": ann_vol,
    "Sharpe":         sharpe.fillna(0),
}).dropna(subset=["Rendement (%)"])

fig2 = go.Figure()
for i, (idx, row) in enumerate(risk_df.iterrows()):
    clr  = PALETTE[i % len(PALETTE)]
    # Bulles plus petites sur mobile
    size = max(14 if MOBILE else 16, min(45 if MOBILE else 55,
               abs(row["Rendement (%)"]) * 0.9 + 10))
    fig2.add_trace(go.Scatter(
        x=[row["Volatilité (%)"]],
        y=[row["Rendement (%)"]],
        mode="markers+text",
        name=idx,
        marker=dict(
            size=size, color=clr, opacity=0.82,
            line=dict(width=2, color="white"),
        ),
        text=[idx],
        textposition="top center",
        textfont=dict(size=9 if MOBILE else 11, family="DM Sans", color="#1A2B45"),
        hovertemplate=(
            f"<b style='color:{clr}'>{idx}</b><br>"
            f"Gain moyen : <b>%{{y:.1f}}%/an</b><br>"
            f"Risque : <b>%{{x:.1f}}%</b><br>"
            f"Sharpe : <b>{row['Sharpe']:.2f}</b><extra></extra>"
        )
    ))

fig2.add_hline(
    y=0, line_dash="dash", line_color="#94A3B8", line_width=1.2,
    annotation_text="Seuil zéro",
    annotation_font=dict(color="#94A3B8", size=11),
    annotation_position="bottom right",
)

x_max = risk_df["Volatilité (%)"].max() * 1.18 if not risk_df.empty else 120
y_min = risk_df["Rendement (%)"].min() * 1.2  if risk_df["Rendement (%)"].min() < 0 else -5
y_max2= risk_df["Rendement (%)"].max() * 1.2  if not risk_df.empty else 50

fig2.update_layout(
    **base_layout(
        height=chart_h(420, 360, 310),
        showlegend=False,
        xaxis=dict(
            title="Risque — Volatilité (%)" if not MOBILE else "Volatilité (%)",
            title_font=dict(size=13 if not MOBILE else 11, color="#475569"),
            gridcolor="#E2E8F0", linecolor="#CBD5E1",
            tickfont=dict(size=12 if not MOBILE else 10, color="#475569"),
            zeroline=False,
            range=[0, x_max],
            ticksuffix="%",
        ),
        yaxis=dict(
            title="Gain annuel moyen (%)" if not MOBILE else "Gain/an (%)",
            title_font=dict(size=13 if not MOBILE else 11, color="#475569"),
            gridcolor="#E2E8F0", linecolor="#CBD5E1",
            tickfont=dict(size=12 if not MOBILE else 10, color="#475569"),
            zeroline=False,
            range=[y_min, y_max2],
            ticksuffix="%",
        ),
        margin=dict(l=10, r=10, t=25, b=40 if MOBILE else 40),
    )
)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig2, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# 03 — DRAWDOWN
# Sur mobile : empilement vertical au lieu de 2 colonnes côte à côte
# ============================================================
st.markdown("""
<div style="margin:1.8rem 0 .35rem">
    <div class="sec-tag">03 · Solidité</div>
    <div class="sec-title">Quelle est la pire chute jamais subie ?</div>
    <p class="sec-desc">
        Le <b>drawdown</b> mesure la plus grande perte depuis un sommet.
        −50 % signifie que l'actif a perdu la moitié de sa valeur à un moment donné.
        Plus la barre est courte (proche de zéro), plus l'actif est solide.
    </p>
</div>
<hr class="sec-divider">
""", unsafe_allow_html=True)

sorted_dd  = max_dd.sort_values()
bar_colors = [PALETTE[list(selected).index(c) % len(PALETTE)]
              if c in selected else PALETTE[0] for c in sorted_dd.index]

fig3a = go.Figure(go.Bar(
    x=sorted_dd.values,
    y=sorted_dd.index,
    orientation='h',
    marker=dict(color=bar_colors, opacity=0.85, line=dict(width=0)),
    hovertemplate="<b>%{y}</b><br>Pire chute : <b>%{x:.1f}%</b><extra></extra>",
    text=[f"{v:.1f}%" for v in sorted_dd.values],
    textposition="outside",
    textfont=dict(size=10 if MOBILE else 11, color="#334155"),
))
dd_x_min = min(sorted_dd.min() * 1.25, -5)
fig3a.update_layout(
    **base_layout(
        height=dd_h(len(selected)),
        showlegend=False,
        xaxis=dict(
            title="Chute maximale (%)",
            title_font=dict(size=13 if not MOBILE else 11, color="#475569"),
            gridcolor="#E2E8F0", linecolor="#CBD5E1",
            tickfont=dict(size=12 if not MOBILE else 10, color="#475569"),
            ticksuffix="%", zeroline=True,
            zerolinecolor="#94A3B8", zerolinewidth=1,
            range=[dd_x_min, 2],
        ),
        yaxis=dict(
            gridcolor="rgba(0,0,0,0)", linecolor="#CBD5E1",
            tickfont=dict(size=10 if MOBILE else 11, color="#334155"),
        ),
        margin=dict(l=5, r=55, t=25, b=45),
    )
)

cols3    = selected[:4]
fig3b    = go.Figure()
for i, col in enumerate(cols3):
    clr = PALETTE[selected.index(col) % len(PALETTE)]
    fig3b.add_trace(go.Scatter(
        x=drawdown.index,
        y=(drawdown[col] * 100).round(2),
        name=col, fill="tozeroy",
        line=dict(width=1.8, color=clr),
        fillcolor=hex_to_rgba(clr, 0.12),
        hovertemplate=f"<b style='color:{clr}'>{col}</b><br>%{{x|%d %b %Y}}<br><b>%{{y:.1f}}%</b><extra></extra>",
    ))
fig3b.add_hline(y=0, line_color="#94A3B8", line_width=1)
dd_y_min = (drawdown[cols3].min().min() * 100) * 1.1 if not drawdown[cols3].empty else -100
fig3b.update_layout(
    **base_layout(
        height=dd_h(len(selected)),
        yaxis=dict(
            title="Perte depuis le sommet (%)" if not MOBILE else "Drawdown (%)",
            title_font=dict(size=13 if not MOBILE else 11, color="#475569"),
            gridcolor="#E2E8F0", linecolor="#CBD5E1",
            tickfont=dict(size=12 if not MOBILE else 10, color="#475569"),
            ticksuffix="%", zeroline=False,
            range=[dd_y_min, 5],
        ),
        xaxis=dict(
            gridcolor="#E2E8F0", linecolor="#CBD5E1",
            tickfont=dict(size=12 if not MOBILE else 10, color="#475569"),
            nticks=5 if MOBILE else 8,
        ),
        legend=LEGEND_H_MOBILE if MOBILE else LEGEND_H,
    )
)

if MOBILE:
    # Empilement vertical sur mobile
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig3a, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig3b, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    dd_c1, dd_c2 = st.columns([2, 3])
    with dd_c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig3a, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with dd_c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig3b, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# 04 — SAISONNALITÉ
# ============================================================
st.markdown("""
<div style="margin:1.8rem 0 .35rem">
    <div class="sec-tag">04 · Saisonnalité</div>
    <div class="sec-title">Certains mois sont-ils meilleurs que d'autres ?</div>
    <p class="sec-desc">
        Chaque cellule montre la performance <b>moyenne historique de ce mois</b>,
        calculée sur toutes les années disponibles.
        <span style="color:#15803D;font-weight:600">Vert = mois généralement favorable</span> ·
        <span style="color:#DC2626;font-weight:600">Rouge = mois généralement difficile</span>.
        Rappel : le passé ne garantit pas l'avenir.
    </p>
</div>
<hr class="sec-divider">
""", unsafe_allow_html=True)

monthly_ret = df_f.resample('ME').last().pct_change()
monthly_ret = monthly_ret.replace([np.inf, -np.inf], np.nan)
monthly_ret['__mois__'] = monthly_ret.index.month_name()
months_en = ['January','February','March','April','May','June',
             'July','August','September','October','November','December']
months_fr_full = ['Jan','Fév','Mar','Avr','Mai','Jun',
                  'Jul','Aoû','Sep','Oct','Nov','Déc']
# Abréviations très courtes pour mobile
months_fr_short = ['J','F','M','A','M','J','J','A','S','O','N','D']
months_fr = months_fr_short if MOBILE else months_fr_full

seas = monthly_ret.groupby('__mois__')[selected].mean().reindex(months_en) * 100
seas.index = months_fr
seas = seas.clip(-30, 30)

fig4 = px.imshow(
    seas.T,
    text_auto=".1f",
    color_continuous_scale=[
        [0.0, "#DC2626"],
        [0.35, "#FCA5A5"],
        [0.5,  "#F8FAFC"],
        [0.65, "#86EFAC"],
        [1.0,  "#15803D"],
    ],
    color_continuous_midpoint=0,
    aspect="auto",
    zmin=-15, zmax=15,
)
fig4.update_traces(
    textfont=dict(size=9 if MOBILE else 11, family="DM Mono", color="#1E293B"),
    hovertemplate="<b>%{y}</b> — <b>%{x}</b><br>Perf. moy. : <b>%{z:.1f}%</b><extra></extra>",
)
fig4.update_layout(
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    font=dict(family="DM Sans, sans-serif", color="#334155", size=12),
    height=max(200 if MOBILE else 220, len(selected) * (36 if MOBILE else 44) + 80),
    margin=dict(l=5, r=70 if MOBILE else 100, t=20, b=10),
    coloraxis_colorbar=dict(
        title=dict(text="%" if MOBILE else "Gain moy. (%)",
                   font=dict(size=11 if MOBILE else 12, color="#475569")),
        thickness=10 if MOBILE else 14, len=0.75,
        tickfont=dict(size=9 if MOBILE else 11, family="DM Mono", color="#475569"),
        ticksuffix="%",
    ),
    xaxis=dict(
        side="bottom",
        tickfont=dict(size=10 if MOBILE else 12, color="#334155"),
        linecolor="#CBD5E1", gridcolor="rgba(0,0,0,0)",
        title=None,
    ),
    yaxis=dict(
        tickfont=dict(size=9 if MOBILE else 11, color="#334155"),
        linecolor="#CBD5E1", gridcolor="rgba(0,0,0,0)",
        title=None,
    ),
)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig4, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# 05 — CORRÉLATION
# ============================================================
if len(selected) >= 2:
    st.markdown("""
    <div style="margin:1.8rem 0 .35rem">
        <div class="sec-tag">05 · Diversification</div>
        <div class="sec-title">Ces actifs évoluent-ils ensemble ?</div>
        <p class="sec-desc">
            <b>+1</b> (bleu foncé) : les deux actifs montent et descendent en même temps.
            <b>−1</b> (rouge) : quand l'un monte, l'autre descend.
            <b>0</b> (blanc) : aucun lien. Pour un portefeuille équilibré, favorisez
            des actifs <b>peu corrélés</b> entre eux.
        </p>
    </div>
    <hr class="sec-divider">
    """, unsafe_allow_html=True)

    corr = ret[selected].corr().clip(-1, 1)
    fig5 = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale=[
            [0.0, "#DC2626"],
            [0.5, "#F8FAFC"],
            [1.0, "#1D4ED8"],
        ],
        color_continuous_midpoint=0,
        aspect="auto",
        zmin=-1, zmax=1,
    )
    fig5.update_traces(
        textfont=dict(size=9 if MOBILE else 11, family="DM Mono", color="#1E293B"),
        hovertemplate="<b>%{y}</b> / <b>%{x}</b><br>Corrélation : <b>%{z:.3f}</b><extra></extra>",
    )
    fig5.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="DM Sans, sans-serif", color="#334155", size=12),
        height=max(260 if MOBILE else 300, len(selected) * (44 if MOBILE else 56) + 80),
        margin=dict(l=5, r=70 if MOBILE else 100, t=20, b=10),
        coloraxis_colorbar=dict(
            title=dict(text="Corr." if MOBILE else "Corrélation",
                       font=dict(size=11 if MOBILE else 12, color="#475569")),
            thickness=10 if MOBILE else 14, len=0.75,
            tickfont=dict(size=9 if MOBILE else 11, family="DM Mono", color="#475569"),
            tickvals=[-1, -0.5, 0, 0.5, 1],
        ),
        xaxis=dict(
            tickfont=dict(size=9 if MOBILE else 11, color="#334155"),
            linecolor="#CBD5E1", gridcolor="rgba(0,0,0,0)",
            title=None, tickangle=-35 if MOBILE else -30,
        ),
        yaxis=dict(
            tickfont=dict(size=9 if MOBILE else 11, color="#334155"),
            linecolor="#CBD5E1", gridcolor="rgba(0,0,0,0)",
            title=None,
        ),
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# 06 — HISTORIQUE ANNUEL
# ============================================================
st.markdown("""
<div style="margin:1.8rem 0 .35rem">
    <div class="sec-tag">06 · Historique</div>
    <div class="sec-title">Performances année par année</div>
    <p class="sec-desc">
        Gain ou perte de chaque actif sur une année entière (en %).
        <span style="color:#15803D;font-weight:600">Vert = bonne année</span> ·
        <span style="color:#DC2626;font-weight:600">Rouge = mauvaise année</span>.
    </p>
</div>
<hr class="sec-divider">
""", unsafe_allow_html=True)

yearly_disp = yearly_perf.copy().replace([np.inf, -np.inf], np.nan)
yearly_disp.index = yearly_disp.index.year
yearly_disp = yearly_disp.clip(-200, 500)

st.dataframe(
    yearly_disp.style
        .background_gradient(cmap='RdYlGn', axis=None, vmin=-40, vmax=80)
        .format(lambda v: f"{v:+.1f}%" if pd.notna(v) else "—")
        .set_properties(**{
            'font-family': 'DM Mono, monospace',
            'font-size':   '11px' if MOBILE else '12px',
            'text-align':  'center',
        }),
    use_container_width=True,
    height=min(520, len(yearly_disp) * 38 + 45),
)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div style="margin-top:2.5rem;padding:1.2rem 2rem;background:#1A2B45;
            border-radius:10px;border-top:3px solid #D97706;
            display:flex;justify-content:space-between;align-items:center;
            flex-wrap:wrap;gap:.8rem">
    <div>
        <div style="font-family:'DM Serif Display',serif;color:#FCD34D;font-size:1rem">
            Global Market Pulse
        </div>
        <div style="font-size:.72rem;color:rgba(255,255,255,.35);margin-top:.15rem">
            À titre informatif uniquement · Aucun conseil en investissement
        </div>
    </div>
    <div style="font-size:.7rem;color:rgba(255,255,255,.25);font-family:'DM Mono',monospace">
        Source : Yahoo Finance · ETL interne
    </div>
</div>
<div style="height:1.5rem"></div>
""", unsafe_allow_html=True)