"""
Color palette viewer
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import importlib
import json
import plistlib
import sys
from types import ModuleType

import palette_converter


class Palette:
    def __init__(self):
        with open("./db.json", "r", encoding="utf8") as f:
            db = json.load(f)

        self.palette = db["Kaninchenhaus"]

    def truecolor_rgb(self, name: str) -> list[int]:
        return self.palette[name]["truecolor"]

    def truecolor(self, name: str) -> str:
        [r, g, b] = self.palette[name]["truecolor"]
        return f"rgb({r},{g},{b})"

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


class PaletteController(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return

        body = palette_view.render(Palette())

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", format(f"{len(body.encode())}"))
        self.end_headers()
        self.wfile.write(body.encode())


PORT: int = 8000
palette_view = PaletteView()

def run():
    """Run a server that serves color platte in HTML"""
    server = HTTPServer(('', PORT), PaletteController)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


def render():
    print(palette_view.render(Palette()))


def iterm_colors():
    colors = palette_converter.ConvertToiTerm2(Palette()).generate()
    plistlib.dump(colors, sys.stdout.buffer)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run()
    elif sys.argv[1] == "render":
        render()
    elif sys.argv[1] == "iterm-colors":
        iterm_colors()
    else:
        raise ValueError()
