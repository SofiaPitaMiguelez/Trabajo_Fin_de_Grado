# import dash
# # Resto de tu configuración de app.py
# import os
# import pathlib
# import numpy as np
# import pandas as pd
# import datetime as dt
# import dash
# from dash import dcc
# #import dash_core_components as dcc
# from dash import html
# #import dash_html_components as html
# import plotly.graph_objects as go
# import plotly.express as px
# from plotly.subplots import make_subplots

# from dash.exceptions import PreventUpdate
# from dash.dependencies import Input, Output, State
# from scipy.stats import rayleigh
# import json

# import dash_leaflet as dl
# from dash.exceptions import PreventUpdate

# import dash_leaflet.express as dlx
# import dash_leaflet as dl

# #from main import main

# app_instance = dash.Dash(__name__, suppress_callback_exceptions=True)
# app_instance.title = "Visualización del ICA en el Puerto de Almería"
# app_instance_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}



# GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

# #app inicialization
# # app = dash.Dash(
# #     __name__,
# #     suppress_callback_exceptions=True 
# # )
# # app.title = "Visualización del ICA en el Puerto de Almería"
# # app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

# server = app_instance.server

# # Get the list of Excel file names in the current directory
# excel_files = [file for file in os.listdir("data") if file.startswith("resultados_INCA_")]

# #excel_files = [file for file in os.listdir("data") if file.startswith("resultados_INCA") and file.endswith(".xlsx")]

# # Extract the month information from the file names
# months = [file.split("_")[2].split(".xlsx")[0] for file in excel_files]

# # Define a function to read Excel data based on the selected month
# def read_excel_data(selected_month):
#     # Assuming the month information is part of the file name
#     file_name = [file for file in excel_files if selected_month in file][0]
#     df = pd.read_excel(file_name)
#     return df

# def get_file_path(selected_month):
#     if selected_month == "MAYO23":
#         return "data/resultados_INCA_MAYO23.xlsx"
#     elif selected_month == "JUNIO23":
#         return "data/resultados_INCA_JUNIO23.xlsx"
#     elif selected_month == "JULIO23":
#         return "data/resultados_INCA_JULIO23.xlsx"
#     elif selected_month == "AGOSTO23":
#         return "data/resultados_INCA_AGOSTO23.xlsx"
#     elif selected_month == "SEPTIEMBRE23":
#         return "data/resultados_INCA_SEPTIEMBRE23.xlsx"
#     elif selected_month == "OCTUBRE23":
#         return "data/resultados_INCA_OCTUBRE23.xlsx"
#     else:
#         raise ValueError("Invalid month selected")


# # Read your data file and perform data preprocessing
# initial_month = "MAYO23"  # Set an initial month
# file_path = get_file_path(initial_month)  # Set an initial file path

# # Define a dictionary to map month names to their corresponding numbers
# month_name_to_number = {
#     "ENERO": "01",
#     "FEBRERO": "02",
#     "MARZO": "03",
#     "ABRIL": "04",
#     "MAYO": "05",
#     "JUNIO": "06",
#     "JULIO": "07",
#     "AGOSTO": "08",
#     "SEPTIEMBRE": "09",
#     "OCTUBRE": "10",
#     "NOVIEMBRE": "11",
#     "DICIEMBRE": "12"
# }
# # Extract the month name from the initial_month
# month_name = initial_month[:-2]  # Remove the last two characters from the initial_month

# dataframes = []
# for day in range(1, 32):
#     month_number = month_name_to_number.get(month_name)
#     sheet_name = f"2023-{month_number}-{day:02}";
#     try:
#         df = pd.read_excel(file_path, sheet_name=sheet_name)
#         dataframes.append(df)
#     except Exception as e:
#         print(f"Error reading sheet {sheet_name}: {e}");

# for day in range(1, 31):
#     month_number = month_name_to_number.get(month_name)
#     sheet_name = f"2023-{month_number}-{day:02}";
#     try:
#         df = pd.read_excel(file_path, sheet_name=sheet_name)
#         dataframes.append(df)
#     except Exception as e:
#         print(f"Error reading sheet {sheet_name}: {e}");

# data = pd.concat(dataframes, ignore_index=True)


# data['Datetime'] = pd.to_datetime(data['Datetime'], format='%d/%m/%Y %H:%M:%S')
# data['Hour'] = data['Datetime'].dt.hour

# # Define the list of devices
# devices = data['Dispositivo'].unique()

# coordenadas = pd.read_csv("data/coordenadas.csv", delimiter=';')


# # Define a function to create and show the plot based on the selected device #CAMBIO SELECTED_DEVICE EN LUGAR DE DEVICE
# def create_and_show_plot(data, selected_device, selected_month):

#     month_name = selected_month[:-2]  # Remove the last two characters from the selected_month (assuming the format is consistent)

#     file_path = get_file_path(selected_month)  # Get the file path based on the selected month
#     dataframes = []

#     #data loading depending on if the month has 30 or 31 days
#     if month_name in ["MAYO", "JULIO", "AGOSTO", "OCTUBRE"]:
#          for day in range(1, 32):
#             month_number = month_name_to_number.get(month_name)
#             sheet_name = f"2023-{month_number}-{day:02}"
#             df = pd.read_excel(file_path, sheet_name=sheet_name)
#             dataframes.append(df)

