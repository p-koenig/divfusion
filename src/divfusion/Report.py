#  Copyright (c) Paul Koenig 2023. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ==============================================================================
import pandas as pd
import plotly.graph_objs as go


class Report:
    """
    This is the main class for divfusion.
    It takes a List of Lists of HTML div's and writes them to disk.
    The placement of the div's is traditional C-Style, with columns being added horizontally and rows vertically.
    """

    def __init__(self, title, div_like, css_files=None,
                 js_files=None, js_libs=None):
        """
        Initialize the Report object.
        :param title: The title of the report
        :param div_like: Something that can be converted to a div. Currently supported are:
            - strings
            - pandas.DataFrame
            - pandas.Series
            - plotly.graph_objs.Figure
            - All nested combinations of the above
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
        assert isinstance(div_like, list), "divs must be a List of Lists of strings"
        assert isinstance(css_files, list), "css_files must be a List of strings"
        assert isinstance(js_files, list), "js_files must be a List of strings"
        assert isinstance(js_libs, list), "js_libs must be a List of strings"

        self.title = title
        self.divs = div_like
        self.css_files = css_files
        self.js_files = js_files
        self.js_libs = js_libs

        self.current_div_id = 0

        self.divs = self.check_divs(self.divs)

    def get_new_div_id(self):
        """
        Get a new div id.
        :return: A new div id
        """
        new_id = self.current_div_id + 1
        self.current_div_id += 1
        return new_id

    @staticmethod
    def check_divs(divs: list):
        """
        Format the divs to be used in the report.
        :param divs: A List of Lists of HTML div_like's
        :return: A List of Lists of HTML div_like's
        """

        def check_div(_div: str):
            """
            Format the div to be used in the report.
            :param _div: An HTML div_like
            :return: An HTML div_like
            """
            if not isinstance(_div, (str, go.Figure, pd.DataFrame, pd.Series)):
                raise TypeError(
                    "Elements in div_like can be either strings, go.Figure, pandas DataFrames, "
                    "or pandas Series.")
            return _div

        results = []
        for div in divs:
            if isinstance(div, list):
                results.append(Report.check_divs(div))
            else:
                results.append(check_div(div))
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
        _div_string = self.convert_to_divs(self.divs, True)  # computed before everything else, as convert_to_divs
        # may add css and js files

        html = '<html>\n'
        html += '<head>\n'
        html += '<title>{}</title>\n'.format(self.title)
        html += '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" ' \
                'rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" ' \
                'crossorigin="anonymous">\n'
        html += '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" ' \
                'integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" ' \
                'crossorigin="anonymous"></script>\n'
        for css_file in self.css_files:
            html += '<link rel="stylesheet" href="{}">\n'.format(css_file)
        for js_lib in self.js_libs:
            html += '<script src="{}"></script>\n'.format(js_lib)
        for js_file in self.js_files:
            html += '<script src="{}"></script>\n'.format(js_file)
        html += '</head>\n'
        html += '<body>\n'
        html += _div_string
        html += '</body>\n'
        html += '</html>\n'
        return html

    @staticmethod
    def convert_string_to_div(string: str):
        """
        Converts a string to a div.
        :param string: str
        :return: string: div
        """
        return string  # raw return for now

    def convert_plotly_figure_to_div(self, figure: go.Figure):
        """
        Converts a Figure to a div.
        Adds the plotly.js library to the report if it is not already there.
        :param figure: go.Figure
        :return: string: div
        """
        if "https://cdn.plot.ly/plotly-2.20.0.min.js" not in self.js_libs:
            self.js_libs.append("https://cdn.plot.ly/plotly-2.20.0.min.js")
        return figure.to_html(full_html=False, include_plotlyjs=False, div_id=self.get_new_div_id())

    @staticmethod
    def convert_dataframe_to_div(df: pd.DataFrame):
        """
        Converts a dataframe to a div.
        :param df: pd.DataFrame
        :return: string: div
        """
        return df.to_html()

    @staticmethod
    def convert_series_to_div(ser: pd.Series):
        """
        Converts a series to a div.
        :param ser: pd.Series
        :return: string: div
        """
        return Report.convert_dataframe_to_div(ser.to_frame())

    def convert_to_divs(self, divs, new_container):
        """
        Adds divs recursively to a string and then return this string.
        :param new_container:
        :param divs:
        :return:
        """
        divs_string = ''
        if new_container:
            divs_string += '<div class="container text-center">\n'
        for element in divs:
            if new_container:
                divs_string += '<div class="row">\n'
            else:
                divs_string += f'<div class="col-md-{int(12 / len(divs))}">\n'

            match element:
                case list():
                    divs_string += self.convert_to_divs(element, new_container=(not new_container))
                case str():
                    divs_string += Report.convert_string_to_div(element)
                case go.Figure():
                    divs_string += self.convert_plotly_figure_to_div(element)
                case pd.DataFrame():
                    divs_string += Report.convert_dataframe_to_div(element)
                case pd.Series():
                    divs_string += Report.convert_series_to_div(element)
                case _:  # element is of false type.
                    raise TypeError(f"Elements in div_like can be either strings, go.Figure, pd DataFrames, pd Series."
                                    f"Value provided was of type {type(element)} False type should not be possible. at "
                                    f"this point. Please report this issue on "
                                    f"https://github.com/p-koenig/divfusion/issues.")
            divs_string += '</div>\n'
        if new_container:
            divs_string += '</div>\n'

        return divs_string
