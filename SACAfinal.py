import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import base64

# import data
# Data Input 
math = pd.read_csv('student-mat.csv')
por = pd.read_csv('student-por.csv')

# Data Organizing 
math.reset_index(inplace=True)
por.reset_index(inplace=True)
data1 = math.merge(por, on=["school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu", "Mjob", "Fjob",
                            "reason", "nursery", "internet"])

math['subject'] = ['Math' if item not in data1['index_x'] else 'Math and Portuguese' for item in math.index]
por['subject'] = ['Portuguese' if item not in data1['index_y'] else 'Math and Portuguese' for item in por.index]

data = pd.concat([math, por], ignore_index=True)
data.drop('index', inplace=True, axis=1)

data['healthstats'] = ['Very Bad' if x == 1 else 'Bad' if x == 2 else 'Neutral' \
    if x == 3 else 'Good' if x == 4 else 'Very Good' for x in data['health']]

columns = ['goout', 'studytime', 'freetime', 'failures', 'absences']
columnn = ['Go Out', 'Study Time', 'Free Time', 'Failures', 'Absences']
res = {columns[i]: columnn[i] for i in range(len(columns))}
filterr = ['sex', 'healthstats', 'subject']
filt = ['Sex', 'Health Status', 'Subject']
res2 = {filterr[i]: filt[i] for i in range(len(filterr))}
colors = ['#488f31', '#92b581', '#efe2b5', '#e49967', '#de425b']


color_head = ['#488f31', '#489871', '#70a979', '#94ba83', '#b7ca91', '#d9daa3']
color_head.reverse()
data['Grade'] = (data['G1'] + data['G2'] + data['G3']) / 3
data['GradeDummy'] = [1 if x > data['Grade'].mean() else 0 for x in data['Grade']]

corr = data.corr()

# Marks for Slider
marks = {}
x = list(np.sort(data['age'].unique()))
x.insert(0,data['age'].min()-1)
for age in x:
    if age == data['age'].min()-1:
        marks[str(age)]='All'
    else:
        marks[str(age)]=age

# Start
app = dash.Dash(__name__)

server = app.server
# Change tab style
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '15px',
    "padding-right": "10px",

}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#F9E79F',
    'color': 'black',
    'padding': '15px',
    'fontWeight': 'bold',
    "padding-right": "10px",
    # "width":"82%"
}