#     elif month_name in ["JUNIO", "SEPTIEMBRE"]:
#         for day in range(1, 31):
#             month_number = month_name_to_number.get(month_name)
#             sheet_name = f"2023-{month_number}-{day:02}"
#             df = pd.read_excel(file_path, sheet_name=sheet_name)
#             dataframes.append(df)
  

#     data = pd.concat(dataframes, ignore_index=True)
#     # Convert 'Datetime' to a datetime object and extract the hour
#     data['Datetime'] = pd.to_datetime(data['Datetime'], format='%d/%m/%Y %H:%M:%S')
#     data['Hour'] = data['Datetime'].dt.hour

#     # Define the order of agents for column ordering in the stacked bar chart
#     agent_order = [
#         "O3 GCc AVG8H (ug/m3)",
#         "SO2 GCc AVG1H (ug/m3)",
#         "PM2.5 AVG24H (ug/m3)",
#         "PM10 AVG24H (ug/m3)",
#         "NO2 GCc AVG1H (ug/m3)",
#     ]

#     # Define a dictionary to map the index level to a numerical value
#     index_level_mapping = {
#         "SIN DATOS": 0,
#         "BUENA": 1,
#         "RAZONABLEMENTE BUENA": 2,
#         "REGULAR": 3,
#         "DESFAVORABLE": 4,
#         "MUY DESFAVORABLE": 5,
#         "EXTREMADAMENTE DESFAVORABLE": 6
#     }

#     # Create a list of all hours from 0 to 23
#     all_hours = list(range(24))

#     # Pivot the data to get the count of each agent for each device and hour
#     pivot_data = data.pivot_table(index=['Dispositivo', 'Hour'], columns='Agente en banda superior', aggfunc='size', fill_value=0)
#     # Calculate the probabilities for each agent for each hour
#     pivot_data_percentages = pivot_data.div(pivot_data.sum(axis=1), axis=0)

#     # Create a stacked bar chart for each device using Plotly Graph Objects
#     devices = pivot_data_percentages.index.get_level_values(0).unique()
#     colors = ['forestgreen', 'orangered', 'gold', 'purple', 'royalblue', 'grey']

#     # Calculate the distribution of "Banda" for each agent, hour, and device
#     banda_distribution = data.pivot_table(index=['Dispositivo', 'Hour', 'Agente en banda superior'], columns='Banda', aggfunc='size', fill_value=0)
#     banda_distribution_percentages = banda_distribution.div(banda_distribution.sum(axis=1), axis=0)


#     hover_info_bar_chart = []
#     # Add "Banda" distribution to the hover information
#     for device in [selected_device]:
#         device_data = pivot_data_percentages.xs(device, level='Dispositivo')
#         hours = device_data.index
#         agent_probabilities = device_data.values.T
#         bottom = np.zeros(len(hours))
#         fig = go.Figure()
#         for i, agent in enumerate(pivot_data_percentages.columns):
#             customdata = []
#             hover_text = []
#             agent_name = agent.split()[0]  # Take just the first word for the agent name in the pop-up
#             for hour in hours:
#                 distribution_info = []
#                 for banda in banda_distribution.columns:
#                     if (device, hour, agent) in banda_distribution_percentages.index and banda in banda_distribution_percentages.columns:
#                         distribution_info.append(f"{banda}: {banda_distribution_percentages.loc[(device, hour, agent)][banda]:.2%}")
#                     else:
#                         distribution_info.append(f"{banda}: 0.00%")
#                 customdata.append(distribution_info)
#                 hover_text.append(f"Agente:{agent_name}<br>Hora: {hour}h<br>Porcentaje: {agent_probabilities[i][hour]:.2%}<br>Distribución de INCA<br>{'<br>'.join(distribution_info)}")
#             hover_info_bar_chart.extend(customdata)  # Collect hover information for the bar chart


#             fig.add_trace(go.Bar(
#                 x=hours,
#                 y=agent_probabilities[i],
#                 name=agent,
#                 customdata=customdata,
#                 hoverinfo="text",
#                 hovertext=hover_text,
#                 marker_color=colors[i],
#             ))
#             bottom += agent_probabilities[i]

#         fig.update_layout(
#             barmode="stack",
#             title=f"Distribución de agentes en {month_name} en el dispositivo {device}",
#             xaxis_title="Tiempo",
#             yaxis_title="Probabilidad",
#             xaxis={'tickvals': all_hours, 'ticktext': all_hours},
#             showlegend=True,
#         )
#     return fig

# #definition of the layout
# app_instance.layout = html.Div(
# #app.layout = html.Div(
#     [
#         #dcc.Location(id='url', refresh=False),
#         dcc.Link(html.Button("Volver"), href="/main"),

        
#         html.H1("Análisis ICA", className="text-center", style={'color': 'white'}),
#         html.H2("En esta pantalla podrás seleccionar el dispositivo y el mes del año 2023 del que quieres visualizar los datos en los siguientes desplegables", style={'color': 'white'}),

#          html.Div(
#             [
#                 html.Label("Seleccionar Mes", style={'color': 'white'}),
#                 dcc.Dropdown(
#                     id='month-dropdown',
#                     options=[{'label': month, 'value': month} for month in months],
#                     value="MAYO23"
#                 ),

