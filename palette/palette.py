"""
Color palette viewer
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
import importlib
import json
import plistlib
import sys
from types import ModuleType

import palette_converter


DEFAULT_PALETTE = "KaninchenhausDark"
palette_names = [DEFAULT_PALETTE]


class Palette:
    def __init__(self, name: str = DEFAULT_PALETTE):
        with open("./db.json", "r", encoding="utf8") as f:
            db = json.load(f)

        self.name = name
        self.palette = db[name]

    def truecolor_rgb(self, name: str) -> list[int]:
        return self.palette[name]["truecolor"]

    def truecolor(self, name: str) -> str:
        [r, g, b] = self.palette[name]["truecolor"]
        return f"rgb({r},{g},{b})"

    def background_color(self) -> str:
        return self.truecolor("background-color")

    def background_color_rgb(self) -> list[int]:
        return self.truecolor_rgb("background-color")

    def background_color_xterm256(self) -> str:
        return self.xterm256("background-color")

    def xterm256(self, name: str) -> str:
        [r, g, b] = self.palette[name]["xterm256"]["rgb"]
        return f"rgb({r},{g},{b})"


class PaletteView:
    view: ModuleType | None

    def __init__(self):
        self.view = None

    def load_view(self):
        if self.view is None:
            self.view = importlib.import_module("palette_view")
        else:
            self.view = importlib.reload(self.view)

    def render(self, palettes) -> str:
        self.load_view()
        assert self.view is not None
        return self.view.render(palettes)

    def render_theme_preview(self, palettes, mode: str) -> str:
        self.load_view()
        assert self.view is not None
        return self.view.render_theme_preview(palettes, mode)


class PaletteController(BaseHTTPRequestHandler):
    def do_GET(self):
        palettes = [Palette(name) for name in palette_names]

        if self.path == "/":
            body = palette_view.render(palettes)
        elif self.path == "/truecolor":
            body = palette_view.render_theme_preview(palettes, "truecolor")
        elif self.path == "/xterm":
            body = palette_view.render_theme_preview(palettes, "xterm")
        else:
            self.send_error(404)
            return

        body_bytes = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", format(len(body_bytes)))
        self.end_headers()
        self.wfile.write(body_bytes)


PORT: int = 8000
palette_view = PaletteView()

def run():
    """Run a server that serves color platte in HTML"""
    server = HTTPServer(('', PORT), PaletteController)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


def palette_names_from_arg(value: str) -> list[str]:
    return [name.strip() for name in value.split(",") if name.strip()]


def render(names: list[str]):
    print(palette_view.render([Palette(name) for name in names]))


def iterm_colors(name: str):
    colors = palette_converter.ConvertToiTerm2(Palette(name)).generate()
    plistlib.dump(colors, sys.stdout.buffer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--palette",
        default=DEFAULT_PALETTE,
        help="Top-level palette name in db.json. Separate multiple names with commas.",
    )
    parser.add_argument("command", choices=["run", "render", "iterm-colors"])
    args = parser.parse_args()

    palette_names = palette_names_from_arg(args.palette)

    if args.command == "run":
        run()
    elif args.command == "render":
        render(palette_names)
    elif args.command == "iterm-colors":
        if len(palette_names) != 1:
            raise ValueError("iterm-colors supports exactly one palette")
        iterm_colors(palette_names[0])
    else:
        raise ValueError()