app.layout = html.Div([
    html.Div(
        [
            html.H1(children="Student Alcohol Consumption Analysis"),
            html.Br(),
            html.Br(),
            # Introduction
            html.Label(
                '''      Consumption of alcohol by secondary school students is a major public health concern globally. Current and binge drinking remain common among high school students, and many students who binge drink do so at high intensity.  In this dashboard, we explore the alcohol consumption of students, as well as their associations with other variables, including gender, grades, health status, etc, to examine the impact of alcohol consumption among secondary students.

                ''',
                style={"color": "rgb(33 36 35)"},
            ),
            html.Br(),
            html.Br(),
             html.Label(
                '''      The data were obtained in a survey of students' maths and Portuguese language courses in secondary school. 



                ''',
                style={"color": "rgb(33 36 35)"},
            ),
            html.Br(),
            html.Br(),
            # Alcohol image
            html.Img(
                src=app.get_asset_url('alc.png'),
                style={
                    "position": "relative",
                    "width": "100%",
                    "height": "",
                },
            ),
        ],
        className="side_bar", style={
            "width": "18%"
        }
    ),

    html.Div(
        [
            # html.Img(src='./assets/alc_top.png',id='top_img')
            html.H2("Drink Wise", style={"text-align": "center"})
            ,
            dcc.Tabs(value='tab-2-example-graph',children=[
                # Tab one
                dcc.Tab(children=[
                    html.Div([
                        dbc.Card([

                            html.Div([
                                dcc.Graph(id="linechart1",
                                          figure={
                                              'data': [go.Scatter(
                                                  x=data.index, y=data['Dalc'],
                                                  mode='lines', name='Dalc',
                                                  hovertemplate='Dalc: %{y:.2f}' + '<br>Index: %{x}'),
                                                  go.Scatter(x=data.index, y=data['Grade'],
                                                             mode='lines', name='Grade',
                                                             hovertemplate='Grade: %{y:.2f}' + '<br>Index: %{x}'
                                                             )],
                                              'layout': go.Layout(title='Line Charts for Grade with Dalc')
                                          }),
                            ]),
                            html.Div([dcc.Graph(id="linechart2",
                                                figure={
                                                    'data': [go.Scatter(
                                                        x=data.index, y=data['Walc'],
                                                        mode='lines', name='Walc',
                                                        hovertemplate='Walc: %{y:.2f}' + '<br>Index: %{x}'),
                                                        go.Scatter(x=data.index, y=data['Grade'],
                                                                   mode='lines', name='Grade',
                                                                   hovertemplate='Grade: %{y:.2f}' + '<br>Index: %{x}'
                                                                   )],
                                                    'layout': go.Layout(title='Line Charts for Grade with Walc')
                                                })])
                            ,
                            html.Div(
                                [
                                    html.Div([
                                        dbc.CardBody([
                                            html.H6("Count: 1044")
                                        ]
                                        ),
                                        html.Div([
                                            dbc.Card([
                                                dbc.CardBody([
                                                    html.H6("Average DALC Mean: 1.49"),
                                                    html.H6("Average WALC Mean: 2.28")
                                                ])
                                            ]),

                                        ]),
                                        html.Div([
                                            dbc.Card([
                                                dbc.CardBody([
                                                    html.H6("Male: 53%"),
                                                    html.H6("Female: 47%")
                                                ])
                                            ])
                                        ]),
                                        html.Div([dbc.Card([
                                            dbc.CardBody([
                                                html.H6("Math & Portuguese: 71.26%"),
                                                html.H6("Math: 26.34%"),
                                                html.H6("Portuguese: 2.40%")
                                            ])
                                        ])
                                        ]),
                                        html.Div([
                                            dbc.Card([
                                                dbc.CardBody([
                                                    html.H6("Younger than 18: 72.03% "),
                                                    html.H6("Older than 18: 27.97%")
                                                ])
                                            ])
                                        ]),
                                    ],className="box1"),

                                    html.Div([
                                        html.Img(src='./assets/tt2.gif',className="first_box_img")
                                    ],className="first_box_div")

                                ] ,className="first_box"
                            ),
                            html.Div([
                                dcc.Graph(id='heatmap',
                                          figure={
                                              'data': [go.Heatmap(
                                                  colorscale=color_head,
                                                  x=corr.index.values,
                                                  y=corr.columns.values,
                                                  z=corr.values,
                                                  name=''
                                              )],

                                              'layout': go.Layout(title='Correlation Heatmap',
                                                                  xaxis_type='category',
                                                                  yaxis_type='category',
                                                                  plot_bgcolor='White',
                                                                  width=800,
                                                                  height=800)
                                          }
                                          ),
                            ],className="heatmap_box")



                        ])
                    ])

                ],

                    label='Statistic Summary', id="tabxxxx", selected_className="tabxxxx", value='tab-2-example-graph',
                    className="box_comment", style=tab_style, selected_style=tab_selected_style),
                # Tab two
                dcc.Tab(children=[

                    html.Div([


                            dcc.RadioItems(
                                id='hue-type',
                                className="radio data_tab",
                                options=[{'label': res2[i], 'value': i} for i in res2],
                                value='sex',
                                style={"opacity": "80%"}
                            ),



                        html.Div(
                            [

                                html.Div([
                                    html.Img(src="./assets/tt1.gif"),
                                    # html.Img(src="./assets/giphy1.gif")
                                ], className="right-img")
                                ,

                                     html.Div([
                                          dcc.Slider(
                                                id='age-slider',
                                                min=data['age'].min()-1,
                                                max=data['age'].max(),
                                                #value=data['age'].min(),
                                                marks=marks,
                                                step=None
                                                    )
                                     ],className="mysliders box")
                                    ,
                                    dcc.Dropdown(
                                        id='variable-dropdown',
                                        clearable=False,
                                        searchable=False,
                                        options=[{'label': res[i], 'value': i} for i in res],
                                        value='goout',
                                        style={
                                            "box-shadow": "0px 0px #ebb36a",
                                            "border-color": "#ebb36a",
                                            "position": "relative"
                                        }
                                    )

                                ,
                            ],
                            id="right-content"

                        ), html.Div(
                            [
                                dcc.Graph(id='dalc-graph', style={"width": '100%'}),
                                # html.Img(src='./assets/alc_center.png',id='top_img'),
                                dcc.Graph(id='walc-graph', style={})
                            ],
                            id="graph_map"
                        )

                    ], id="tab2_content")

                ], label='Detailed Data', className="box_comment", style=tab_style, selected_style=tab_selected_style),

            ], style={}),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3("Group 1",className=""),
                            html.P("Chiayi Lin, Jessica Xu, Xinde Huang, Zhewen Liu, Muhan Liu, Benjamin Zhao")
                        ]
                    ),
                    html.Div(
                        [
                            html.H3("Sources",className=""),
                            html.A("Kaggle Data Set : Student Alcohol Consumption",href="https://www.kaggle.com/uciml/student-alcohol-consumption",title="Student Alcohol Consumption")
                        ]
                    )
                ]
                ,className='footer'
            )
            ,
        ], id="content_body"
    ),

])