#                 html.Label("Seleccionar Dispositivo", style={'color': 'white'}),
#                 dcc.Dropdown(
#                     id='device-dropdown',
#                     options=[{'label': device, 'value': device} for device in devices],
#                     value=devices[0]
#                 ),

#                 html.Button("Visualizar Gráficas", id="ver-graficas-button", n_clicks=0, style={'color': 'white'}),

#                 html.Div(id="app-content"),
#             ],
#             style={'margin': '100px'} 
#         ),

#         # DISTRIBUCIÓN AGENTES EN BANDA SUPERIOR graphic at the top
#         dcc.Graph(
#             id='device-graph',
#             config={'displayModeBar': False},
#             style={'display': 'block'}
#         ),

#         #Pie Chart with DISTRIBUCIÓN DE NIVELES PARA AGENTE Y HORA SELECCIONADOS the first graphic
#         dcc.Graph(
#             id="pie-chart",
#             config={'displayModeBar': False},
#             style={'display': 'block'}
#         ),

#         # Add a new row for the "INCA" graph
#         html.Div(
#             dcc.Graph(
#                 id="inca-graph",
#                 config={'displayModeBar': False},
#                 style={'display': 'block'}

#                 #style={'display': 'flex'}
#             ),
#         ),
#     ],
    
#     style={'margin': '100px'}  # Adjust the margin as needed
# )


# def get_current_time():
#     """ Helper function to get the current time in seconds. """

#     now = dt.datetime.now()
#     total_time = (now.hour * 3600) + (now.minute * 60) + (now.second)
#     return total_time



# def generate_inca_graph(selected_month, selected_device):
    
#     dataframes = []

#     file_path = get_file_path(selected_month)  # Get the file path based on the selected month
#     month_name = selected_month[:-2] 
    
#     if month_name in ["MAYO", "JULIO", "AGOSTO", "OCTUBRE"]:
#         for day in range(1, 32):
#             month_number = month_name_to_number.get(month_name)
#             sheet_name = f"2023-{month_number}-{day:02}"
#             df = pd.read_excel(file_path, sheet_name=sheet_name)
#             dataframes.append(df)
#     elif month_name in ["JUNIO", "SEPTIEMBRE"]:
#         for day in range(1, 31):
#             month_number = month_name_to_number.get(month_name)
#             sheet_name = f"2023-{month_number}-{day:02}"
#             df = pd.read_excel(file_path, sheet_name=sheet_name)
#             dataframes.append(df)

#     # Load the data from the sheet
#     combined_data = pd.concat(dataframes, ignore_index=True)

#     # Filter data based on the selected device and month
#     combined_data = combined_data[(combined_data['Dispositivo'] == selected_device) & (combined_data['Datetime'].dt.month == int(month_name_to_number[month_name]))]

#     banda_to_index = {
#         "BUENA": 1,
#         "RAZONABLEMENTE BUENA": 2,
#         "REGULAR": 3,
#         "DESFAVORABLE": 4,
#         "MUY DESFAVORABLE": 5,
#         "EXTREMADAMENTE DESFAVORABLE": 6
#     }

#     # Convert the "Datetime" column to datetime format
#     combined_data['Datetime'] = pd.to_datetime(combined_data['Datetime'], format='%d/%m/%Y %H:%M:%S')

#     # Create a separate plot for each device
#     devices = combined_data['Dispositivo'].dropna().unique()   
    

#     fig = go.Figure()

#     for device in devices:
#         if device == selected_device:
#             device_data = combined_data[combined_data['Dispositivo'] == device]
#             device_data = device_data.dropna(subset=['Datetime'])
            
#             if not device_data.empty:
#                 device_data = device_data.sort_values(by='Datetime')
#                 continuous_data = pd.DataFrame({'Datetime': pd.date_range(start=device_data['Datetime'].min(), end=device_data['Datetime'].max(), freq='H')})
#                 continuous_data['Banda'] = pd.merge_asof(continuous_data, device_data, on='Datetime', direction='backward')['Banda']
                
#                 fig.add_trace(go.Scatter(
#                     x=continuous_data['Datetime'],
#                     y=[banda_to_index.get(banda, 0) for banda in continuous_data['Banda']],
#                     mode='lines',
#                     name=f"Device: {device}"
#                 ))

#     fig.update_layout(
#         title=f"INCA en el mes de {month_name}  del 2023 en el Dispositivo {selected_device}",
#         xaxis=dict(title='Fecha'),
#         yaxis=dict(title='Indice', range=[1, 6]),
#         legend=dict(title='Dispositivo'),
#     )
#     return fig


# def update_inca_graph(selected_month, selected_device):
#     # Your existing code to generate INCA graph
#     return generate_inca_graph(selected_month, selected_device)

# # @app_instance.callback(
# #     Output('pie-chart', 'figure'),
# #     [Input('device-graph', 'clickData')]
# # )
# def update_pie_chart(click_data):
#     print(click_data)  # Add this line to inspect the click_data structure

#     if click_data is None:
#         # No click data, return an empty figure
#         return go.Figure()

#     # Extract relevant information from click data
#     custom_data = click_data['points'][0].get('customdata', [])

#     # Create a dictionary from custom data for easier extraction
#     custom_data_dict = {entry.split(': ')[0]: float(entry.split(': ')[1][:-1]) for entry in custom_data}

