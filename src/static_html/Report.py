class Report:
    """
    This is the main class for the static_html.
    It takes a List of Lists of HTML div's and writes them to disk.
    The placement of the div's is traditional C-Style, with columns being added horizontally and rows vertically.
    """

    def __init__(self, title, divs, css_files=None, js_files=None, js_libs=None):
        """
        Initialize the Report object.
        :param title: The title of the report
        :param divs: A List of Lists of HTML div's
        :param css_files: The CSS file to use
        :param js_files: The JS file to use
        :param js_libs: A List of JS libraries to use
        """
        # INPUT DEFAULTS
        if js_libs is None:
            js_libs = []
        if js_files is None:
            js_files = []
        if css_files is None:
            css_files = []

        # INPUT VALIDATION
        assert isinstance(title, str), "title must be a string!"
        assert isinstance(divs, list), "divs must be a List of Lists of strings"
        assert isinstance(css_files, list), "css_files must be a List of strings"
        assert isinstance(js_files, list), "js_files must be a List of strings"
        assert isinstance(js_libs, list), "js_libs must be a List of strings"

        self.title = title
        self.divs = divs
        self.css_files = css_files
        self.js_files = js_files
        self.js_libs = js_libs

    @staticmethod
    def format_divs(divs: list):
        """
        Format the divs to be used in the report.
        :param divs: A List of Lists of HTML div's
        :return: A List of Lists of HTML div's
        """

        def format_div(_div: str):
            """
            Format the div to be used in the report.
            :param _div: An HTML div
            :return: An HTML div
            """
            if not isinstance(_div, str):
                raise TypeError("divs must be a List of Lists of strings (max 2 dimension, but can be only one-dim!")

            # Check whether this is an div tag

            return _div

        results = []
        for div in divs:
            if isinstance(div, list):
                results.append(Report.format_divs(div))
            elif isinstance(div, str):
                results.append(format_div(div))
            else:
                raise TypeError("Divs can only contain strings!")
        return results

    def write(self, output_filepath):
        """
        Write the report to disk.
        """
        html = self._generate_html()
        with open(output_filepath, 'w+') as f:
            f.write(html)

    def _generate_html(self):
        """
        Generate the HTML for the report.
        :return: The HTML for the report
        """
        html = '<html>\n'
        html += '<head>\n'
        html += '<title>{}</title>\n'.format(self.title)
        for css_file in self.css_files:
            html += '<link rel="stylesheet" href="{}">\n'.format(css_file)
        for js_lib in self.js_libs:
            html += '<script src="{}"></script>\n'.format(js_lib)
        for js_file in self.js_files:
            html += '<script src="{}"></script>\n'.format(js_file)
        html += '</head>\n'
        html += '<body>\n'
        html += '<div class="container">\n'
        for row in self.divs:
            html += '<div class="row">\n'
            for div in row:
                html += '<div class="col-md-6">\n'
                html += div
                html += '</div>\n'
            html += '</div>\n'
        html += '</div>\n'
        html += '</body>\n'
        html += '</html>\n'
        return html
