import streamlit as st

# =========================================================
# THEMES  (add your own: copy a block and change the colors)
# =========================================================
THEMES = {
    "Blurple": dict(
        bg1="#6B77FF", bg2="#5865F2", bg3="#4752C4",
        glow1="rgba(235,69,158,.35)", glow2="rgba(255,255,255,.20)", dot="rgba(255,255,255,.13)",
        title="#FFFFFF", on_bg="#EEF0FF",
        card="#F1F2FF", card_border="rgba(255,255,255,.65)", ink="#23272A", muted="#4E5058",
        accent="#5865F2", accent_hover="#4752C4", accent2="#EB459E", accent2_hover="#D12F87",
        dark_btn="#111214", shadow="rgba(30,35,110,.35)",
        dash_bg="#E0E3FF", dash_card="#FFFFFF", dash_border="#CBD0FF", dash_ink="#23272A",
        sidebar="#5865F2", sidebar_ink="#FFFFFF", input_bg="#FFFFFF", input_ink="#23272A",
    ),
    "Sunset": dict(
        bg1="#FFA45C", bg2="#FF5E62", bg3="#C33764",
        glow1="rgba(255,214,102,.45)", glow2="rgba(255,255,255,.22)", dot="rgba(255,255,255,.14)",
        title="#FFFFFF", on_bg="#FFF1E8",
        card="#FFF5EE", card_border="rgba(255,255,255,.7)", ink="#3A1F2B", muted="#6B4A55",
        accent="#FF5E62", accent_hover="#E04448", accent2="#7B2FF7", accent2_hover="#6322CC",
        dark_btn="#2B1620", shadow="rgba(120,30,60,.38)",
        dash_bg="#FFE8DC", dash_card="#FFFFFF", dash_border="#FFC9B0", dash_ink="#3A1F2B",
        sidebar="#C33764", sidebar_ink="#FFFFFF", input_bg="#FFFFFF", input_ink="#3A1F2B",
    ),
    "Emerald": dict(
        bg1="#34D8A8", bg2="#0F9D77", bg3="#0B6E5A",
        glow1="rgba(255,235,120,.35)", glow2="rgba(255,255,255,.22)", dot="rgba(255,255,255,.14)",
        title="#FFFFFF", on_bg="#E8FFF7",
        card="#EFFFF9", card_border="rgba(255,255,255,.7)", ink="#0F2E27", muted="#3F6A60",
        accent="#0F9D77", accent_hover="#0B7F61", accent2="#FF7A59", accent2_hover="#E85F3E",
        dark_btn="#0B1F1A", shadow="rgba(5,60,48,.40)",
        dash_bg="#D9F7EC", dash_card="#FFFFFF", dash_border="#A8E8D2", dash_ink="#0F2E27",
        sidebar="#0B6E5A", sidebar_ink="#FFFFFF", input_bg="#FFFFFF", input_ink="#0F2E27",
    ),
    "Ocean": dict(
        bg1="#38BDF8", bg2="#0284C7", bg3="#0C4A6E",
        glow1="rgba(125,255,235,.35)", glow2="rgba(255,255,255,.20)", dot="rgba(255,255,255,.14)",
        title="#FFFFFF", on_bg="#E6F6FF",
        card="#EEF8FF", card_border="rgba(255,255,255,.7)", ink="#0B2540", muted="#3E5C76",
        accent="#0284C7", accent_hover="#0369A1", accent2="#F59E0B", accent2_hover="#D97706",
        dark_btn="#0A1A2B", shadow="rgba(6,40,80,.40)",
        dash_bg="#DCEFFD", dash_card="#FFFFFF", dash_border="#B3DBF7", dash_ink="#0B2540",
        sidebar="#0C4A6E", sidebar_ink="#FFFFFF", input_bg="#FFFFFF", input_ink="#0B2540",
    ),
    "Rose Candy": dict(
        bg1="#FF8FC7", bg2="#F0509B", bg3="#A62A6E",
        glow1="rgba(255,236,150,.40)", glow2="rgba(255,255,255,.22)", dot="rgba(255,255,255,.15)",
        title="#FFFFFF", on_bg="#FFEAF5",
        card="#FFF1F8", card_border="rgba(255,255,255,.7)", ink="#3B1130", muted="#6E3F5E",
        accent="#F0509B", accent_hover="#D63A85", accent2="#6C5CE7", accent2_hover="#5546D1",
        dark_btn="#2A0D22", shadow="rgba(100,20,70,.40)",
        dash_bg="#FFE3F1", dash_card="#FFFFFF", dash_border="#FFC2E0", dash_ink="#3B1130",
        sidebar="#A62A6E", sidebar_ink="#FFFFFF", input_bg="#FFFFFF", input_ink="#3B1130",
    ),
    "Midnight Neon": dict(
        bg1="#1B1740", bg2="#11122B", bg3="#07071A",
        glow1="rgba(124,92,255,.40)", glow2="rgba(0,229,255,.22)", dot="rgba(255,255,255,.07)",
        title="#FFFFFF", on_bg="#C9CBF5",
        card="#1C1D3A", card_border="rgba(124,92,255,.55)", ink="#FFFFFF", muted="#B6B8E0",
        accent="#7C5CFF", accent_hover="#6445F0", accent2="#00C2E0", accent2_hover="#00A5BF",
        dark_btn="#2A2B4F", shadow="rgba(0,0,0,.60)",
        dash_bg="#0E0F24", dash_card="#1C1D3A", dash_border="#34366B", dash_ink="#F2F2FF",
        sidebar="#15163A", sidebar_ink="#FFFFFF", input_bg="#252650", input_ink="#FFFFFF",
    ),
}