#     # Ensure all values are present in custom_data_dict, even if not in the current data
#     all_values = ["SIN DATOS", "BUENA", "RAZONABLEMENTE BUENA", "REGULAR", "DESFAVORABLE", "MUY DESFAVORABLE", "EXTREMADAMENTE DESFAVORABLE"]
#     custom_data_dict.update({value: 0 for value in all_values if value not in custom_data_dict})

#     # Exclude entries with 0% values
#     custom_data_dict = {key: value for key, value in custom_data_dict.items() if value > 0}

#     # Define colors for each value
#     default_colors_dict = {
#         "SIN DATOS": (85/255, 89/255, 93/255),
#         "BUENA": (56/255, 162/255, 206/255),
#         "RAZONABLEMENTE BUENA": (50/255, 161/255, 94/255),
#         "REGULAR": (241/255, 229/255, 73/255),
#         "DESFAVORABLE": (200/255, 52/255, 65/255),
#         "MUY DESFAVORABLE": (110/255, 22/255, 29/255),
#         "EXTREMADAMENTE DESFAVORABLE": (162/255, 91/255, 164/255),
#     }

#     # Sort the dictionary by values to create a color scale
#     sorted_custom_data = {k: v for k, v in sorted(custom_data_dict.items(), key=lambda item: item[1], reverse=True)}

#     # Extract values and corresponding colors
#     labels = list(sorted_custom_data.keys())
#     values = list(sorted_custom_data.values())
#     colors = [default_colors_dict[label] for label in labels]

#     # Convert RGB tuples to color strings
#     colors_str = [f'rgb({int(r * 255)},{int(g * 255)},{int(b * 255)})' for (r, g, b) in colors]

#     # Create the Pie Chart for the chart
#     pie_chart = go.Figure(go.Pie(
#         labels=labels,
#         values=values,
#         textinfo='percent',
#         marker=dict(colors=colors),
#     ))

#     pie_chart.update_layout(
#         title="Distribución de valores del INCA para el agente seleccionado",
#         colorway=colors_str,
#         showlegend=True,
#         legend=dict(title='', orientation='v', yanchor='bottom', y=1.02, xanchor='right', x=1),
#     )

#     return pie_chart


# # @app_instance.callback(
# #     [Output('device-graph', 'figure'),
# #      Output('inca-graph', 'figure')],
# #     [Input('month-dropdown', 'value'),
# #      Input('device-dropdown', 'value')]
# #      #Input('ver-graficas-button', 'n_clicks')]##TESTING
# # )
# ##def update_layout(selected_month, selected_device, n_clicks):
# # def update_layout(selected_month, selected_device):
# #     # Load data
# #     file_path = get_file_path(selected_month)
# #     data = pd.read_excel(file_path)
    
# #     # Filter data based on selected device
# #     filtered_data = data[data['Dispositivo'] == selected_device]

# #     # Generate the large graph
# #     large_graph = create_and_show_plot(filtered_data, selected_device, selected_month)

# #     # Generate the INCA graph
# #     inca_graph = generate_inca_graph(selected_month, selected_device)

# #     return large_graph, inca_graph
#     ###########################################         ################################                ########################                ##############
# # @app_instance.callback(
# #     [Output('device-graph', 'figure'),
# #      Output('inca-graph', 'figure')],
# #     [Input('month-dropdown', 'value'),
# #      Input('device-dropdown', 'value')]
# # )
# # def update_layout(selected_month, selected_device):
# #     # Generate the large graph
# #     large_graph = create_and_show_plot(data, selected_device, selected_month)

# #     # Generate the INCA graph
# #     inca_graph = generate_inca_graph(selected_month, selected_device)

# #     return large_graph, inca_graph


# # def update_graph(selected_month, selected_device):
# #     # Load data
# #     file_path = get_file_path(selected_month)
# #     data = pd.read_excel(file_path)

# #     # Filter data based on selected device
# #     filtered_data = data[data['Dispositivo'] == selected_device]

# #     # Generate the device graph
# #     device_fig = create_and_show_plot(filtered_data, selected_device, selected_month)

# #     # Generate the INCA graph
# #     inca_fig = generate_inca_graph(selected_month, selected_device)
# #     return device_fig, inca_fig


# # Define app_instance_callbacks with the callbacks for the app_instance page
# # def app_instance_callbacks(app):
# #     @app_instance.callback(
# #         [Output('pie-chart', 'figure'),
# #          Output('device-graph', 'figure'),
# #          Output('inca-graph', 'figure')],
# #         [Input('device-graph', 'clickData'),
# #          Input('month-dropdown', 'value'),
# #          Input('device-dropdown', 'value')],
# #          allowDuplicates=True
# #     )
    
    
# #     # def update_figures(click_data, selected_month, selected_device):
# #     #     # Callback for updating the Pie Chart
# #     #     pie_chart = update_pie_chart(click_data)

# #     #     # Callback for updating the large graph
# #     #     large_graph = create_and_show_plot(data, selected_device, selected_month)

# #     #     # Callback for updating the INCA graph
# #     #     inca_graph = generate_inca_graph(selected_month, selected_device)

# #     #     return pie_chart, large_graph, inca_graph
# # def update_layout(selected_month, selected_device):
# #     # Generate the large graph
# #     large_graph = create_and_show_plot(data, selected_device, selected_month)

