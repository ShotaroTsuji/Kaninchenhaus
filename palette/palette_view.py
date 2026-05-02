import html


COLORS: list[str] = [
    "bright-black",
    "dim-black",
    "bright-red",
    "dim-red",
    "bright-green",
    "dim-green",
    "bright-yellow",
    "dim-yellow",
    "bright-blue",
    "dim-blue",
    "bright-magenta",
    "dim-magenta",
    "bright-cyan",
    "dim-cyan",
    "bright-white",
    "dim-white",
]

SAMPLE_WORDS: list[str] = [
    "Kaninchenhaus",
    "branch",
    "status",
    "commit",
    "warning",
    "success",
    "prompt",
    "selection",
]


def nav_links() -> str:
    return """
    <nav class="page-nav">
      <a href="/">Palette</a>
      <a href="/truecolor">True Color Preview</a>
      <a href="/xterm">xterm256 Preview</a>
    </nav>
    """


def sample_text(color: str) -> str:
    words = " ".join(SAMPLE_WORDS)
    return f"{color:14} $ {words} 0123456789 ./src/theme.py"


def palette_box_truecolor(palette, color: str) -> str:
    return f"""
    <div class="palette-box-container">
      <div class="palette-box-caption">{html.escape(color)}<br>{palette.truecolor(color)}</div>
      <div class="palette-box" style="background-color: {palette.truecolor(color)}"></div>
    </div>
    """


def palette_box_xterm256(palette, color: str) -> str:
    return f"""
    <div class="palette-box-container">
      <div class="palette-box-caption">{html.escape(color)}<br>{palette.xterm256(color)}</div>
      <div class="palette-box" style="background-color: {palette.xterm256(color)}"></div>
    </div>
    """


def color_value(palette, color: str, mode: str) -> str:
    if mode == "truecolor":
        return palette.truecolor(color)
    if mode == "xterm":
        return palette.xterm256(color)
    raise ValueError(f"Unknown color mode: {mode}")


def background_color_value(palette, mode: str) -> str:
    if mode == "truecolor":
        return palette.background_color()
    if mode == "xterm":
        return palette.background_color_xterm256()
    raise ValueError(f"Unknown color mode: {mode}")


def preview_line(palette, color: str, mode: str) -> str:
    value = color_value(palette, color, mode)
    return f"""
      <div class="preview-row">
        <span class="preview-label">{html.escape(color)}</span>
        <span class="preview-text" style="color: {value};">{html.escape(sample_text(color))}</span>
      </div>
    """


def as_palette_list(palettes) -> list:
    if isinstance(palettes, list):
        return palettes
    return [palettes]


def palette_name(palette) -> str:
    return html.escape(getattr(palette, "name", "Palette"))


def theme_preview_panel(palette, mode: str) -> str:
    background = background_color_value(palette, mode)
    foreground = color_value(palette, "dim-white", mode)
    border = color_value(palette, "bright-black", mode)
    muted = color_value(palette, "bright-black", mode)

    return f"""
      <section class="theme-panel" style="background-color: {background}; color: {foreground}; border-color: {border};">
        <div class="theme-panel-header">
          <h2>{palette_name(palette)}</h2>
          <span style="color: {muted};">Background: {background}</span>
        </div>
        <div class="terminal" style="border-color: {border};">
          {''.join([preview_line(palette, color, mode) for color in COLORS])}
        </div>
      </section>
    """


