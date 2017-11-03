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

dnmr_two_singlets.layout = html.Div([

    # top toolbar: list of Label/Input paired widgets
    html.Div(id='dnmr-2s-top-toolbar', children=dnmr_two_singlets.toolbar),

    # The plot
    dcc.Graph(id='dnmr-2s-graph',
              figure=dnmr_two_singlets.update_graph(165, 135, 1.5, 0.5,
                                                      0.5, 50)),

    # retaining a pair of Pre for now in case of json dumps
    html.Pre(id='dnmr-2s-current-model',
             children='dnmr-two-singlets',
             style={
                 'border': 'thin lightgrey solid',
                 'overflowX': 'scroll'
             }),

    html.Pre(id='dnmr-2s-variables',
             children='placeholder',
             style={
                 'border': 'thin lightgrey solid',
                 'overflowX': 'scroll'
             })
])

dnmr_AB.layout = html.Div([

    # top toolbar: list of Label/Input paired widgets
    html.Div(id='dnmr-AB-top-toolbar', children=dnmr_AB.toolbar),

    # The plot
    dcc.Graph(id='dnmr-AB-graph'),

    # retaining a pair of Pre for now in case of json dumps
    html.Pre(id='dnmr-AB-current-model',
             children='dnmr-two-singlets',
             style={
                 'border': 'thin lightgrey solid',
                 'overflowX': 'scroll'
             }),

    html.Pre(id='dnmr-AB-variables',
             children='placeholder',
             style={
                 'border': 'thin lightgrey solid',
                 'overflowX': 'scroll'
             })
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

# @app.callback(
#     Output('current-model', 'children'),
#     [Input('model-select', 'value')]
# )
# def set_model(selected_model):
#     print('set_model entered')
#     return selected_model
#
# @app.callback(
#     Output('top-toolbar', 'children'),
#     [Input('model-select', 'value')])
# def update_toolbar(model_name):
#     print('update toolbar for model named ', model_name)
#     selected_model = model_dict[model_name]
#     print('selected model named ', selected_model.name)
#     # set_model(selected_model)
#     # print('active_model is now ', active_model.name)
#     # make_input_list()
#     return selected_model.toolbar

# def make_input_list():
#     input_ = [Input('selected-data', 'children')]
#     input_.append([Input(component_id=key, component_property='value')
#                    for key in active_model.entry_names])
    # input_.append(Input(component_id='model-select',
    #                     component_property='value'))
    # # print('input list is now: ', [i.component_id for i in input_])
    # print('input list: ', input_)
    # return input_

# input_list = make_input_list()

dnmr_two_singlets.inputs = [
    Input(component_id='dnmr-2s-' + entry, component_property='value')
    for entry in dnmr_two_singlets.entry_names
]
print('checking input ids for 2s:')
print(['dnmr-2s-' + entry for entry in dnmr_two_singlets.entry_names])

dnmr_AB.inputs = [
    Input(component_id='dnmr-AB-' + entry, component_property='value')
    for entry in dnmr_AB.entry_names
]

dnmr_two_singlets.output = Output('dnmr-2s-graph', 'figure')
dnmr_AB.output = Output('dnmr-AB-graph', 'figure')


@app.callback(dnmr_two_singlets.output, dnmr_two_singlets.inputs)
def update_dnmr_two_singlets(*string_values):
    values = (float(i) for i in string_values)

    return dnmr_two_singlets.update_graph(*values)


@app.callback(dnmr_AB.output, dnmr_AB.inputs)
def update_dnmr_AB(*string_values):
    values = (float(i) for i in string_values)

    return dnmr_AB.update_graph(*values)


# @app.callback(
#     Output('selected-data', 'children'),
#     [Input('top-toolbar', 'children')]
# )
# def update_data(*args):
#     values = []
#     print('args: ', args[0])
#     print('args length', len(args[0]))
#     child_dicts = args[0]
#     for child in child_dicts:
#         values.append(child['props']['children'][1]['props']['value'])
#
#     print('scraped values', values)
#     # return json.dumps(args[0], sort_keys=True, indent=2)
#     return json.dumps(values)
#
# @app.callback(
#     Output(component_id='test-dnmr-plot', component_property='figure'),
#     # [State('current-model', 'children')],
#     # [Input('selected-data', 'children')],
#     [Input(component_id=key, component_property='value')
#                    for key in active_model.entry_names],
#     [State('current-model', 'children')])
# def update_graph(*args):
#     """Update the figure of the Graph whenever an Input value is changed.
#
#     :param input_values: (str,) the values of the Input widgets.
#     :return: (dict) the kwargs for the Graph's figure.
#     """
#     input_values_str, model_name, *crap = args
#
#     print('input values: ', input_values_str, ' type ',
#           type(input_values_str))
#     print('model name: ', model_name)
#     input_values = json.loads(input_values_str)
#     print('input_values:', input_values, ' type ',
#           type(input_values))
#     current_model = model_dict[model_name]
#     # set_model(current_model)
#
#     # Currently, even when Input type='number', value is a string.
#     # A forum discussion indicated this may change at some point
#     variables = (float(i) for i in input_values)
#     # print('variables: ', *variables)
#
#     return current_model.update_graph(*variables)
#
#
# # retaining function below temporarily for debugging purposes
# def update_output_div(*input_values):
#
#     # Currently, even when Input type='number', value is a string.
#     # A forum discussion indicated this may change at some point
#     variables = (float(i) for i in input_values)
#     x, y = dnmrplot_2spin(*variables)
#     line1 = 'You\'ve entered "{}"\n'.format(input_values)
#     line2 = 'x = {}...\n'.format(x[:10])
#     line3 = 'y = {}...'.format(y[:10])
#     return line1 + line2 + line3


if __name__ == '__main__':
    app.run_server(debug=True)
