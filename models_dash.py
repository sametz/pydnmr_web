"""Concept: each different model's GUI behavior will be contained in a Class.
 The class will have:
 - attributes for the values passed to the model,
 - a method that calls the model and creates a figure for the Graph.
 """
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import json


class BaseDashModel:
    def __init__(self, name, model, entry_names, entry_dict):
        self.name = name
        self.model = model
        self.entry_names = entry_names
        self.entry_dict = entry_dict

        self._make_toolbar()

    def _make_toolbar(self):
        self.toolbar = [
            html.Div([
                html.Label(key),

                dcc.Input(
                    id=key,
                    type='number',
                    name=key,
                    **self.entry_dict[key])],
                style={'display': 'inline-block', 'textAlign': 'center'})
            for key in self.entry_names]

    def update_graph(self, *input_values):
        """Update the figure of the Graph whenever an Input value is changed.

        :param input_values: (float,) the float(values) of the Input widgets.
        :return: (dict) the kwargs for the Graph's figure.
        """
        print('class received input values: ', input_values, ' of type ',
              type(input_values))
        x, y = self.model(*input_values)

        return {
            # IMPORTANT: despite what some online examples show, apparently
            # 'data' must be a list, even if only one element. Otherwise, if []
            # omitted, it won't plot.
            'data': [go.Scatter(
                x=x,
                y=y,
                mode='lines',
                opacity=0.7,
                line={'color': 'blue',
                      'width': 1},
                name=self.name
            )],
            'layout': go.Layout(
                xaxis={'title': 'frequency',
                       'autorange': 'reversed'},
                yaxis={'title': 'intensity'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest')
        }


if __name__ == '__main__':
    import dash
    from dash.dependencies import Input, Output, State
    import numpy as np
    from model_definitions import dnmr_two_singlets_kwargs, dnmr_AB_kwargs

    app = dash.Dash()
    # Demos on the plot.ly Dash site use secret-sauce css:
    app.css.append_css(
        {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

    dnmr_two_singlets = BaseDashModel(**dnmr_two_singlets_kwargs)
    dnmr_AB = BaseDashModel(**dnmr_AB_kwargs)
    models = (dnmr_two_singlets, dnmr_AB)
    model_names = [model.name for model in models]
    model_dict = {'dnmr-two-singlets': dnmr_two_singlets,
              'dnmr-AB': dnmr_AB}
    active_model = dnmr_two_singlets  # choose one of two models above

    app.layout = html.Div([

        # Model toggle
        dcc.RadioItems(
            id='model-select',
            options=[{'label': model.name, 'value': model.name} for model in
                     models],
            value='dnmr-two-singlets'
        ),

        # top toolbar: list of Label/Input paired widgets
        html.Div(id='top-toolbar', children=active_model.toolbar),

        # The plot
        dcc.Graph(id='test-dnmr-plot'),  # figure added by callback


        html.Pre(id='current-model',
                 children='dnmr-two-singlets',
                 style={
                     'border': 'thin lightgrey solid',
                     'overflowX': 'scroll'
                 }),
        # retaining Pre for debugging purposes
        html.Pre(id='selected-data',
                 children='placeholder',
                 style={
                     'border': 'thin lightgrey solid',
                     'overflowX': 'scroll'
                 })
    ])

    @app.callback(
        Output('current-model', 'children'),
        [Input('model-select', 'value')]
    )
    def set_model(selected_model):
        print('set_model entered')
        return selected_model

    @app.callback(
        Output('top-toolbar', 'children'),
        [Input('model-select', 'value')])
    def update_toolbar(model_name):
        print('update toolbar for model named ', model_name)
        selected_model = model_dict[model_name]
        print('selected model named ', selected_model.name)
        # set_model(selected_model)
        # print('active_model is now ', active_model.name)
        # make_input_list()
        return selected_model.toolbar

    # def make_input_list():
    #     input_ = [Input('selected-data', 'children')]
    #     input_.append([Input(component_id=key, component_property='value')
    #                    for key in active_model.entry_names])
        # input_.append(Input(component_id='model-select',
        #                     component_property='value'))
        # # print('input list is now: ', [i.component_id for i in input_])
        # print('input list: ', input_)
        # return input_

    input_list = make_input_list()

    @app.callback(
        Output('selected-data', 'children'),
        [Input('top-toolbar', 'children')]
    )
    def update_data(*args):
        values = []
        print('args: ', args[0])
        print('args length', len(args[0]))
        child_dicts = args[0]
        for child in child_dicts:
            values.append(child['props']['children'][1]['props']['value'])

        print('scraped values', values)
        # return json.dumps(args[0], sort_keys=True, indent=2)
        return json.dumps(values)

    @app.callback(
        Output(component_id='test-dnmr-plot', component_property='figure'),
        # [State('current-model', 'children')],
        # [Input('selected-data', 'children')],
        [Input(component_id=key, component_property='value')
                       for key in active_model.entry_names],
        [State('current-model', 'children')])
    def update_graph(*args):
        """Update the figure of the Graph whenever an Input value is changed.

        :param input_values: (str,) the values of the Input widgets.
        :return: (dict) the kwargs for the Graph's figure.
        """
        input_values_str, model_name, *crap = args

        print('input values: ', input_values_str, ' type ',
              type(input_values_str))
        print('model name: ', model_name)
        input_values = json.loads(input_values_str)
        print('input_values:', input_values, ' type ',
              type(input_values))
        current_model = model_dict[model_name]
        # set_model(current_model)

        # Currently, even when Input type='number', value is a string.
        # A forum discussion indicated this may change at some point
        variables = (float(i) for i in input_values)
        # print('variables: ', *variables)

        return current_model.update_graph(*variables)


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

    app.run_server()
