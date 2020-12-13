# Dash imports
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import dash_table
# General imports


# Local imports
from components.app_style import *
import data





# act_table_cols_new = ['Event date', 'Event type', 'Project', 'EBS', 'System', 'Group', 'Component', 'Status']
# act_table_cols = ['date', 'outage_type', 'projectid',  'responsible_ebs', 'responsible_system', 'responsible_group', 'responsible_component', 'analysis_status']
# act_table = dt.activity_log[act_table_cols]
# act_table.rename(columns=dict(zip(act_table_cols, act_table_cols_new)))

# General functions
def gen_card(children, bg_col=card_col):
    return dbc.Card(dbc.CardBody(children, style={'margin': 0,
                                                  'backgroundColor': bg_col}))


def gap(num):
    return html.Div(style={"height": f"{num}px"})


def gen_table(table_id, col_names):
    table = html.Div([
        dash_table.DataTable(
            id=table_id,
            columns=[{"name": col, "id": col} for col in
                     col_names],
            # data=act_table.to_dict('records'),
            filter_action='custom',
            filter_query='',
            style_filter={'textAlign': 'left',
                          "font-family": font_family
                          },
            fixed_rows={'headers': True, 'data': 0},
            page_size=10,
            style_table={
                'align-self': 'center',
                "verticalAlign": "middle",
                "font-family": font_family,
                "font-size": "14px",
                'marginLeft': 0,
                'marginRight': 25,
            },
            style_data={'whiteSpace': 'pre-line'},
            style_cell={'textAlign': 'left',
                        "verticalAlign": "top",
                        'whiteSpace': 'normal',
                        'textOverflow': 'ellipsis',
                        'maxWidth': '250px',
                        'minWidth': '100px',
                        'height': 'auto',
                        "font-family": font_family,
                        },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': card_col
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': card_col
                }],
            style_header={
                'backgroundColor': even_row_col,
                'border': f'1px solid {table_header_bod_col}',
                'color': header_text_color,
                'fontWeight': 'bold',
                'maxWidth': '250px',
                'minWidth': '100px',
                'whiteSpace': 'normal',
                'height': 'auto',
                "font-size": "16px",
                "font-family": font_family,
            }
        )
    ],
        style={
            'height': 'auto',
            'width': '100%',
            "font-family": font_family,
        },
    )
    return table


# Layout
def serve_layout() -> html.Div():
    appLayout = html.Div([
    html.Div([
        gen_navbar()
    ], style={'height': '75px'}),
    html.Div(
        id='page',
        style=page_style)
    ], style=layout_style)
    return appLayout


def gen_navbar():
    return dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Img(src=encode_image(logo_file), height="60px")),
                # dbc.Col(html.Div(style={'width': '275px'})),
                dbc.Col(dbc.NavbarBrand("",
                                        # className="ml-4",
                                        style={"font-size": "26px",
                                               "font-family": font_family,
                                               'color': card_col}),
                        style={'marginLeft': 50}),

                dbc.Col(html.Div([
                    dcc.Tabs(id='nav_menu', value='fleet', children=[
                        dcc.Tab(
                            label='Fleet',
                            value='fleet',
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label='Project',
                            value='project',
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                    ], style=tabs_styles,
                             persistence=True),

                ], style={'display': 'inline-block', 'width': '250px',
                          "verticalAlign": "middle", 'marginLeft': 20,
                          }), className="ml-4"),

                dbc.Col(
                    html.Div([
                        html.Div(
                            dcc.Dropdown(
                                id='customer_checklist',
                                options=[{'label': p + "            ", 'value': p}
                                         for p in
                                         data.project_list],
                                value=data.project_list[0],
                                style=dropdown_style,
                                clearable=False,
                                persistence=True
                            ),
                            style={
                                "verticalAlign": "center", 'height': '12px',
                                "color": "#02BC94", "text-align": "left",
                                'width': '250px', 'marginBottom': 20,
                            })], id='site_drop_down',
                    ),)
            ],
            align="center",
            no_gutters=True,
        ), ],
        color=nav_bar_color,
        dark=True,
        fixed='top')


