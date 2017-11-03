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
    def __init__(self, name, id, model, entry_names, entry_dict):
        self.name = name
        self.id = id
        self.model = model
        self.entry_names = entry_names
        self.entry_dict = entry_dict

        self._make_toolbar()

    def _make_toolbar(self):
        print('entered _make_toolbar for ', self.name)
        self.toolbar = [
            html.Div([
                html.Label(key),

                dcc.Input(
                    id=self.id + '-' + key,
                    type='number',
                    name=key,
                    **self.entry_dict[key])],
                style={'display': 'inline-block', 'textAlign': 'center'})
            for key in self.entry_names]
        print('from within ', self.name, ': ')
        print([self.id + '-' + key for key in self.entry_names])

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
    from model_definitions_remodel import dnmr_two_singlets_kwargs

    app = dash.Dash()
    # Demos on the plot.ly Dash site use secret-sauce css:
    app.css.append_css(
        {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

    dnmr_two_singlets = BaseDashModel(**dnmr_two_singlets_kwargs)
    # dnmr_AB = BaseDashModel(**dnmr_AB_kwargs)
    # active_model = dnmr_two_singlets  # choose one of two models above

    app.layout = html.Div([

        # top toolbar: list of Label/Input paired widgets
        html.Div(id='top-toolbar', children=dnmr_two_singlets.toolbar),

        # The plot
        dcc.Graph(id='test-dnmr-plot')  # figure added by callback
    ])


    @app.callback(
        Output(component_id='test-dnmr-plot', component_property='figure'),
        [Input(component_id=key, component_property='value')
         for key in dnmr_two_singlets.entry_names]
    )
    def update_graph(*input_values):
        """Update the figure of the Graph whenever an Input value is changed.

        :param input_values: (str,) the values of the Input widgets.
        :return: (dict) the kwargs for the Graph's figure.
        """
        # Currently, even when Input type='number', value is a string.
        # A forum discussion indicated this may change at some point
        variables = (float(i) for i in input_values)

        return dnmr_two_singlets.update_graph(*variables)

    app.run_server()
