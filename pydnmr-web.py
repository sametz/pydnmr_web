import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

from dnmrplot import dnmrplot_2spin
from testdata import TWOSPIN_SLOW

entry_names = ['va', 'vb', 'ka', 'wa', 'wb', 'pa']
entry_dict = {'va': 165,
              'vb': 135,
              'ka': 1.5,
              'wa': 0.5,
              'wb': 0.5,
              'pa': 50}

app = dash.Dash()

# Demos on the plot.ly Dash site use secret-sauce css:
app.css.append_css(
    {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.layout = html.Div([

    html.Div([
        html.Div([
            html.Label(key),

            dcc.Input(
                id=key,
                type='number',
                name=key,
                value=entry_dict[key])],
            style={'display': 'inline-block', 'textAlign': 'center'})
        for key in entry_names]
    ),

    dcc.Graph(
        id='test-dnmr-plot',
        figure={
            # IMPORTANT: despite what some online examples show, apparently
            # 'data' must be a list, even if only one element. Otherwise, if []
            # omitted, it won't plot.
            'data': [go.Scatter(
                x=TWOSPIN_SLOW[0],
                y=TWOSPIN_SLOW[1],
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
    ),

    html.Pre(id='selected-data',
             style={
                'border': 'thin lightgrey solid',
                'overflowX': 'scroll'
             })
])


@app.callback(
    Output(component_id='selected-data', component_property='children'),
    [Input(component_id=key, component_property='value') for key in entry_names]
)
def update_output_div(*input_values):

    # Currently, even when Input type='number', value is a string.
    # A forum discussion indicated this may change at some point
    variables = (float(i) for i in input_values)
    x, y = dnmrplot_2spin(*variables)
    line1 = 'You\'ve entered "{}"\n'.format(input_values)
    line2 = 'x = {}...\n'.format(x[:10])
    line3 = 'y = {}...'.format(y[:10])
    return line1 + line2 + line3
    # return line2

if __name__ == '__main__':
    app.run_server()
