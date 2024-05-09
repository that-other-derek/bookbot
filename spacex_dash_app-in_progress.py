# Import required libraries
import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
#print('min payload is ',min_payload)
#launch site list
launch_sites = spacex_df['Launch Site'].unique()
#print(launch_sites)
launch_list =[i for i in (launch_sites)]

#some task work
success_df = spacex_df.groupby('Launch Site')['class'].sum().to_frame().reset_index()
my_values=success_df['class']
my_names=success_df['Launch Site']
#print(success_df.values)

#some task work
payload_class = spacex_df['class']
payload_wt =spacex_df['Payload Mass (kg)']

#my_values=success_df['class']
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard02',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Label('Select Launch Site'),
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[{'label': i, 'value':i} for i in launch_list],
                                    value='default',
                                    placeholder='Select A Launch Site'
                                ),
                                html.Br(),
                                html.Div(

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                
                                
                                    dcc.Graph(
                                        id='success-pie-chart',
                                        figure=px.pie(
                                            success_df,
                                            values=my_values,
                                            names=my_names,
                                            title='Successful Launches'
                                            
                                            )
                                        )
                                )
                                    ,
                                html.Br(),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.P("Payload range (Kg):"),
                                html.Div(
                                    dcc.RangeSlider(
                                        id='payload-slider',
                                        min= min_payload, 
                                        max= max_payload,
                                        value=[500,5000]
                                        )
                                        ),
                                
 
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(
                                        id='success-payload-scatter-chart',
                                        figure=px.scatter(spacex_df,x=payload_wt, y=payload_class)
                                        )),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown',component_property='value')
    )
def update_output_pie(selected_site):
    if selected_site is None:
        return px.pie(
            success_df,
            values=my_values,
            names=my_names,
            title='Succesful Launches Initial2'
        ) 
    elif selected_site == 'default':
        print('default')
        #print(success_df.head())
        return px.pie(
            success_df,
            
            values=my_values,
            names=my_names,
            title='Succesful Launches Initial1'
        )
    else:
        print('selected site is: ', selected_site)
        site_df = spacex_df[spacex_df['Launch Site'] == selected_site][['Launch Site', 'class']].reset_index(drop=True)
        print(site_df.head())
            
        #site_values=site_df['class']
        #site_names=site_df["Launch Site"]
        

        return px.pie(
            site_df,
            values='class',
            names='Launch Site',
            title='Succesful Launches Initial3'
            )
            
          


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
