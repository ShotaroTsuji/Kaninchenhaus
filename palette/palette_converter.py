from palette import Palette


def rgb_to_iterm2_rgb(rgb: list[int]) -> dict[str, float | str]:
    [r, g, b] = rgb
    return {
        "Green Component": g / 255.0,
        "Red Component": r / 255.0,
        "Blue Component": b / 255.0,
        "Color Space": "sRGB",
    }


class ConvertToiTerm2:
    palette: Palette

    def __init__(self, palette: Palette):
        self.palette = palette

    def generate(self) -> dict[str, dict[str, float | str]]:
        colors = {
            "Ansi 0 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("dim-black")),
            "Ansi 1 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("dim-red")),
            "Ansi 2 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("dim-green")),
            "Ansi 3 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("dim-yellow")),
            "Ansi 4 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("dim-blue")),
            "Ansi 5 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("dim-magenta")),
            "Ansi 6 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("dim-cyan")),
            "Ansi 7 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("dim-white")),
            "Ansi 8 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("bright-black")),
            "Ansi 9 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("bright-red")),
            "Ansi 10 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("bright-green")),
            "Ansi 11 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("bright-yellow")),
            "Ansi 12 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("bright-blue")),
            "Ansi 13 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("bright-magenta")),
            "Ansi 14 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("bright-cyan")),
            "Ansi 15 Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("bright-white")),
            "Background Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("dim-black")),
            "Foreground Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("dim-white")),
            "Cursor Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("dim-white")),
            "Cursor Text Color": rgb_to_iterm2_rgb(self.palette.truecolor_rgb("bright-white")),
        }
        return colors
