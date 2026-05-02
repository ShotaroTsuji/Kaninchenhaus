# Kaninchenhaus

## Palette script usage

The palette scripts read `palette/db.json` and generate palette previews or iTerm2
theme files. Run `palette.py` from the `palette` directory because it reads
`db.json` from the current working directory.

```sh
cd palette
```

By default, `palette.py` uses the `KaninchenhausDark` object in `db.json`. To use
another top-level palette object, pass `--palette`.

```sh
python3 palette.py --palette KaninchenhausDark render
python3 palette.py --palette KaninchenhausLight render
```

### Preview in a browser

Start a local HTTP server for the palette preview.

```sh
python3 palette.py run
```

Then open:

```text
http://localhost:8000/
```

### Render HTML

Print the palette preview HTML to standard output.

```sh
python3 palette.py render
```

To write it to a file:

```sh
python3 palette.py render > palette.html
```

### Generate iTerm2 colors

Print an iTerm2 `.itermcolors` plist to standard output.

```sh
python3 palette.py iterm-colors
```

To update the theme file:

```sh
python3 palette.py --palette KaninchenhausDark iterm-colors > "../themes/Kaninchenhaus Dark.itermcolors"
python3 palette.py --palette KaninchenhausLight iterm-colors > "../themes/Kaninchenhaus Light.itermcolors"
```
