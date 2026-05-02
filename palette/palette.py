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
palette_name = DEFAULT_PALETTE


class Palette:
    def __init__(self, name: str = DEFAULT_PALETTE):
        with open("./db.json", "r", encoding="utf8") as f:
            db = json.load(f)

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

    def render(self, palette) -> str:
        self.load_view()
        assert self.view is not None
        return self.view.render(palette)

    def render_theme_preview(self, palette, mode: str) -> str:
        self.load_view()
        assert self.view is not None
        return self.view.render_theme_preview(palette, mode)


class PaletteController(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            body = palette_view.render(Palette(palette_name))
        elif self.path == "/truecolor":
            body = palette_view.render_theme_preview(Palette(palette_name), "truecolor")
        elif self.path == "/xterm":
            body = palette_view.render_theme_preview(Palette(palette_name), "xterm")
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


def render(name: str):
    print(palette_view.render(Palette(name)))


def iterm_colors(name: str):
    colors = palette_converter.ConvertToiTerm2(Palette(name)).generate()
    plistlib.dump(colors, sys.stdout.buffer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--palette",
        default=DEFAULT_PALETTE,
        help="Top-level palette name in db.json",
    )
    parser.add_argument("command", choices=["run", "render", "iterm-colors"])
    args = parser.parse_args()

    palette_name = args.palette

    if args.command == "run":
        run()
    elif args.command == "render":
        render(args.palette)
    elif args.command == "iterm-colors":
        iterm_colors(args.palette)
    else:
        raise ValueError()
