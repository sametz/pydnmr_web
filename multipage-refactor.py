"""Refactoring to use urls and multiple page views in order to implement
multiple models.
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go

from model_definitions_remodel import dnmr_two_singlets_kwargs, dnmr_AB_kwargs
from models_remodel import BaseDashModel


app = dash.Dash()
# Demos on the plot.ly Dash site use secret-sauce css:
app.css.append_css(
    {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

dnmr_two_singlets = BaseDashModel(**dnmr_two_singlets_kwargs)
dnmr_AB = BaseDashModel(**dnmr_AB_kwargs)
models = (dnmr_two_singlets, dnmr_AB)
# model_names = [model.name for model in models]
model_dict = {'dnmr-two-singlets': dnmr_two_singlets,
              'dnmr-AB': dnmr_AB}
# active_model = dnmr_two_singlets  # choose one of two models above

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.supress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    # Model toggle
    dcc.RadioItems(
        id='model-select',
        options=[{'label': model.name, 'value': model.name} for model in
                 models],
        value='dnmr-two-singlets'
    ),

    html.Div(id='page-content')
])


# Update the index
@app.callback(dash.dependencies.Output('model-select', 'value'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dnmr-two-singlets':
        return 'dnmr-2s'
    elif pathname == '/dnmr-AB':
        return 'dnmr-AB'
    else:
        return 'dnmr-two-singlets'
    # You could also return a 404 "URL not found" page here


@app.callback(Output('page-content', 'children'),
              [Input('model-select', 'value')])
def display_page(model_key):
    return model_dict[model_key].layout


@app.callback(dnmr_two_singlets.output, dnmr_two_singlets.inputs)
def update_dnmr_two_singlets(*string_values):
    values = (float(i) for i in string_values)
    return dnmr_two_singlets.update_graph(*values)


@app.callback(dnmr_AB.output, dnmr_AB.inputs)
def update_dnmr_AB(*string_values):
    values = (float(i) for i in string_values)
    return dnmr_AB.update_graph(*values)


if __name__ == '__main__':
    app.run_server(debug=True)
