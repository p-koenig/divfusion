# divfusion

`divfusion` takes multiple HTML elements and generates a stand-alone HTML-Report while managing styling and layout.
In practise, these elements ('divs') would originate from other Python modules, especially those that generate plots
and provide a html export (e.g. `plotly`).

If used with plotly, this closes between a single-figure plotly export and a full-fledged plotly-dash server, which
needs to be hosted somewhere. Using this Library, all interactivity of plotly is preserved (hovering, zooming, buttons,
dropdowns, etc.). In addition to that, you can add html-exports of your pd.DataFrames, images or any other HTML content.
`divfusion` brings all of this together and manges the layout and style of the report for you (bring your own css is
possible in a future version).

The resulting html file is completely self-contained and can be opened in any browser on any device.

## Installation

You can install `divfusion` via pip:

```bash
pip install divfusion
```

## Usage

To use `divfusion.Report`, you must first import the class:

```python
from divfusion import Report
```

Next, create a new instance of `Report` by passing the following parameters:

* `title` - The title of the report (string)
* `div_like` - A list of div_like elements. Can be
    * strings
    * plotly figures
    * pandas dataframes
    * pandas series
    * All nested combinations of the above (first dimension is columns, second dimension is rows)
* `css_files` (optional) - The CSS files to include (list)
* `js_files` (optional) - The JS files to include (list)
* `js_libs` (optional) - A list of JS libraries to include (list)

```python
report = Report(title="My Report",
                div_like=[[px.scatter(x=[1, 2, 3], y=[1, 2, 3]), "<div>some text</div>"],
                          ["<div>Some Info Text</div>", "<div>HTML Table</div>"],
                          [pd.DataFrame([[1, 2, 3], [4, 5, 6]]), pd.Series([1, 2, 3])]
                          ])
```
The Elements will be placed as the nested list of divs suggests: Columns horizontally, Rows vertically.
Optionally you can add custom css files, js files or js script tags.

To generate the HTML report, call the `write` method and pass the file path where you want to save the report:

```python
report.write("path/to/report.html")
```

## Dependencies

Currently `divfusion` requires pandas>=1.4.0 and plotly>=5.0.0. Python >= 3.10 is required.

## Future Work

- Add support for custom css
- Provide easy-to-use wrapper functions for adding plotly-figures, pandas-dataframes, etc.

## Contribution

I welcome any and all contributions, no matter what size. Please feel free to open an issue or pull request against dev.

## License

Apache License 2.0
