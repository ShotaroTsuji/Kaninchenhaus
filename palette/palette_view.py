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
      <div class="palette-box-caption">{palette.truecolor(color)}</div>
      <div class="palette-box" style="background-color: {palette.truecolor(color)}"></div>
    </div>
    """


def palette_box_xterm256(palette, color: str) -> str:
    return f"""
    <div class="palette-box-container">
      <div class="palette-box-caption">{palette.xterm256(color)}</div>
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


def render_theme_preview(palette, mode: str) -> str:
    background = background_color_value(palette, mode)
    foreground = color_value(palette, "dim-white", mode)
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
        background-color: {background};
        color: {foreground};
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
        color: {foreground};
      }}
      h1 {{
        margin-bottom: 8px;
        font-size: 24px;
        font-weight: 700;
      }}
      p {{
        margin-bottom: 24px;
        color: {foreground};
      }}
      .terminal {{
        border: 1px solid {color_value(palette, "bright-black", mode)};
        padding: 20px;
      }}
      .preview-row {{
        display: grid;
        grid-template-columns: 16ch 1fr;
        gap: 16px;
        min-height: 28px;
        align-items: baseline;
      }}
      .preview-label {{
        color: {color_value(palette, "bright-black", mode)};
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
        <p>Background: {background}</p>
        <div class="terminal">
          {''.join([preview_line(palette, color, mode) for color in COLORS])}
        </div>
      </main>
    </body>
    </html>
    """


def render(palette) -> str:
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
      }}
      .page-nav {{
        width: 260mm;
        margin: 0 auto;
        padding: 1em 0 0;
        display: flex;
        gap: 16px;
      }}
      .page-nav a {{
        color: inherit;
      }}
      div.palettes {{
        width: 260mm;
        margin: auto;
        padding: 1em 0;
        display: grid;
        grid-template-columns: 12.5cm 12.5cm;
        column-gap: 1cm;
      }}
      div.palette-container {{
        display: grid;
        grid-template-columns: 6cm 6cm;
        column-gap: 0.5cm;
        row-gap: 0.25cm;
      }}
      .palette-container-title {{
        font-size: 14pt;
        text-align: center;
      }}
      div.palette-box-container {{
        width: 6cm;
      }}
      div.palette-box {{
        width: 6cm;
        height: 2cm;
      }}
      div.palette-box-caption {{
        text-align: center;
      }}
      </style>
    </head>

    <body style="background-color: {palette.background_color()};">
    {nav_links()}
    <div class="palettes">
      <div class="palette-container-wrapper">
        <h2 class="palette-container-title">TrueColor</h2>
        <div class="palette-container">
          {''.join([palette_box_truecolor(palette, color) for color in COLORS])}
        </div>
      </div>
      <div class="palette-container-wrapper">
        <h2 class="palette-container-title">xterm256</h2>
        <div class="palette-container">
          {''.join([palette_box_xterm256(palette, color) for color in COLORS])}
        </div>
      </div>
    </div>
    </body>
    </html>
    """