# #     # Generate the INCA graph
# #     inca_graph = generate_inca_graph(selected_month, selected_device)

# #     return large_graph, inca_graph

# # # @app_instance.callback(
# # #     [Output('device-graph', 'figure'),
# # #      Output('inca-graph', 'figure')],
# # #     [Input('ver-graficas-button', 'n_clicks')],
# # #     [State('month-dropdown', 'value'),
# # #      State('device-dropdown', 'value')],
# # #     prevent_initial_call=True
# # # )
# # def update_graph(n_clicks, selected_month, selected_device):
# #     # Load data
# #     file_path = get_file_path(selected_month)
# #     data = pd.read_excel(file_path)

# #     # Filter data based on selected device
# #     filtered_data = data[data['Dispositivo'] == selected_device]

# #     # Generate the device graph
# #     device_fig = create_and_show_plot(filtered_data, selected_device, selected_month)

# #     # Generate the INCA graph
# #     inca_fig = generate_inca_graph(selected_month, selected_device)
# #     return device_fig, inca_fig

# # Define app_instance_callbacks with the callbacks for the app_instance page

# def app_instance_callbacks(app_instance):
#     # @app_instance.callback(
#     #     [Output('pie-chart', 'figure'),
#     #      Output('device-graph', 'figure'),
#     #      Output('inca-graph', 'figure')],
#     #     [Input('device-graph', 'clickData'),
#     #      Input('month-dropdown', 'value'),
#     #      Input('device-dropdown', 'value')],
#     #     prevent_initial_call=True
#     # )
#     def update_layout(click_data, selected_month, selected_device):
#         # Check which input triggered the callback
#         triggered_input = dash.callback_context.triggered_id
#         if triggered_input == 'device-graph.clickData':
#             # Handle clickData input
#             return update_pie_chart(click_data), dash.no_update, dash.no_update
#         elif triggered_input == 'month-dropdown.value':
#             # Handle month-dropdown input
#             # ... your logic for month dropdown update
#             return dash.no_update, update_inca_graph(selected_month, selected_device), dash.no_update
#         elif triggered_input == 'device-dropdown.value':
#             # Handle device-dropdown input
#             # ... your logic for device dropdown update
#             return dash.no_update, update_inca_graph(selected_month, selected_device), dash.no_update
#         else:
#             return dash.no_update, dash.no_update, dash.no_update

#     @app_instance.callback(
#         [Output('device-graph', 'figure'),
#          Output('inca-graph', 'figure')],
#         [Input('ver-graficas-button', 'n_clicks')],
#         [State('month-dropdown', 'value'),
#          State('device-dropdown', 'value')],
#         prevent_initial_call=True
#     )
#     def update_graph(n_clicks, selected_month, selected_device):
#        # Load data
#         file_path = get_file_path(selected_month)
#         data = pd.read_excel(file_path)

#         # Filter data based on selected device
#         filtered_data = data[data['Dispositivo'] == selected_device]

#         # Generate the device graph
#         device_fig = create_and_show_plot(filtered_data, selected_device, selected_month)

#         # Generate the INCA graph
#         inca_fig = generate_inca_graph(selected_month, selected_device)
#         return device_fig, inca_fig


# if __name__ == "__main__":
#     app_instance.run_server(debug=True)





import dash
# Resto de tu configuración de app.py
import os
import pathlib
import numpy as np
import pandas as pd
import datetime as dt
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from scipy.stats import rayleigh
import json

import dash_leaflet as dl
from dash.exceptions import PreventUpdate

import dash_leaflet.express as dlx
import dash_leaflet as dl

from dash import dash_table
from dash import callback_context

#from main import main

app_instance = dash.Dash(__name__, suppress_callback_exceptions=True)
app_instance.title = "Visualización del ICA en el Puerto de Almería"
app_instance_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}



GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)


server = app_instance.server

# Get the list of Excel file names in the current directory
excel_files = [file for file in os.listdir("data") if file.startswith("resultados_INCA_")]

#excel_files = [file for file in os.listdir("data") if file.startswith("resultados_INCA") and file.endswith(".xlsx")]

# Extract the month information from the file names
months = [file.split("_")[2].split(".xlsx")[0] for file in excel_files]

# Define a function to read Excel data based on the selected month
def read_excel_data(selected_month):
    # Assuming the month information is part of the file name
    file_name = [file for file in excel_files if selected_month in file][0]
    df = pd.read_excel(file_name)
    return df

def get_file_path(selected_month):
    if selected_month == "MAYO23":
        return "data/resultados_INCA_MAYO23.xlsx"
    elif selected_month == "JUNIO23":
        return "data/resultados_INCA_JUNIO23.xlsx"
    elif selected_month == "JULIO23":
        return "data/resultados_INCA_JULIO23.xlsx"
    elif selected_month == "AGOSTO23":
        return "data/resultados_INCA_AGOSTO23.xlsx"
    elif selected_month == "SEPTIEMBRE23":
        return "data/resultados_INCA_SEPTIEMBRE23.xlsx"
    elif selected_month == "OCTUBRE23":
        return "data/resultados_INCA_OCTUBRE23.xlsx"
    else:
        raise ValueError("Invalid month selected")


# Read your data file and perform data preprocessing
initial_month = "MAYO23"  # Set an initial month
file_path = get_file_path(initial_month)  # Set an initial file path

