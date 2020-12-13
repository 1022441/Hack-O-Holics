from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go


# General imports
import numpy as np
import pandas as pd

# Local imports
from app import app
import layouts as lyt
import data
from components.app_style import *
from components.utility import *

events = data.activity_log
status_count = data.activity_log_count
act_table_cols_new = ['Event date', 'Event type', 'Project', 'EBS', 'System', 'Group', 'Component', 'Status']
act_table_cols = ['date', 'outage_type', 'projectid',  'responsible_ebs', 'responsible_system', 'responsible_group', 'responsible_component', 'analysis_status']
act_table = events[act_table_cols]
act_table.rename(columns=dict(zip(act_table_cols, act_table_cols_new)), inplace=True)



def get_top_off_gr_data(project_events, event_type, next_click, prev_click):

    top_offender_df = project_events[project_events["outage_type"] == event_type]
    if top_offender_df.empty:
        return lyt.dummy_fig()
    else:
        # y_max = top_offender_df['total'].max()
        annotations = [dict(
            x=0.5,
            y=-0.35,
            showarrow=False,
            text="EBS (System/Group/Component)",
            xref="paper",
            yref="paper",
            font={'size': 14,
                  'family': font_family},
        ),
        ]
        ind = get_group(len(top_offender_df.index), (int(next_click) -
                                                     int(prev_click)),
                        7)
        top_offender_df_mod = top_offender_df[ind[0]:ind[-1] + 1]
        top_offender_df_mod_validated = top_offender_df_mod[top_offender_df_mod["analysis_status"] == "VALIDATED"]
        top_offender_df_mod_tbd = top_offender_df_mod[
            top_offender_df_mod["analysis_status"] == "TBD"]
        top_offender_df_mod_ongoing = top_offender_df_mod[
            top_offender_df_mod["analysis_status"] == "ONGOING"]
        data = [go.Bar(x=top_offender_df_mod_tbd['label'],
                       y=top_offender_df_mod_tbd['status_count'],
                       name='To be started',
                       marker={'color': to_be_started_col},
                       width=0.25,
                       ),
                go.Bar(x=top_offender_df_mod_ongoing['label'],
                       y=top_offender_df_mod_ongoing['status_count'],
                       name='Ongoing',
                       marker={'color': ongoing_col},
                       width=0.25,
                       ),
                go.Bar(x=top_offender_df_mod_validated['label'],
                       y=top_offender_df_mod_validated['status_count'],
                       name='Implemented/Validated',
                       marker={'color': implemented_col},
                       width=0.25,
                       )
                ]

        layout = go.Layout(
            yaxis={'title': {'text': f'Number of {event_type}',
                             'font': {'size': 14,
                                      'family': font_family},
                             },
                   'fixedrange': True,
                   'visible': True,
                   'linecolor': 'black',
                   # 'range': [0, y_max * 1.2],
                   'tickfont': {'size': 12,
                                'family': font_family},
                   'tickformat': ',d'

                   },
            legend=legend_style2,
            annotations=annotations,
            barmode='stack',
            font=dict(
                family=font_family,
                size=12,
                color="black"
            ),
            margin={'r': 50, 't': 40, 'l': 50},
            xaxis={'visible': True,
                   'linecolor': 'black',
                   'tickfont': {'color': 'black',
                                'family': font_family,
                                'size': 12}
                   },
        )


        fig = {
            'data': data,
            'layout': layout,
        }
        return fig


@app.callback([Output('page', 'children'),
               Output('site_drop_down', 'style')],
              [Input('nav_menu', 'value')])
def nav_menu(sel_val):
    if sel_val == 'fleet':
        return lyt.gen_fleet_page(), {"display": "none"}
    else:
        return lyt.gen_project_page(), {}


@app.callback([Output('res_sys', 'options'),
               Output('res_sys', 'value')],
              [Input('responsible_ebs', 'value')])
def responsible_ebs_callback(responsible_ebs_sel):
    responsible_ebs_sel = responsible_ebs_sel.strip()
    mask = events['responsible_ebs'] == responsible_ebs_sel
    ebs_system = events[mask]['responsible_system'].unique()
    # ebs_system = ebs_system[(ebs_system != 'Not defined') & (ebs_system != '')]
    return [{'label': es, 'value': es} for es in ebs_system], ebs_system[0]


@app.callback([Output('res_grp', 'options'),
               Output('res_grp', 'value')],
              [Input('responsible_ebs', 'value'),
               Input('res_sys', 'value')])
