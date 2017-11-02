"""A toolbar will be a list of html.Div objects. Each Div object will be a
collection of widgets, e.g a label and an Input.  The list will be used as
the children of the app's html.Div for the toolbar."""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

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

dnmr_two_singlets = [
    html.Div([
        html.Label(key),

        dcc.Input(
            id=key,
            type='number',
            name=key,
            **entry_dict[key])],
        style={'display': 'inline-block', 'textAlign': 'center'})
    for key in entry_names]
