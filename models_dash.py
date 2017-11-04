"""Abstracts a Dash NMR model as a class.

Provides the following class:
*BaseDashModel: creates the layout for a model, and has a method for updating
the plot associated with the model.
 """
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output


class BaseDashModel:
    """Provides calls to the Model for simulation calculations, and the Dash
    layout and routines for creating and updating the GUIl

    Has the following attributes:
    * name: (str) a descriptive name for the model.
    * id: (str) an identifier; also used as a prefix for creating the unique
    component names required for callbacks.
    * model: (function) a reference to the function used to calculate the
    lineshape.
    * entry_names: ([str...]) the names for the Input widgets, listed in left
    to right order.
    * entry_dict: ({str: {**kwargs}}) dict that matches entry name to kwargs
    for Input instantiation.
    * layout: (html.Div) the layout for the model simulation to be added to
    the Dash app.
    * output: (Output) the Output object to be used in Dash callbacks,
    providing the destination for the .update_graph() figure.
    * inputs: ([Input...]) the list of Input objects to be used in Dash
    callbacks.
    """
    def __init__(self, name, id_, model, entry_names, entry_dict):
        self.name = name
        self.id = id_
        self.model = model
        self.entry_names = entry_names
        self.entry_dict = entry_dict

        self._make_toolbar()

        self.layout = html.Div([

            # top toolbar: list of Label/Input paired widgets
            html.Div(id='{}-top-toolbar'.format(self.id),
                     children=self.toolbar),

            # The plot
            dcc.Graph(id='{}-graph'.format(self.id))
        ])

        self.output = Output('{}-graph'.format(self.id), 'figure')
        self.inputs = [Input('{}-{}'.format(self.id, entry), 'value')
                       for entry in self.entry_names]

    def _make_toolbar(self):
        """Create the list of (html.Label, dcc.Input) objects that comprise
        the model's toolbar.

        :return: ([html.Div...])"""
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

    def update_graph(self, *input_values):
        """Update the figure of the Graph.

        :param input_values: (float,)
        :return: (dict) the kwargs for the Graph's figure.
        """
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
    # BROKEN
    import dash
    from model_definitions import dnmr_two_singlets_kwargs

    app = dash.Dash()
    # Demos on the plot.ly Dash site use secret-sauce css:
    app.css.append_css(
        {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

    dnmr_two_singlets = BaseDashModel(**dnmr_two_singlets_kwargs)
    # dnmr_AB = BaseDashModel(**dnmr_AB_kwargs)
    # active_model = dnmr_two_singlets  # choose one of two models above

    app.layout = html.Div(dnmr_two_singlets.layout)


    @app.callback(dnmr_two_singlets.output, dnmr_two_singlets.inputs)
    def update_dnmr_two_singlets(*string_values):
        """Update the figure for the dnmr_two_singlets Graph.

        :param string_values: (str...)
        :return: {**kwargs} for the Graph figure
        """
        values = (float(i) for i in string_values)
        return dnmr_two_singlets.update_graph(*values)

    app.run_server()