# Layout
# call back
@app.callback(
    Output('dalc-graph', 'figure'),
    Input('variable-dropdown', 'value'),
    Input('hue-type', 'value'),
    Input('age-slider','value'))
def update_figure(variable_name, hue_name,age):
    fig = go.Figure()
    empt = list(data[hue_name].unique())
    for i in range(len(empt)):
        if age not in data['age'].unique():
            data1 = data
        else:
            data1 = data[data['age']==age]
        df = data1[data1[hue_name] == empt[i]].groupby(variable_name).Dalc.mean()

        fig.add_trace(go.Bar(
            x=df.index,
            y=df,
            text=round(df, 2),
            textposition='auto',
            name=empt[i],
            hovertemplate=
            'Daily Alcohol Consumption: %{y:.2f}' +
            '<br>' + res[variable_name] + ' : %{x}',
            marker_color=colors[i]
        ))
    fig.update_layout(title=f'{res[variable_name]} vs. Daily Alcohol Consumption',
                      xaxis_title=f'{res[variable_name]}',
                      yaxis_title='Daily Alcohol Consumption', plot_bgcolor='white')
    return fig


# Weekly Alcohol Consumption Graph

@app.callback(
    Output('walc-graph', 'figure'),
    Input('variable-dropdown', 'value'),
    Input('hue-type', 'value'),
    Input('age-slider','value'))
def update_figure(variable_name, hue_name,age):
    fig = go.Figure()
    empt = list(data[hue_name].unique())
    for i in range(len(empt)):
        if age not in data['age'].unique():
            data1 = data
        else:
            data1 = data[data['age']==age]
        df = data1[data1[hue_name] == empt[i]].groupby(variable_name).Walc.mean()

        fig.add_trace(go.Bar(
            x=df.index,
            y=df,
            text=round(df, 2),
            textposition='auto',
            name=empt[i],
            hovertemplate=
            'Weekly Alcohol Consumption: %{y:.2f}' +
            '<br>' + res[variable_name] + ' : %{x}',
            marker_color=colors[i]

        ))
    fig.update_layout(title=f'{res[variable_name]} vs. Weekly Alcohol Consumption',
                      xaxis_title=f'{res[variable_name]}',
                      yaxis_title='Weekly Alcohol Consumption', plot_bgcolor='white')
    return fig


# End

# app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=True)
