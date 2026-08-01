# ui_theme.py — Shared design token module for CATS Webcamviewer
# Inspired by: Apex Legends HUD  ×  Linear.app  ×  Sports analytics dashboards
# Import this anywhere you need consistent styling.

from app_config import CONFIG

def S(base: float) -> int:
    """Scale a px value by ui_scale."""
    return int(base * CONFIG['ui_scale'])

# ── Palette ───────────────────────────────────────────────────
BG_BASE      = "#07080f"   # deepest background
BG_RAISED    = "#0c0e18"   # panels / cards
BG_SURFACE   = "#111627"   # input fields, secondary surfaces
BG_HOVER     = "#161d2e"   # hover state background

CYAN         = "#00d4ff"   # primary interactive accent
CYAN_DIM     = "#0099bb"   # dimmed cyan
CYAN_DARK    = "#003344"   # very subtle cyan tint

BLUE         = "#3b82f6"   # secondary accent
BLUE_DIM     = "#1d4ed8"

ORANGE       = "#ff7a00"   # recording / energy accent
ORANGE_DIM   = "#cc5f00"
ORANGE_DARK  = "#2a1400"

PURPLE       = "#a78bfa"   # loop markers
PURPLE_DARK  = "#1e1535"

GREEN        = "#22c55e"   # status / success
RED          = "#ef4444"   # danger / clear

TEXT_BRIGHT  = "#f0f4ff"   # headings
TEXT_BODY    = "#94a3b8"   # body text
TEXT_DIM     = "#3d4f66"   # placeholder / disabled
TEXT_MONO    = "#00d4ff"   # readout values (monospace)

BORDER       = "#1a2236"   # default border
BORDER_MID   = "#233047"   # medium border
BORDER_GLOW  = CYAN        # glowing border

FONT_UI      = "'Segoe UI', 'Inter', 'Helvetica Neue', sans-serif"
FONT_MONO    = "'Consolas', 'Courier New', monospace"

# ── Reusable style snippets ────────────────────────────────────

def action_button_style(
    color: str = CYAN,
    bg: str = BG_SURFACE,
    font_size: int = None,
    letter_spacing: int = 2,
) -> str:
    """Action button: outlined, uppercase, accent colour."""
    fs = font_size or S(14)
    return f"""
        QPushButton {{
            background: {bg};
            color: {color};
            font-family: {FONT_UI};
            font-size: {fs}px;
            font-weight: 700;
            letter-spacing: {letter_spacing}px;
            text-transform: uppercase;
            border: 1px solid {color};
            border-bottom: 3px solid {color};
            border-radius: 6px;
            padding: 8px 20px;
        }}
        QPushButton:hover {{
            background: rgba(0,212,255,0.08);
            color: #ffffff;
            border-color: #ffffff;
        }}
        QPushButton:pressed {{
            background: {CYAN_DARK};
        }}
        QPushButton:disabled {{
            color: {TEXT_DIM};
            border-color: {BORDER};
            border-bottom-color: {BORDER};
            background: {BG_RAISED};
        }}
    """

def recording_mode_btn_style(color: str = ORANGE, font_size: int = None) -> str:
    """Large recording-mode action button (DATA PRODUCE / SOURCE CHANGE / AUTO RECORDING)."""
    # Default matches original: int(44 * CONFIG['ui_scale']) = 22px in hospital mode
    fs = font_size or int(44 * CONFIG['ui_scale'])
    return f"""
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {BG_SURFACE}, stop:1 {BG_RAISED});
            color: {color};
            font-family: {FONT_UI};
            font-size: {fs}px;
            font-weight: 800;
            letter-spacing: 3px;
            text-transform: uppercase;
            border: 1px solid {BORDER_MID};
            border-left: 4px solid {color};
            border-radius: 8px;
            padding: 0 24px;
        }}
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #1a1000, stop:1 {BG_RAISED});
            border-left-color: {color};
            border-color: {color};
            color: #ffffff;
        }}
        QPushButton:pressed {{
            background: {ORANGE_DARK};
        }}
        QPushButton:disabled {{
            color: {TEXT_DIM};
            border-left-color: {BORDER};
            border-color: {BORDER};
            background: {BG_RAISED};
        }}
    """

def toolbutton_style() -> str:
    return f"""
        QToolButton {{
            background: {BG_SURFACE};
            border: 1px solid {BORDER_MID};
            border-radius: 8px;
        }}
        QToolButton:hover {{
            border-color: {CYAN};
            background: {CYAN_DARK};
        }}
        QToolButton:pressed {{
            background: #001824;
        }}
        QToolButton:disabled {{
            background: {BG_RAISED};
            border-color: {BORDER};
            opacity: 0.4;
        }}
    """
