import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server

card_filters = dbc.Card([
    dbc.Row([
        # Year title
        dbc.Col([
            dbc.Button(
                "Federation:",
                id="federation-target",
                color="info",
                className="me-1",
                n_clicks=0,
                style={'font-family': "Franklin Gothic"},
            ),

        ], align='center', className="d-grid gap-2"),
        # ELO title
        dbc.Col([
            dbc.Button(
                "ELO:",
                id="ELO-target",
                color="info",
                className="me-1",
                n_clicks=0,
                style={'font-family': "Franklin Gothic"},
            ),

        ], align='center', className="d-grid gap-2"),
        # Birth Year title
        dbc.Col([
            dbc.Button(
                "Birth Year:",
                id="BY-target",
                color="info",
                className="me-1",
                n_clicks=0,
                style={'font-family': "Franklin Gothic"},
            ),

        ], align='center', className="d-grid gap-2"),
    ]),

    dbc.Row([
        # Year
        dbc.Col([
            dbc.Spinner(children=[
                dbc.Accordion([
                    dbc.AccordionItem(
                        dcc.Dropdown(id='federation',
                                     options=[],
                                     # value='2',
                                     multi=True,
                                     style={'font-family': "Franklin Gothic"}
                                     ),
                        title=""
                    ),
                ], start_collapsed=True, style={'font-family': "Franklin Gothic"}),
            ], size="lg", color="primary", type="border", fullscreen=True,),
        ]),
        # ELO
        dbc.Col([
            dcc.RangeSlider(min=2608,
                            max=2864,
                            marks={
                                2608: '2608',
                                2650: '2650',
                                2700: '2700',
                                2750: '2750',
                                2800: '2800',
                                2850: '2850',
                            },
                            value=[2608, 2864],
                            allowCross=False,

                            id='ELO-slider')
        ]),
        # Birth Year
        dbc.Col([
            dcc.RangeSlider(min=1965,
                            max=2006,
                            marks={
                                1965: '1965',
                                1975: '1975',
                                1985: '1985',
                                1995: '1995',
                                2006: '2006',
                            },
                            value=[1965, 2006],
                            allowCross=False,
                            id='birth-year-slider')
        ]),



    ]),
])

card_graphs = dbc.Card([
    dbc.Row([
        dbc.Col([
            dbc.Spinner(children=[dcc.Graph(id="fig-bar")], size="lg",
                        color="primary", type="border", fullscreen=True, ),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Spinner(children=[dcc.Graph(id="fig-scatter")], size="lg",
                        color="primary", type="border", fullscreen=True, ),
        ]),
    ]),
])


app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.H5('FIDE Chess Rankings'),style={'color':"", 'font-family': "Franklin Gothic"})
    ]),

    dcc.Tabs([
        dcc.Tab([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
        dbc.CardBody([
            # Filters
            dbc.Row([
                dbc.Col(card_filters),
            ]),
            html.Br(),
            # Graphs
            dbc.Row([
                dbc.Col(card_graphs),
            ]),
            html.Br(),
        ])
    ], color="#2E8BC0"),
                ]),
            ]),
        ], label='Dashboard',),

    ]),


    dbc.Row([
        dbc.Col(html.H6('© 2023 Pingahla'), style={'color': "black", 'font-family': "Franklin Gothic"})
    ]),


])

@app.callback(
    Output('federation', 'options'),
    Output('federation', 'value'),

    Input('federation-target', 'value'),
)

def dropdown_initialization(value_clicks,):
    # Load CSV files
    df = pd.read_csv('Chess_FIDE_Rankings.csv')

    # Gets list of possible values for the dropdowns
    federationDD = df["federation "]
    federationDD = list(dict.fromkeys(federationDD))
    federationDD.sort()


    return federationDD, federationDD


@app.callback(
    Output('fig-bar', "figure"),
    Output('fig-scatter', "figure"),

    Input('federation', 'value'),
    Input('ELO-slider', 'value'),
    Input('birth-year-slider', 'value'),

)

def graphs(federation_value, ELO_value, birth_year_value):

    # Load CSV files
    df = pd.read_csv('Chess_FIDE_Rankings.csv')

    # Filter df by dashboard values
    df = df[df['federation '].isin(federation_value)]
    df = df[(df['ELO '] >= ELO_value[0]) & (df['ELO '] <= ELO_value[1])]
    df = df[(df['birth_year'] >= birth_year_value[0]) & (df['birth_year'] <= birth_year_value[1])]


    # Bar Chart
    df_bar_chart = df.nlargest(10, 'ELO ')
    fig_bar = px.bar(df_bar_chart, x='name ', y='ELO ')

    # Scatter Plot
    fig_scatter = px.scatter(df, x="birth_year", y="ELO ", color='ELO ', hover_data=['name '])

    return fig_bar, fig_scatter


if __name__ == '__main__':
    app.run_server()



