"""The main script of the pydnmr_web app.

Currently only provides the model for two uncoupled spins.

TODO: Add the model for two coupled spins.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

# from dnmrplot import dnmrplot_2spin

from model_definitions import dnmr_two_singlets_kwargs, dnmr_AB_kwargs
from models_dash import BaseDashModel


app = dash.Dash()
# Demos on the plot.ly Dash site use secret-sauce css:
app.css.append_css(
    {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

dnmr_two_singlets = BaseDashModel(**dnmr_two_singlets_kwargs)
dnmr_AB = BaseDashModel(**dnmr_AB_kwargs)
active_model = dnmr_two_singlets  # choose one of two models above

app.layout = html.Div([

    # top toolbar: list of Label/Input paired widgets
    html.Div(id='top-toolbar', children=active_model.toolbar),

    # The plot
    dcc.Graph(id='test-dnmr-plot'),  # figure added by callback

    # retaining Pre for debugging purposes
    html.Pre(id='selected-data',
             style={
                'border': 'thin lightgrey solid',
                'overflowX': 'scroll'
             })
])


@app.callback(
    Output(component_id='test-dnmr-plot', component_property='figure'),
    [Input(component_id=key, component_property='value')
     for key in active_model.entry_names]
)
def update_graph(*input_values):
    """Update the figure of the Graph whenever an Input value is changed.

    :param input_values: (str,) the values of the Input widgets.
    :return: (dict) the kwargs for the Graph's figure.
    """
    # Currently, even when Input type='number', value is a string.
    # A forum discussion indicated this may change at some point
    variables = (float(i) for i in input_values)

    return active_model.update_graph(*variables)


# retaining function below temporarily for debugging purposes
def update_output_div(*input_values):

    # Currently, even when Input type='number', value is a string.
    # A forum discussion indicated this may change at some point
    variables = (float(i) for i in input_values)
    x, y = dnmrplot_2spin(*variables)
    line1 = 'You\'ve entered "{}"\n'.format(input_values)
    line2 = 'x = {}...\n'.format(x[:10])
    line3 = 'y = {}...'.format(y[:10])
    return line1 + line2 + line3


if __name__ == '__main__':
    app.run_server()
