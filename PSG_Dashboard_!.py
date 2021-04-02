import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output
import plotly.graph_objects as go
import pandas as pd
import dash_auth
import schedule
import time

df = pd.read_csv("Book1.csv")
production_rate = pd.read_csv("Production.csv")
print(production_rate.head())

user_login = [['ravirajvarma.iemech97@gmail.com','19MF09']]
app = dash.Dash(__name__, )
auth = dash_auth.BasicAuth(app,user_login)
server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('PSG_LOGO.png'),
                     id = 'PSG-logo',
                     style={'height':'120px',
                            'width':'auto',
                            'margin-bottom':'25px'})

        ],className='one-third column'),

        html.Div([
            html.Div([
                html.H1('PSG INDUSTRIAL MOTORS & PUMPS',style={'margin-bottom':'0px','color':'white'}),
                html.H4('Monitoring Production Rate',style={'margin-bottom':'0px','color':'white'})

            ])

        ],className='one-half column', id = 'title'),

        html.Div([
            html.H6('Last Update: ' + str(production_rate['Date'].iloc[-1]),
                    style={'color':'orange'})
        ],className='one-third column', id = 'title1')


    ],id = 'header',className='row flex-display',style={'margin-bottom':'25px'}),

    html.Div([
        html.Div([
            html.H6(children='Customer Demand',
                    style={'textAlign': ' center',
                           'color': 'white'}),
            html.P(f"{production_rate['Actual Demand'].iloc[-1]:,.0f}",
                   style={'textAlign':'center',
                          'color': '#ff3399',
                          'fontSize':40}),


        ], className='card_container three columns'),

        html.Div([
            html.H6(children='Total Production',
                    style={'textAlign': ' center',
                           'color': 'white'}),
            html.P(f"{production_rate['Total Production'].iloc[-1]:,.0f}",
                   style={'textAlign':'center',
                          'color': '#008000',
                          'fontSize':40}),
            html.P('New: '+f"{production_rate['Total Production'].iloc[-1]- production_rate['Total Production'].iloc[-2]:,.0f}",
                   style={'textAlign':'center',
                          'color':'#008000',
                          'fontSize':15,
                          'margin-bottom': '-18px'})

        ], className='card_container two columns'),

        html.Div([
            html.H6(children='Total Defective Product',
                    style={'textAlign': ' center',
                           'color': 'white'}),
            html.P(f"{production_rate['Total Defects'].iloc[-1]:,.0f}",
                   style={'textAlign':'center',
                          'color': '#FF0000',
                          'fontSize':40}),
            html.P('New: '+f"{production_rate['Total Defects'].iloc[-1]- production_rate['Total Defects'].iloc[-2]:,.0f}",
                   style={'textAlign':'center',
                          'color':'#FF0000',
                          'fontSize':15,
                          'margin-bottom': '-18px'})

        ], className='card_container two columns'),

        html.Div([
            html.H6(children='Products Reworked',
                    style={'textAlign': ' center',
                           'color': 'white'}),
            html.P(f"{production_rate['Products Reworked'].iloc[-1]:,.0f}",
                   style={'textAlign':'center',
                          'color': '#FFFF00',
                          'fontSize':40}),
            html.P('New: '+f"{production_rate['Products Reworked'].iloc[-1]- production_rate['Products Reworked'].iloc[-2]:,.0f}",
                   style={'textAlign':'center',
                          'color':'#FFFF00',
                          'fontSize':15,
                          'margin-bottom': '-18px'})

        ], className='card_container two columns'),

        html.Div([
            html.H6(children='Difference in Demand',
                    style={'textAlign': ' center',
                           'color': 'white'}),
            html.P(f"{production_rate['Demand'].iloc[-1]:,.0f}",
                   style={'textAlign':'center',
                          'color': 'orange',
                          'fontSize':40}),
            html.P('New: '+f"{production_rate['Demand'].iloc[-1]- production_rate['Demand'].iloc[-2]:,.0f}",
                   style={'textAlign':'center',
                          'color':'orange',
                          'fontSize':15,
                          'margin-bottom': '-18px'})

        ], className='card_container three columns')
    ], className= 'row flex display'),

    html.Div([
        html.Div([
            html.P('Select Pump Model:',className='fix_label',style={'color':'white'}),
            dcc.Dropdown(id = 'Pump_Model',
                         multi = False,
                         searchable= True,
                         value='',
                         placeholder='Select Model',
                         options=[{'label':c, 'value':c}
                                  for c in (production_rate['Model'].unique())],className='dcc_compon'),
            html.P('Latest Update: '+' '+ str(production_rate['Date'].iloc[-1]),
                   className='fix_label',style={'text-align':'center','color':'white'}),

            dcc.Graph(id = 'Total Production', config = {'displayModeBar':False},className='dcc_compon',
                      style={'margin-top':'20px'}),

            dcc.Graph(id = 'Total Defects', config = {'displayModeBar':False},className='dcc_compon',
                      style={'margin-top':'20px'}),

            dcc.Graph(id = 'Products Reworked', config = {'displayModeBar':False},className='dcc_compon',
                      style={'margin-top':'20px'})


        ],className='create_container three columns'),

        html.Div([
            dcc.Graph(id = 'pie_chart',config={'displayModeBar':'hover'})

        ],className='create_container four columns'),

        html.Div([
            dcc.Graph(id = 'line_chart',config={'displayModeBar':'hover'})

        ],className='create_container five columns'),
    ],className='row flex-display'),

    html.Div([
        html.Div([
            html.H6(children='Testing Table',
                    className= 'fix_label',
                    style={'textAlign': ' center',
                           'color': 'white'}),
            html.P('Select Pump Model:',className='fix_label',style={'color':'white'}),
            dcc.Dropdown(id = 'Model_Type',
                         multi = False,
                         searchable= True,
                         value='',
                         placeholder='Select Model',
                         options=[{'label':c, 'value':c}
                                  for c in (production_rate['Model'].unique())],className='dcc_compon'),
            dash_table.DataTable(
                id ='datatable_id',
                data = df.to_dict('records'),
                columns = [
                    {"name":i,"id":i,"deletable":False,"selectable":False} for i in df.columns
                ],
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                row_selectable="multi",
                row_deletable=False,
                selected_rows=[],
                page_action="native",
                page_current=0,
                page_size=8,
                style_cell= {
                    'minWidth':95,'maxWidth':95,'width':95
                },
            )
        ],className='create_container ten columns')
    ],className='row flex-display')

], id = 'mainContainer',style={'display':'flex','flex-direction':'column'})