DEFAULT_THEME = "Blurple"


def get_theme_name():
    name = st.session_state.get("fv_theme", DEFAULT_THEME)
    return name if name in THEMES else DEFAULT_THEME


def theme_picker(container=None):
    """Optional dropdown so users can switch themes live.
    Example: theme_picker(st.sidebar)  -- call BEFORE the style_* functions."""
    box = container or st
    box.selectbox("Theme", list(THEMES), key="fv_theme",
                  index=list(THEMES).index(DEFAULT_THEME))


def _vars():
    t = THEMES[get_theme_name()]
    rows = "".join(f"--fv-{k.replace('_', '-')}:{v};" for k, v in t.items())
    return f":root{{{rows}}}"


def _inject(css):
    st.markdown(f"<style>{_vars()}{css}</style>", unsafe_allow_html=True)


# =========================================================
# HOME PAGE: gradient background + two equal, centered cards
# =========================================================
def style_background_home():
    _inject("""
        .stApp {
            background:
                radial-gradient(circle at 15% 10%, var(--fv-glow1), transparent 40%),
                radial-gradient(circle at 85% 90%, var(--fv-glow2), transparent 45%),
                radial-gradient(var(--fv-dot) 1.5px, transparent 1.5px),
                linear-gradient(160deg, var(--fv-bg1) 0%, var(--fv-bg2) 50%, var(--fv-bg3) 100%) !important;
            background-size: auto, auto, 28px 28px, auto !important;
            overflow-x: hidden;
        }

        .block-container {
            max-width: 1100px !important;
            margin: 0 auto !important;
            padding: 2rem 2rem 3rem !important;
        }

        .stApp [data-testid="stMarkdownContainer"],
        .stApp [data-testid="stCaptionContainer"],
        .stApp [data-testid="stAlert"],
        .stApp label { text-align: center !important; }

        .stApp [data-testid="stImage"],
        .stApp .stButton {
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
        }

        .stApp h1 {
            color: var(--fv-title) !important;
            text-align: center !important;
            text-shadow: 4px 4px 0 var(--fv-accent2);
            overflow-wrap: anywhere;
        }

        .stApp > div p, .stApp label { color: var(--fv-on-bg); }

        /* ---------- Two equal cards ---------- */
        .stApp [data-testid="stHorizontalBlock"] {
            align-items: stretch !important;
            justify-content: center !important;
            gap: 2rem !important;
            flex-wrap: wrap !important;
        }

        .stApp [data-testid="stColumn"],
        .stApp [data-testid="column"] {
            flex: 1 1 320px !important;
            min-width: 0 !important;
            box-sizing: border-box !important;
            background: var(--fv-card) !important;
            padding: 2.5rem 2rem !important;
            border-radius: 2.5rem !important;
            border: 3px solid var(--fv-card-border) !important;
            box-shadow: 0 18px 45px var(--fv-shadow), 0 0 0 8px rgba(255,255,255,.10);
            text-align: center !important;
            transition: transform .3s ease, box-shadow .3s ease;
        }

        @media (hover: hover) {
            .stApp [data-testid="stColumn"]:hover,
            .stApp [data-testid="column"]:hover {
                transform: translateY(-8px);
                box-shadow: 0 26px 55px var(--fv-shadow), 0 0 0 8px rgba(255,255,255,.18);
            }
        }

        .stApp [data-testid="stColumn"] > div,
        .stApp [data-testid="column"] > div {
            height: 100%;
            justify-content: space-between;
            align-items: center;
            text-align: center;
        }

        .stApp [data-testid="stColumn"] h1, .stApp [data-testid="stColumn"] h2,
        .stApp [data-testid="stColumn"] h3, .stApp [data-testid="stColumn"] h4,
        .stApp [data-testid="column"] h1, .stApp [data-testid="column"] h2,
        .stApp [data-testid="column"] h3, .stApp [data-testid="column"] h4 {
            color: var(--fv-ink) !important;
            text-align: center !important;
            text-shadow: none !important;
        }

        .stApp [data-testid="stColumn"] p, .stApp [data-testid="column"] p,
        .stApp [data-testid="stColumn"] label, .stApp [data-testid="column"] label {
            color: var(--fv-muted) !important;
            text-align: center !important;
        }

        .stApp [data-testid="stColumn"] .stButton > button,
        .stApp [data-testid="column"] .stButton > button {
            min-width: 220px;
            max-width: 100%;
            box-shadow: 0 8px 20px var(--fv-shadow) !important;
        }

        /* ---------- Phones ---------- */
        @media (max-width: 640px) {
            .block-container { padding: 1rem .9rem 2rem !important; }

            .stApp h1 {
                font-size: clamp(1.9rem, 10vw, 2.6rem) !important;
                text-shadow: 3px 3px 0 var(--fv-accent2);
            }
            .stApp h2 { font-size: clamp(1.4rem, 7vw, 1.8rem) !important; }

            .stApp [data-testid="stHorizontalBlock"] {
                flex-direction: column !important;
                gap: 1.2rem !important;
            }

            .stApp [data-testid="stColumn"],
            .stApp [data-testid="column"] {
                flex: 1 1 100% !important;
                width: 100% !important;
                min-width: 100% !important;
                padding: 1.6rem 1.2rem !important;
                border-radius: 2rem !important;
                box-shadow: 0 12px 30px var(--fv-shadow), 0 0 0 5px rgba(255,255,255,.10);
            }

            .stApp .stButton > button {
                width: 100% !important;
                min-width: 0 !important;
                min-height: 48px;
                font-size: 1rem !important;
            }
        }
    """)