# Define a dictionary to map month names to their corresponding numbers
month_name_to_number = {
    "ENERO": "01",
    "FEBRERO": "02",
    "MARZO": "03",
    "ABRIL": "04",
    "MAYO": "05",
    "JUNIO": "06",
    "JULIO": "07",
    "AGOSTO": "08",
    "SEPTIEMBRE": "09",
    "OCTUBRE": "10",
    "NOVIEMBRE": "11",
    "DICIEMBRE": "12"
}
# Extract the month name from the initial_month
month_name = initial_month[:-2]  # Remove the last two characters from the initial_month

dataframes = []
for day in range(1, 32):
    month_number = month_name_to_number.get(month_name)
    sheet_name = f"2023-{month_number}-{day:02}";
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        dataframes.append(df)
    except Exception as e:
        print(f"Error reading sheet {sheet_name}: {e}");

for day in range(1, 31):
    month_number = month_name_to_number.get(month_name)
    sheet_name = f"2023-{month_number}-{day:02}";
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        dataframes.append(df)
    except Exception as e:
        print(f"Error reading sheet {sheet_name}: {e}");

data = pd.concat(dataframes, ignore_index=True)


data['Datetime'] = pd.to_datetime(data['Datetime'], format='%d/%m/%Y %H:%M:%S')
data['Hour'] = data['Datetime'].dt.hour

# Define the list of devices
devices = data['Dispositivo'].unique()

coordenadas = pd.read_csv("data/coordenadas.csv", delimiter=';')


# Define a function to create and show the plot based on the selected device #CAMBIO SELECTED_DEVICE EN LUGAR DE DEVICE
def create_and_show_plot(data, selected_device, selected_month):

    month_name = selected_month[:-2]  # Remove the last two characters from the selected_month (assuming the format is consistent)

    file_path = get_file_path(selected_month)  # Get the file path based on the selected month
    dataframes = []

    #data loading depending on if the month has 30 or 31 days
    if month_name in ["MAYO", "JULIO", "AGOSTO", "OCTUBRE"]:
         for day in range(1, 32):
            month_number = month_name_to_number.get(month_name)
            sheet_name = f"2023-{month_number}-{day:02}"
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            dataframes.append(df)

    elif month_name in ["JUNIO", "SEPTIEMBRE"]:
        for day in range(1, 31):
            month_number = month_name_to_number.get(month_name)
            sheet_name = f"2023-{month_number}-{day:02}"
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            dataframes.append(df)
  

    data = pd.concat(dataframes, ignore_index=True)
    # Convert 'Datetime' to a datetime object and extract the hour
    data['Datetime'] = pd.to_datetime(data['Datetime'], format='%d/%m/%Y %H:%M:%S')
    data['Hour'] = data['Datetime'].dt.hour

    # Define the order of agents for column ordering in the stacked bar chart
    agent_order = [
        "O3 GCc AVG8H (ug/m3)",
        "SO2 GCc AVG1H (ug/m3)",
        "PM2.5 AVG24H (ug/m3)",
        "PM10 AVG24H (ug/m3)",
        "NO2 GCc AVG1H (ug/m3)",
    ]

    # Define a dictionary to map the index level to a numerical value
    index_level_mapping = {
        "SIN DATOS": 0,
        "BUENA": 1,
        "RAZONABLEMENTE BUENA": 2,
        "REGULAR": 3,
        "DESFAVORABLE": 4,
        "MUY DESFAVORABLE": 5,
        "EXTREMADAMENTE DESFAVORABLE": 6
    }

    # Create a list of all hours from 0 to 23
    all_hours = list(range(24))

    # Pivot the data to get the count of each agent for each device and hour
    pivot_data = data.pivot_table(index=['Dispositivo', 'Hour'], columns='Agente en banda superior', aggfunc='size', fill_value=0)
    # Calculate the probabilities for each agent for each hour
    pivot_data_percentages = pivot_data.div(pivot_data.sum(axis=1), axis=0)

    # Create a stacked bar chart for each device using Plotly Graph Objects
    devices = pivot_data_percentages.index.get_level_values(0).unique()
    colors = ['forestgreen', 'orangered', 'gold', 'purple', 'royalblue', 'grey']

    # Calculate the distribution of "Banda" for each agent, hour, and device
    banda_distribution = data.pivot_table(index=['Dispositivo', 'Hour', 'Agente en banda superior'], columns='Banda', aggfunc='size', fill_value=0)
    banda_distribution_percentages = banda_distribution.div(banda_distribution.sum(axis=1), axis=0)


    hover_info_bar_chart = []
    # Add "Banda" distribution to the hover information
    for device in [selected_device]:
        device_data = pivot_data_percentages.xs(device, level='Dispositivo')
        hours = device_data.index
        agent_probabilities = device_data.values.T
        bottom = np.zeros(len(hours))
        fig = go.Figure()
        for i, agent in enumerate(pivot_data_percentages.columns):
            customdata = []
            hover_text = []
            agent_name = agent.split()[0]  # Take just the first word for the agent name in the pop-up
            for hour in hours:
                distribution_info = []
                for banda in banda_distribution.columns:
                    if (device, hour, agent) in banda_distribution_percentages.index and banda in banda_distribution_percentages.columns:
                        distribution_info.append(f"{banda}: {banda_distribution_percentages.loc[(device, hour, agent)][banda]:.2%}")
                    else:
                        distribution_info.append(f"{banda}: 0.00%")
                customdata.append(distribution_info)
                hover_text.append(f"Agente:{agent_name}<br>Hora: {hour}h<br>Porcentaje: {agent_probabilities[i][hour]:.2%}<br>Distribución de INCA<br>{'<br>'.join(distribution_info)}")
            hover_info_bar_chart.extend(customdata)  # Collect hover information for the bar chart


            fig.add_trace(go.Bar(
                x=hours,
                y=agent_probabilities[i],
                name=agent,
                customdata=customdata,
                hoverinfo="text",
                hovertext=hover_text,
                marker_color=colors[i],
            ))
            bottom += agent_probabilities[i]

        fig.update_layout(
            barmode="stack",
            title=f"Distribución de agentes en {month_name} en el dispositivo {device}",
            xaxis_title="Tiempo",
            yaxis_title="Probabilidad",
            xaxis={'tickvals': all_hours, 'ticktext': all_hours},
            showlegend=True,
        )
    return fig

