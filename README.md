# static_html

`static_html` is a Python class that generates an HTML report from a list of HTML divs.

## Installation

You can install `static_html` via pip:

```bash
pip install static_html
```

## Usage

To use `static_html.Report`, you must first import the class:

```python
from static_html import Report
```

Next, create a new instance of `Report` by passing the following parameters:

* `title` - The title of the report (string)
* `divs` - A list of lists of HTML divs (list)
* `css_files` (optional) - The CSS files to use (list)
* `js_files` (optional) - The JS files to use (list)
* `js_libs` (optional) - A list of JS libraries to use (list)

```python
report = Report(title="My Report",
                divs=[["<h1>Heading 1</h1>", "<p>Paragraph 1</p>"], ["<h2>Heading 2</h2>", "<p>Paragraph 2</p>"]])
```

To generate the HTML report, call the `write` method and pass the file path where you want to save the report:

```python
report.write("path/to/report.html")
```

## Example

Here's an example of how to use `static_html.Report`:

```python
from static_html import Report

report = Report(title="My Report",
                divs=[["<h1>Heading 1</h1>", "<p>Paragraph 1</p>"], ["<h2>Heading 2</h2>", "<p>Paragraph 2</p>"]])
report.write("path/to/report.html")
```

This will generate an HTML report with the title "My Report" and two rows of HTML divs. The first row contains a heading
and a paragraph, and the second row contains a subheading and another paragraph. The report will be saved to the file
path specified.