# =========================================================
# DASHBOARDS
# =========================================================
def style_background_dashboard():
    _inject("""
        .stApp {
            background:
                radial-gradient(circle at 100% 0%, var(--fv-glow1), transparent 38%),
                radial-gradient(circle at 0% 100%, var(--fv-glow2), transparent 38%),
                var(--fv-dash-bg) !important;
        }

        .block-container {
            max-width: 1240px !important;
            padding: 1.5rem 2rem 3rem !important;
        }

        .stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: var(--fv-dash-ink) !important; }
        .stApp p, .stApp label, .stApp li { color: var(--fv-dash-ink); }

        [data-testid="stSidebar"] { background: var(--fv-sidebar) !important; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label { color: var(--fv-sidebar-ink) !important; }

        .stApp [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stMetric"] {
            background: var(--fv-dash-card) !important;
            border: 2px solid var(--fv-dash-border) !important;
            border-radius: 1.5rem !important;
            box-shadow: 0 10px 28px var(--fv-shadow);
        }

        [data-testid="stMetric"] { padding: 1rem 1.2rem; border-radius: 1.2rem !important; }

        [data-testid="stDataFrame"] {
            border: 2px solid var(--fv-dash-border);
            border-radius: 1rem;
            overflow: hidden;
        }

        hr { border-color: var(--fv-dash-border) !important; }

        @media (max-width: 640px) {
            .block-container { padding: 1rem .8rem 2rem !important; }
            .stApp [data-testid="stVerticalBlockBorderWrapper"] { border-radius: 1.2rem !important; }
        }
    """)


# =========================================================
# GLOBAL: fonts, headings, buttons, inputs
# =========================================================
def style_base_layout():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');
        </style>
    """, unsafe_allow_html=True)

    _inject("""
        #MainMenu, footer, header { visibility: hidden; }

        .block-container { padding-top: 1.5rem !important; }

        html, body, [class*="css"], .stApp p, .stApp label, .stApp li {
            font-family: 'Outfit', sans-serif;
        }

        h1 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: clamp(2rem, 9vw, 3.5rem) !important;
            line-height: 1.1 !important;
            margin-bottom: 0 !important;
        }

        h2 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: clamp(1.4rem, 6vw, 2rem) !important;
            line-height: 1 !important;
            margin-bottom: 0 !important;
        }

        h3, h4 { font-family: 'Outfit', sans-serif !important; font-weight: 700 !important; }

        /* Primary */
        .stButton > button, .stFormSubmitButton > button, button[kind="primary"] {
            border-radius: 1.5rem !important;
            background-color: var(--fv-accent) !important;
            color: #FFFFFF !important;
            padding: 10px 24px !important;
            border: none !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
            transition: transform .25s ease-in-out, background-color .25s ease-in-out !important;
        }

        /* Secondary */
        button[kind="secondary"], button[data-testid="stBaseButton-secondary"] {
            background-color: var(--fv-accent2) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 1.5rem !important;
            padding: 10px 24px !important;
        }

        /* Tertiary */
        button[kind="tertiary"], button[data-testid="stBaseButton-tertiary"] {
            background-color: var(--fv-dark-btn) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 1.5rem !important;
            padding: 10px 24px !important;
        }

        button:hover { transform: scale(1.05); }

        .stButton > button:hover, button[kind="primary"]:hover {
            background-color: var(--fv-accent-hover) !important;
        }
        button[kind="secondary"]:hover, button[data-testid="stBaseButton-secondary"]:hover {
            background-color: var(--fv-accent2-hover) !important;
        }

        button p, button:hover p, button:focus p { color: #FFFFFF !important; }

        /* Inputs */
        .stTextInput input, .stNumberInput input, .stTextArea textarea {
            background: var(--fv-input-bg) !important;
            color: var(--fv-input-ink) !important;
            border-radius: 1rem !important;
            border: 2px solid var(--fv-dash-border) !important;
        }

        .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
            border-color: var(--fv-accent) !important;
            box-shadow: 0 0 0 2px var(--fv-accent) !important;
        }

        @media (prefers-reduced-motion: reduce) {
            * { transition: none !important; animation: none !important; }
        }
    """)