def gen_fleet_page():

    return html.Div([
        gap(10),
        html.Div([
            html.Div([
                html.Div([
                    html.Label('Responsible EBS',
                               style=label_style2),
                    html.Br(),
                    dcc.Dropdown(
                        id='responsible_ebs',
                        options=[{'label': r_ebs, 'value': r_ebs} for r_ebs in
                                 data.responsible_ebs],
                        value=data.responsible_ebs[1],
                        clearable=False,
                        style=dropdown_style
                    )
                ], style={'display': 'inline-block', 'width': '23%',
                          'marginLeft': 0, "color": "#02BC94"}),

                html.Div(
                    id='ebs_system',
                    children=[
                        html.Label('Responsible System',
                                   style=label_style2
                                   ),
                        html.Br(),
                        dcc.Dropdown(
                            id='res_sys',
                            clearable=False,
                            style=dropdown_style
                        )
                    ],
                    style={'display': 'inline-block', 'width': '23%',
                           'marginLeft': 30}
                ),
                html.Div(
                    id='ebs_group',
                    children=[
                        html.Label('Responsible Group',
                                   style=label_style2
                                   ),
                        html.Br(),
                        dcc.Dropdown(
                            id='res_grp',

                            clearable=False,
                            style=dropdown_style
                        ), ],
                    style={'display': 'inline-block', 'width': '23%',
                           'marginLeft': 30}
                ),
                html.Div(
                    id='ebs_component',
                    children=[
                        html.Label('Responsible Component',
                                   style=label_style2
                                   ),
                        html.Br(),
                        dcc.Dropdown(
                            id='res_cmp',

                            clearable=False,
                            style=dropdown_style
                        ), ],
                    style={'display': 'inline-block', 'width': '23%',
                           'marginLeft': 30}
                ),
            ],
                style={'float': 'center'},
            ),
        ], style={'width': '100%', 'display': 'inline-block', }),
        html.Br(),
        html.Label('Event distribution',
                   style=label_style2),
        html.Div(
            [
                # Graph MTBT
                dbc.Card(
                    dbc.CardBody(
                        children=html.Div([
                            dcc.Graph(
                                id='home_tab1_ebs_graph',
                                # figure=fig1,
                                style=graph_style1
                            )], )
                    )),
                html.Br(),

                html.Div([
                    html.Label('Event count',
                               style=label_style2),
                ], style={'display': 'inline-block',
                          'float': 'top',
                          }),

                dbc.Card(
                    dbc.CardBody(
                        children=html.Div([
                            dcc.Graph(
                                id='home_tab1_ebs_count_graph',
                                # figure=fig2,
                                style=graph_style1
                            )
                        ], ),
                    ),
                ),

                html.Br(),
            ]
        ),
        html.Div([html.Label("Activity details", style=label_style2)]),
        gen_table('fleet_activity_table', act_table_cols)

    ], style=page_style)


def gen_project_page():
    return html.Div([
        gap(20),
        html.Label("Trip trend", style=label_style2),
        gen_card(html.Div([
            dcc.Graph(
                id="project_trip_graph",
                # figure=fig1
            ),
        ], style={"height": "500px"})),
        gap(20),
        html.Div([
            html.Div([
                html.Label('Top offenders',
                           style=label_style2),
            ], style={'width': '10%', 'display': 'inline-block',
                      "verticalAlign": "middle",
                      "text-align": "left",
                      'marginLeft': 0, }),

            html.Div([
                dcc.RadioItems(
                    id='site_tab1_top_off_radio',
                    options=[{'label': t_off, 'value': t_off} for t_off in
                             top_offenders],
                    value=top_offenders[0],
                    labelStyle=radio_label_style1,
                    style=radio_style1,
                    inputStyle=radio_input_style1,

                ),

            ], style={'width': '25%', 'display': 'inline-block',
                      "verticalAlign": "middle",
                      "color": "#02BC94", "text-align": "left"}),
        ]),
        gen_card(
            html.Div([
                dcc.Graph(
                    id='site_tab1_top_off_graph',
                ),
                html.Div([html.Div(
                    [
                        dbc.Button(html.Img(
                            src=encode_image(next_icon),
                            height=next_icon_height),
                            id='next_button_site',
                            size="sm",
                            style=next_icon_style,
                            n_clicks=1
                        )
                    ], style={'width': '5%',
                              'display': 'inline-block',
                              "verticalAlign": "middle",
                              'float': 'right',
                              "text-align": "left",
                              'marginLeft': 0, 'marginRight': 0,
                              "font-family": font_family}

                ),
                    html.Div(
                        [
                            dbc.Button(html.Img(
                                src=encode_image(previous_icon),
                                height=next_icon_height),
                                id='previous_button_site',
                                size="sm",
                                style=next_icon_style,
                                n_clicks=0,
                            )
                        ], style={'width': '5%',
                                  'display': 'inline-block',
                                  "verticalAlign": "middle",
                                  "text-align": "left",
                                  'float': 'left',
                                  'marginLeft': 30,
                                  "font-family": font_family}

                    )
                ], style={'marginTop': 0, 'float': 'top'}),
                html.Br()
            ]),
        ),
        gap(20),
    ])


def dummy_fig():
    fig = go.Figure()
    # Constants
    img_width = 783
    img_height = 442
    scale_factor = 1

    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
        )
    )

    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )

    fig.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that
        # the aspect ratio stays constant
        scaleanchor="x"
    )

    # Add image
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="fill",
            source=encode_image(default_img_file),
        )
    )
    return fig