def reponsible_sys_callback(responsible_ebs_sel, ebs_system_sel):
    responsible_ebs_sel = responsible_ebs_sel.strip()
    ebs_system_sel = ebs_system_sel.strip()
    mask = (events['responsible_ebs'] == responsible_ebs_sel) & (
                events['responsible_system'] == ebs_system_sel)
    ebs_group = events[mask]['responsible_group'].unique()
    return [{'label': es, 'value': es} for es in ebs_group], ebs_group[0]


@app.callback([Output('res_cmp', 'options'),
               Output('res_cmp', 'value')],
              [Input('responsible_ebs', 'value'),
               Input('res_sys', 'value'),
               Input('res_grp', 'value')])
def reponsible_grp_callback(responsible_ebs_sel, ebs_system_sel,
                            ebs_group_sel):
    responsible_ebs_sel = responsible_ebs_sel.strip()
    ebs_system_sel = ebs_system_sel.strip()
    ebs_group_sel = ebs_group_sel.strip()
    mask = (events['responsible_ebs'] == responsible_ebs_sel) & (
                events['responsible_system'] == ebs_system_sel) & (
                   events['responsible_group'] == ebs_group_sel)
    ebs_components = events[mask]['responsible_component'].unique()
    return [{'label': es, 'value': es} for es in ebs_components], \
           ebs_components[0]



@app.callback(Output('home_tab1_ebs_graph', 'figure'),
              [Input('responsible_ebs', 'value'),
               Input('res_sys', 'value'),
               Input('res_grp', 'value'),
               Input('res_cmp', 'value')])
def home_tab2_ebs_dropdown_callback(responsible_ebs_sel, ebs_system_sel,
                                    ebs_group_sel, ebs_component_sel):
    responsible_ebs_sel = responsible_ebs_sel.strip()
    ebs_system_sel = ebs_system_sel.strip()
    ebs_group_sel = ebs_group_sel.strip()
    ebs_component_sel = ebs_component_sel.strip()
    mask = (events['responsible_ebs'] == responsible_ebs_sel) & (
            events['responsible_system'] == ebs_system_sel) & (
                   events['responsible_group'] == ebs_group_sel) & (
                   events['responsible_component'] == ebs_component_sel)

    df_master_ebs_selcted = events[mask]
    fig1 = px.scatter(df_master_ebs_selcted,
                      x=df_master_ebs_selcted['date'],
                      y=df_master_ebs_selcted['projectid'],
                      symbol='manufacturer',
                      color='outage_type',
                      )
    fig1.update_layout(
        dict1=dict(
            yaxis={
                'title': {'text': 'Projects',
                          'font': {'size': 14,
                                   'family': font_family},
                          },
                'fixedrange': True,
                'visible': True,
                'linecolor': 'black',
                # 'range': [0, y_max * 1.2],
                'tickfont': {'size': 12,
                             'family': font_family},
                'tickformat': ',d'

            },
            # legend=legend_style4,
            # barmode='stack',
            font=dict(
                family=font_family,
                size=10,
                color="black"
            ),
            margin={'r': 50, 't': 40, 'b': 50, 'l': 50},
            xaxis={'visible': True,
                   'title': {'text': 'Event timeline',
                             'font': {'size': 14,
                                      'family': font_family},
                             },
                   'linecolor': 'black',
                   'tickfont': {'color': 'black',
                                'family': font_family,
                                'size': 12}
                   },
            plot_bgcolor='white',

        ),
        overwrite=True
    )
    return fig1


@app.callback(Output('home_tab1_ebs_count_graph', 'figure'),
              [Input('responsible_ebs', 'value'),
               Input('res_sys', 'value'),
               Input('res_grp', 'value'),
               Input('res_cmp', 'value')])