@app.callback(Output('Total Production','figure'),
              [Input('Pump_Model','value')])

def update_production(Pump_Model):
    latest_update = production_rate['Total Production'].iloc[-1]- production_rate['Total Production'].iloc[-2]
    delta_update = production_rate['Total Production'].iloc[-2]- production_rate['Total Production'].iloc[-3]

    return{
        'data':[go.Indicator(
            mode = 'number+delta',
            value = latest_update,
            delta = {'reference':delta_update,
                     'position': 'right',
                     'valueformat':'g',
                     'relative':False,
                     'font':{'size':15}},

            number = {'valueformat':',',
                      'font':{'size':20}},

            domain = {'y':[0,1],'x':[0,1]}
        )],

        'layout':go.Layout(
            title = {'text':'New Arrival',
                     'y':1,
                     'x':0.5,
                     'xanchor':'center',
                     'yanchor':'top'},

            font = dict(color = '#008000'),
            paper_bgcolor= '#1f2c56',
            plot_bgcolor= '#1f2c56',
            height=50,
        )
    }

@app.callback(Output('Total Defects','figure'),
              [Input('Pump_Model','value')])

def update_production(Pump_Model):
    latest_update = production_rate['Total Defects'].iloc[-1]- production_rate['Total Defects'].iloc[-2]
    delta_update = production_rate['Total Defects'].iloc[-2]- production_rate['Total Defects'].iloc[-3]

    return{
        'data':[go.Indicator(
            mode = 'number+delta',
            value = latest_update,
            delta = {'reference':delta_update,
                     'position': 'right',
                     'valueformat':'g',
                     'relative':False,
                     'font':{'size':15}},

            number = {'valueformat':',',
                      'font':{'size':20}},

            domain = {'y':[0,1],'x':[0,1]}
        )],

        'layout':go.Layout(
            title = {'text':'Defects',
                     'y':1,
                     'x':0.5,
                     'xanchor':'center',
                     'yanchor':'top'},

            font = dict(color = '#FF0000'),
            paper_bgcolor= '#1f2c56',
            plot_bgcolor= '#1f2c56',
            height=50,
        )
    }