def render_theme_preview(palettes, mode: str) -> str:
    palettes = as_palette_list(palettes)
    title = "True Color Preview" if mode == "truecolor" else "xterm256 Preview"

    return f"""
    <html>
    <head>
      <title>{title}</title>
      <style>
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      body {{
        min-height: 100vh;
        background-color: #ece7dd;
        color: #252525;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 15px;
        line-height: 1.55;
      }}
      main {{
        max-width: 1040px;
        margin: 0 auto;
        padding: 32px;
      }}
      .page-nav {{
        display: flex;
        gap: 16px;
        margin-bottom: 24px;
      }}
      .page-nav a {{
        color: inherit;
      }}
      h1 {{
        margin-bottom: 8px;
        font-size: 24px;
        font-weight: 700;
      }}
      p {{
        margin-bottom: 24px;
        color: #55514b;
      }}
      .theme-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(min(100%, 360px), 1fr));
        gap: 24px;
      }}
      .theme-panel {{
        min-width: 0;
        border: 1px solid;
        padding: 20px;
      }}
      .theme-panel-header {{
        display: flex;
        justify-content: space-between;
        gap: 16px;
        align-items: baseline;
        margin-bottom: 16px;
      }}
      .theme-panel h2 {{
        font-size: 18px;
        font-weight: 700;
      }}
      .theme-panel-header span {{
        font-size: 13px;
      }}
      .terminal {{
        border: 1px solid;
        padding: 20px;
        overflow: auto;
      }}
      .preview-row {{
        display: grid;
        grid-template-columns: 16ch 1fr;
        gap: 16px;
        min-height: 28px;
        align-items: baseline;
      }}
      .preview-label {{
        opacity: 0.78;
      }}
      .preview-text {{
        white-space: pre-wrap;
      }}
      </style>
    </head>

    <body>
      <main>
        {nav_links()}
        <h1>{title}</h1>
        <p>Each theme is rendered against its own terminal background.</p>
        <div class="theme-grid">
          {''.join([theme_preview_panel(palette, mode) for palette in palettes])}
        </div>
      </main>
    </body>
    </html>
    """


def swatch_panel(palette, mode: str) -> str:
    title = "TrueColor" if mode == "truecolor" else "xterm256"
    boxes = (
        [palette_box_truecolor(palette, color) for color in COLORS]
        if mode == "truecolor"
        else [palette_box_xterm256(palette, color) for color in COLORS]
    )

    return f"""
      <section
        class="palette-panel"
        style="
          background-color: {background_color_value(palette, mode)};
          color: {color_value(palette, "dim-white", mode)};
          border-color: {color_value(palette, "bright-black", mode)};
        "
      >
        <div class="palette-panel-header">
          <h2>{palette_name(palette)} {title}</h2>
          <span>{background_color_value(palette, mode)}</span>
        </div>
        <div class="palette-container">
          {''.join(boxes)}
        </div>
      </section>
    """


def render(palettes) -> str:
    palettes = as_palette_list(palettes)
    return f"""
    <html>
    <head>
      <title>Color Palette</title>
      <style>
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      body {{
        width: 100%;
        min-height: 100vh;
        background-color: #ece7dd;
        color: #252525;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 15px;
        line-height: 1.55;
      }}
      .page-nav {{
        max-width: 1040px;
        margin: 0 auto;
        padding: 32px 32px 0;
        display: flex;
        gap: 16px;
      }}
      .page-nav a {{
        color: inherit;
      }}
      div.palettes {{
        max-width: 1040px;
        margin: 0 auto;
        padding: 24px 32px 32px;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(min(100%, 360px), 1fr));
        gap: 24px;
      }}
      .palette-panel {{
        min-width: 0;
        border: 1px solid;
        padding: 20px;
      }}
      .palette-panel-header {{
        display: flex;
        justify-content: space-between;
        gap: 16px;
        align-items: baseline;
        margin-bottom: 16px;
      }}
      .palette-panel-header span {{
        opacity: 0.78;
        font-size: 13px;
      }}
      div.palette-container {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
      }}
      .palette-container-title {{
        margin-bottom: 12px;
        font-size: 24px;
        font-weight: 700;
      }}
      div.palette-box-container {{
        min-width: 0;
      }}
      div.palette-box {{
        width: 100%;
        height: 72px;
      }}
      div.palette-box-caption {{
        margin-bottom: 4px;
        min-height: 48px;
        opacity: 0.86;
      }}
      </style>
    </head>

    <body>
    {nav_links()}
    <div class="palettes">
      {''.join([swatch_panel(palette, "truecolor") for palette in palettes])}
      {''.join([swatch_panel(palette, "xterm") for palette in palettes])}
    </div>
    </body>
    </html>
    """