#definition of the layout
app_instance.layout = html.Div(
    [
        #dcc.Location(id='url', refresh=False),
        dcc.Link(html.Button("Volver"), href="/main"),

        
        html.H1("Análisis ICA", className="text-center", style={'color': 'white'}),
        html.H2("En esta pantalla podrás seleccionar el dispositivo y el mes del año 2023 del que quieres visualizar los datos en los siguientes desplegables", style={'color': 'white'}),

         html.Div(
            [
                html.Label("Seleccionar Mes", style={'color': 'white'}),
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label': month, 'value': month} for month in months],
                    value="MAYO23"
                ),

                html.Label("Seleccionar Dispositivo", style={'color': 'white'}),
                dcc.Dropdown(
                    id='device-dropdown',
                    options=[{'label': device, 'value': device} for device in devices],
                    value=devices[0]
                ),

                html.Button("Visualizar Gráficas", id="ver-graficas-button", n_clicks=0, style={'color': 'white'}),

                html.Div(id="app-content"),
            ],
            style={'margin': '100px'} 
        ),

        # DISTRIBUCIÓN AGENTES EN BANDA SUPERIOR graphic at the top
        dcc.Graph(
            id='device-graph',
            config={'displayModeBar': False},
            style={'display': 'block'}
        ),

        #Pie Chart with DISTRIBUCIÓN DE NIVELES PARA AGENTE Y HORA SELECCIONADOS the first graphic
        dcc.Graph(
            id="pie-chart",
            config={'displayModeBar': False},
            style={'display': 'block'}
        ),

        # Add a new row for the "INCA" graph
        html.Div(
            dcc.Graph(
                id="inca-graph",
                config={'displayModeBar': False},
                style={'display': 'block'}

                #style={'display': 'flex'}
            ),
        ),
    ],
    
    style={'margin': '100px'}  # Adjust the margin as needed
)


def get_current_time():
    """ Helper function to get the current time in seconds. """

    now = dt.datetime.now()
    total_time = (now.hour * 3600) + (now.minute * 60) + (now.second)
    return total_time



def generate_inca_graph(selected_month, selected_device):
    
    dataframes = []

    file_path = get_file_path(selected_month)  # Get the file path based on the selected month
    month_name = selected_month[:-2] 
    
    if month_name in ["MAYO", "JULIO", "AGOSTO", "OCTUBRE"]:
        for day in range(1, 32):
            month_number = month_name_to_number.get(month_name)
            sheet_name = f"2023-{month_number}-{day:02}"
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            dataframes.append(df)
    elif month_name in ["JUNIO", "SEPTIEMBRE"]:
        for day in range(1, 31):
            month_number = month_name_to_number.get(month_name)
            sheet_name = f"2023-{month_number}-{day:02}"
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            dataframes.append(df)

    # Load the data from the sheet
    combined_data = pd.concat(dataframes, ignore_index=True)

    # Filter data based on the selected device and month
    combined_data = combined_data[(combined_data['Dispositivo'] == selected_device) & (combined_data['Datetime'].dt.month == int(month_name_to_number[month_name]))]

    banda_to_index = {
        "BUENA": 1,
        "RAZONABLEMENTE BUENA": 2,
        "REGULAR": 3,
        "DESFAVORABLE": 4,
        "MUY DESFAVORABLE": 5,
        "EXTREMADAMENTE DESFAVORABLE": 6
    }

    # Convert the "Datetime" column to datetime format
    combined_data['Datetime'] = pd.to_datetime(combined_data['Datetime'], format='%d/%m/%Y %H:%M:%S')

    # Create a separate plot for each device
    devices = combined_data['Dispositivo'].dropna().unique()   
    

    fig = go.Figure()

    for device in devices:
        if device == selected_device:
            device_data = combined_data[combined_data['Dispositivo'] == device]
            device_data = device_data.dropna(subset=['Datetime'])
            
            if not device_data.empty:
                device_data = device_data.sort_values(by='Datetime')
                continuous_data = pd.DataFrame({'Datetime': pd.date_range(start=device_data['Datetime'].min(), end=device_data['Datetime'].max(), freq='H')})
                continuous_data['Banda'] = pd.merge_asof(continuous_data, device_data, on='Datetime', direction='backward')['Banda']
                
                fig.add_trace(go.Scatter(
                    x=continuous_data['Datetime'],
                    y=[banda_to_index.get(banda, 0) for banda in continuous_data['Banda']],
                    mode='lines',
                    name=f"Device: {device}"
                ))

    fig.update_layout(
        title=f"INCA en el mes de {month_name}  del 2023 en el Dispositivo {selected_device}",
        xaxis=dict(title='Fecha'),
        yaxis=dict(title='Indice', range=[1, 6]),
        legend=dict(title='Dispositivo'),
    )
    return fig