@app.callback(Output('Products Reworked','figure'),
              [Input('Pump_Model','value')])

def update_production(Pump_Model):
    latest_update = production_rate['Products Reworked'].iloc[-1]- production_rate['Products Reworked'].iloc[-2]
    delta_update = production_rate['Products Reworked'].iloc[-2]- production_rate['Products Reworked'].iloc[-3]

    return{
        'data':[go.Indicator(
            mode = 'number+delta',
            value = latest_update,
            delta = {'reference':delta_update,
                     'position': 'right',
                     'valueformat':'g',
                     'relative':False,
                     'font':{'size':15}},

            number = {'valueformat':',',
                      'font':{'size':20}},

            domain = {'y':[0,1],'x':[0,1]}
        )],

        'layout':go.Layout(
            title = {'text':'Reworked',
                     'y':1,
                     'x':0.5,
                     'xanchor':'center',
                     'yanchor':'top'},

            font = dict(color = '#FFFF00'),
            paper_bgcolor= '#1f2c56',
            plot_bgcolor= '#1f2c56',
            height=50,
        )
    }

@app.callback(Output('pie_chart','figure'),
              [Input('Pump_Model','value')])

def update_graph(Pump_Model):
    TotalProduction_update = production_rate['Total Production'].iloc[-1]
    TotalDefects_update = production_rate['Total Defects'].iloc[-1]
    colors = ['green','red']

    return{
        'data':[go.Pie(
            labels=['Total Production','Total Defects'],
            values=[TotalProduction_update,TotalDefects_update],
            marker = dict(colors = colors),
            hoverinfo='label+value+percent',
            textinfo= 'label+value',
            hole = .7

        )],

        'layout':go.Layout(
            title = {'text':'Total_production:'+(Pump_Model),
                     'y':1,
                     'x':0.5,
                     'xanchor':'center',
                     'yanchor':'top'},
            titlefont = {'color':'white',
                         'size':20},
            font=dict(family = 'sans-serif',
                      color = 'white',
                      size = 12),
            hovermode= 'closest',
            paper_bgcolor= '#1f2c56',
            plot_bgcolor= '#1f2c56',
            legend={'orientation':'h',
                    'bgcolor':'#1f2c56',
                    'xanchor':'center','x':0.5,'y':-0.7}
        )
    }

@app.callback(Output('line_chart','figure'),
              [Input('Pump_Model','value')])

def update_graph(Pump_Model):
    Daily_update = pd.read_csv("Production.csv")
    return{
        'data':[go.Bar(
            x = Daily_update['Date'].tail(25),
            y = Daily_update['Production Rate'].tail(25),
            name = 'daily Production',
            marker= dict(color='orange'),
            hoverinfo='text',


        )],

        'layout':go.Layout(
            title = {'text':'Daily Production:'+(Pump_Model),
                     'y':1,
                     'x':0.5,
                     'xanchor':'center',
                     'yanchor':'top'},
            titlefont = {'color':'white',
                         'size':20},
            font=dict(family = 'sans-serif',
                      color = 'white',
                      size = 12),
            hovermode= 'closest',
            paper_bgcolor= '#1f2c56',
            plot_bgcolor= '#1f2c56',
            legend={'orientation':'h',
                    'bgcolor':'#1f2c56',
                    'xanchor':'center','x':0.5,'y':-0.7},
            xaxis = dict(title ='<b>Date</b>',
                         color = 'white',
                         showline = True,
                         showgrid = True,),

            yaxis = dict(title='<b>production Rate</b>',
                     color='white',
                     showline=True,
                     showgrid=True, )
    )
    }

if __name__ == '__main__':
    app.run_server(port = 8000,debug=True)