def home_tab2_ebs_radio_callback(responsible_ebs_sel, ebs_system_sel,
                                    ebs_group_sel, ebs_component_sel):

    responsible_ebs_sel = responsible_ebs_sel.strip()
    ebs_system_sel = ebs_system_sel.strip()
    ebs_group_sel = ebs_group_sel.strip()
    ebs_component_sel = ebs_component_sel.strip()

    mask = (events['responsible_ebs'] == responsible_ebs_sel) & (
            events['responsible_system'] == ebs_system_sel) & (
                   events['responsible_group'] == ebs_group_sel) & (
                   events['responsible_component'] == ebs_component_sel)

    df_master_ebs_selcted = events[mask]

    event_count = df_master_ebs_selcted.groupby('projectid').count()
    event_type = df_master_ebs_selcted.groupby('outage_type')
    event_dict = {grp: df.groupby('projectid').count()
                  for grp, df in event_type}
    data = [go.Bar(x=df.index,
                   y=df['outage_type'],
                   opacity=0.5,
                   name=grp,
                   )
            for grp, df in event_dict.items()]
    x_title = "Project"

    y_max = event_count['outage_type'].max()
    fig = {
        'data': data,
        'layout': go.Layout(

            yaxis={'title': {'text': 'Event count',
                             'font': {'size': 14,
                                      'family': font_family},
                             },
                   'fixedrange': True,
                   'visible': True,
                   'linecolor': 'black',
                   'range': [0, y_max * 1.2],
                   'tickfont': {'size': 12,
                                'family': font_family},
                   'tickformat': ',d'

                   },
            legend=legend_style1,
            barmode='stack',
            font=dict(
                family=font_family,
                size=10,
                color="black"
            ),
            margin={'r': 50, 't': 30, 'b': 50, 'l': 50},
            xaxis={'title': {'text': x_title,
                             'font': {'size': 14,
                                      'family': font_family},
                             },
                   'visible': True,
                   'linecolor': 'black',
                   'tickfont': {'color': 'black',
                                'family': font_family,
                                'size': 12}
                   }, )
    }


    return fig


@app.callback(Output('fleet_activity_table', 'data'),
              [Input('fleet_activity_table', 'filter_query'),
               ]
              )
def uer_table_filter_callback(filter_query):
    return update_table(filter_query, act_table)


@app.callback(Output('site_tab1_top_off_graph', 'figure'),
              [Input('customer_checklist', 'value'),
               Input('site_tab1_top_off_radio', 'value'),
               Input('previous_button_site', 'n_clicks'),
               Input('next_button_site', 'n_clicks')])
def site_tab1top_off_drop_callback1(cust_name, ebs_radio_val,
                                    prev_click, next_click):

    project_events = status_count[status_count["projectid"] == cust_name]
    return get_top_off_gr_data(project_events, ebs_radio_val, next_click,
                               prev_click)


@app.callback(Output('project_trip_graph', 'figure'),
              [Input('customer_checklist', 'value')])
def home_tab2_ebs_radio_callback(cust_name):
    project_fired_hours_cols = ["date"] + [col for col in data.fired_hours if cust_name in col]
    project_fired_hours = data.fired_hours[project_fired_hours_cols]
    project_fired_hours['sum'] = project_fired_hours.iloc[:, 1:].sum(axis=1)
    project_fired_hours['cum_sum'] = project_fired_hours['sum'].cumsum()
    project_fired_hours['count'] = range(1,len(project_fired_hours['sum'])+1)
    project_fired_hours['mov_avg'] = project_fired_hours['cum_sum'] / project_fired_hours['count']

    moving_average = pd.merge(data.activity_log, project_fired_hours, on='date', how='right')
    trip_event = moving_average[
        moving_average["outage_type"] == "Trip"]

    fig = {
        'data': [go.Scatter(x=trip_event["date"],
                            y=trip_event["mov_avg"],
                            # mode='lines + markers',
                            mode='lines',
                            # name=f'{cust}',
                            # line={'color': next(color1)},
                            # marker={'size': 8,
                            #         'opacity': 0.5},
                            # text=df['BH_Customer_MTBT_pct'],
                            # hovertemplate="%{text}%",
                            )],

        'layout': go.Layout(
            yaxis={'title': 'Hours',
                   'fixedrange': True,
                   'visible': True,
                   'linecolor': 'black',
                   'rangemode': 'tozero',
                   # 'range': [0, y_max * 1.8],
                   "tickformat": "s"
                   },
            legend=legend_style1,
            font=dict(
                family=font_family,
                size=12,
                color="black"
            ),
            margin={'r': 10, 't': 30, 'b': 40, 'l': 50},
            xaxis=dict(
                # range=[moving_average["date"].min(), moving_average["date"].max()],
                visible=True,
                linecolor="black",
                # rangeselector=dict(
                #     buttons=list([
                #         dict(count=3,
                #              label="3m",
                #              step="month",
                #              stepmode="backward"),
                #         dict(count=6,
                #              label="6m",
                #              step="month",
                #              stepmode="backward"),
                #         dict(count=1,
                #              label="YTD",
                #              step="year",
                #              stepmode="todate"),
                #         dict(count=1,
                #              label="1y",
                #              step="year",
                #              stepmode="backward"),
                #         dict(step="all")
                #     ])
                # ),
                # type="date"
            ))
    }

    return fig
