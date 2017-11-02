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

from dnmrplot import dnmrplot_2spin

# list order reflects left-->right order of widgets in top toolbar
entry_names = ['va', 'vb', 'ka', 'wa', 'wb', 'pa']

# each Input widget has the following custom kwargs:
entry_dict = {
    'va': {'value': 165},
    'vb': {'value': 135},
    'ka': {
        'value': 1.5,
        'min': 0.01},
    'wa': {
        'value': 0.5,
        'min': 0.01},
    'wb': {
        'value': 0.5,
        'min': 0.01},
    'pa': {
        'value': 50,
        'min': 0,
        'max': 100}
}

app = dash.Dash()

# Demos on the plot.ly Dash site use secret-sauce css:
app.css.append_css(
    {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.layout = html.Div([

    # top toolbar: list of Label/Input paired widgets
    html.Div([
        html.Div([
            html.Label(key),

            dcc.Input(
                id=key,
                type='number',
                name=key,
                **entry_dict[key])],
            style={'display': 'inline-block', 'textAlign': 'center'})
        for key in entry_names]
    ),

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
    [Input(component_id=key, component_property='value') for key in entry_names]
)
def update_graph(*input_values):
    """Update the figure of the Graph whenever an Input value is changed.

    :param input_values: (str,) the values of the Input widgets.
    :return: (dict) the kwargs for the Graph's figure.
    """
    # Currently, even when Input type='number', value is a string.
    # A forum discussion indicated this may change at some point
    variables = (float(i) for i in input_values)
    x, y = dnmrplot_2spin(*variables)

    return {
        # IMPORTANT: despite what some online examples show, apparently
        # 'data' must be a list, even if only one element. Otherwise, if []
        # omitted, it won't plot.
        'data': [go.Scatter(
            x=x,
            y=y,
            text='banana',
            mode='lines',
            opacity=0.7,
            line={'color': 'blue',
                  'width': 1},
            name='test'
        )],
        'layout': go.Layout(
            xaxis={'title': 'frequency',
                   'autorange': 'reversed'},
            yaxis={'title': 'intensity'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest')
    }


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