def update_inca_graph(selected_month, selected_device):
    # Your existing code to generate INCA graph
    return generate_inca_graph(selected_month, selected_device)


def update_pie_chart(click_data):
    print(click_data)  # Add this line to inspect the click_data structure

    if click_data is None:
        # No click data, return an empty figure
        return go.Figure()

    # Extract relevant information from click data
    custom_data = click_data['points'][0].get('customdata', [])

    # Create a dictionary from custom data for easier extraction
    custom_data_dict = {entry.split(': ')[0]: float(entry.split(': ')[1][:-1]) for entry in custom_data}

    # Ensure all values are present in custom_data_dict, even if not in the current data
    all_values = ["SIN DATOS", "BUENA", "RAZONABLEMENTE BUENA", "REGULAR", "DESFAVORABLE", "MUY DESFAVORABLE", "EXTREMADAMENTE DESFAVORABLE"]
    custom_data_dict.update({value: 0 for value in all_values if value not in custom_data_dict})

    # Exclude entries with 0% values
    custom_data_dict = {key: value for key, value in custom_data_dict.items() if value > 0}

    # Define colors for each value
    default_colors_dict = {
        "SIN DATOS": (85/255, 89/255, 93/255),
        "BUENA": (56/255, 162/255, 206/255),
        "RAZONABLEMENTE BUENA": (50/255, 161/255, 94/255),
        "REGULAR": (241/255, 229/255, 73/255),
        "DESFAVORABLE": (200/255, 52/255, 65/255),
        "MUY DESFAVORABLE": (110/255, 22/255, 29/255),
        "EXTREMADAMENTE DESFAVORABLE": (162/255, 91/255, 164/255),
    }

    # Sort the dictionary by values to create a color scale
    sorted_custom_data = {k: v for k, v in sorted(custom_data_dict.items(), key=lambda item: item[1], reverse=True)}

    # Extract values and corresponding colors
    labels = list(sorted_custom_data.keys())
    values = list(sorted_custom_data.values())
    colors = [default_colors_dict[label] for label in labels]

    # Convert RGB tuples to color strings
    colors_str = [f'rgb({int(r * 255)},{int(g * 255)},{int(b * 255)})' for (r, g, b) in colors]

    # Create the Pie Chart for the chart
    pie_chart = go.Figure(go.Pie(
        labels=labels,
        values=values,
        textinfo='percent',
        marker=dict(colors=colors),
    ))

    pie_chart.update_layout(
        title="Distribución de valores del INCA para el agente seleccionado",
        colorway=colors_str,
        showlegend=True,
        legend=dict(title='', orientation='v', yanchor='bottom', y=1.02, xanchor='right', x=1),
    )

    return pie_chart


def app_instance_callbacks(app_instance):
  
    def update_layout(click_data, selected_month, selected_device):
        # Check which input triggered the callback
        triggered_input = callback_context.triggered_id

        if triggered_input == 'device-graph.clickData':
            # Handle clickData input
            return update_pie_chart(click_data), dash.no_update, dash.no_update
        elif triggered_input == 'month-dropdown.value':
            # Handle month-dropdown input
            return dash.no_update, update_inca_graph(selected_month, selected_device), dash.no_update
        elif triggered_input == 'device-dropdown.value':
            # Handle device-dropdown input
            return dash.no_update, update_inca_graph(selected_month, selected_device), dash.no_update
        else:
            # Default case or initial load
            return update_pie_chart(None), update_inca_graph(selected_month, selected_device), dash.no_update


    @app_instance.callback(
        [Output('device-graph', 'figure'),
         Output('inca-graph', 'figure')],
        [Input('ver-graficas-button', 'n_clicks')],
        [State('month-dropdown', 'value'),
         State('device-dropdown', 'value')],
        prevent_initial_call=True
    )
    def update_graph(n_clicks, selected_month, selected_device):
       # Load data
        file_path = get_file_path(selected_month)
        data = pd.read_excel(file_path)

        # Filter data based on selected device
        filtered_data = data[data['Dispositivo'] == selected_device]

        # Generate the device graph
        device_fig = create_and_show_plot(filtered_data, selected_device, selected_month)

        # Generate the INCA graph
        inca_fig = generate_inca_graph(selected_month, selected_device)
        return device_fig, inca_fig
    
    @app_instance.callback(
    Output('pie-chart', 'figure'),
    [Input('device-graph', 'clickData')],
    [State('month-dropdown', 'value'),
     State('device-dropdown', 'value')],
)
    def update_pie_chart_callback(click_data, selected_month, selected_device):
        return update_pie_chart(click_data)






if __name__ == "__main__":
    app_instance.run_server(debug=True)