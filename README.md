# SVG-Color-Edit-Script
This Python script allows to show or change the fill color of SVG files.

### Installation:
```bash
pip install -r requirements.txt
```

### Usage:
```bash
python3 script.py --path ./image.svg --pathType file --method change_colors --colors #ed1c24:#000080
```

### Arguments:
- `--path`: Path to the file or directory.
- `--pathType`: Type of the path. It can be `file` or `folder`.
- `--method`: Method to use. It can be `show_colors` or `change_colors`.
- `--colors`: Colors to change. It can be a single color or a list of colors separated by `:`. Example: `#ED1C24:#000080,#FF00FF:#0000FF`.
- `--output`: Path to the output file or directory. If not specified, the output will be saved in the same path as the input file or directory.