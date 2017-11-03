"""Refactoring to use urls and multiple page views in order to implement
multiple models.
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go

from model_definitions import dnmr_two_singlets_kwargs, dnmr_AB_kwargs
from models_dash import BaseDashModel


app = dash.Dash()
# Demos on the plot.ly Dash site use secret-sauce css:
app.css.append_css(
    {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

dnmr_two_singlets = BaseDashModel(**dnmr_two_singlets_kwargs)
dnmr_AB = BaseDashModel(**dnmr_AB_kwargs)
models = (dnmr_two_singlets, dnmr_AB)
model_dict = {'dnmr-two-singlets': dnmr_two_singlets,
              'dnmr-AB': dnmr_AB}

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.supress_callback_exceptions = True

app.layout = html.Div([
    # navbar
    dcc.Location(id='url', refresh=False),

    # Model toggle
    dcc.RadioItems(
        id='model-select',
        options=[{'label': model.name, 'value': model.name} for model in
                 models],
        value='dnmr-two-singlets'
    ),

    # Model-specific content
    html.Div(id='page-content')
])


# Update the index
@app.callback(dash.dependencies.Output('model-select', 'value'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    """Update the current model name when the url changes.

    :return: (str) the name of the selected model
    """
    if pathname == '/dnmr-two-singlets':
        return 'dnmr-two-singlets'
    elif pathname == '/dnmr-AB':
        return 'dnmr-AB'
    else:
        return 'dnmr-two-singlets'
    # You could also return a 404 "URL not found" page here


@app.callback(Output('page-content', 'children'),
              [Input('model-select', 'value')])
def display_page(model_key):
    """Add the new model's layout to the GUI when a new model is selected.

    :return: (html.Div)
    """
    return model_dict[model_key].layout


@app.callback(dnmr_two_singlets.output, dnmr_two_singlets.inputs)
def update_dnmr_two_singlets(*string_values):
    """Update the figure for the dnmr_two_singlets Graph.

    :param string_values: (str...)
    :return: {**kwargs} for the Graph figure
    """
    values = (float(i) for i in string_values)
    return dnmr_two_singlets.update_graph(*values)


@app.callback(dnmr_AB.output, dnmr_AB.inputs)
def update_dnmr_AB(*string_values):
    """Update the figure for the dnmr_AB Graph.

    :param string_values: (str...)
    :return: {**kwargs} for the Graph figure
    """
    values = (float(i) for i in string_values)
    return dnmr_AB.update_graph(*values)


if __name__ == '__main__':
    app.run_server(debug=True)
