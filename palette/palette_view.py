COLORS: list[str] = [
    "bright-black",
    "dim-black",
    "bright-magenta",
    "dim-magenta",
    "bright-green",
    "dim-green",
    "bright-yellow",
    "dim-yellow",
    "bright-blue",
    "dim-blue",
    "bright-purple",
    "dim-purple",
    "bright-cyan",
    "dim-cyan",
    "bright-white",
    "dim-white",
]

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

    <body style="background-color: rgb(255,255,255);">
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
