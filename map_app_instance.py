import dash
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import folium
import pandas as pd

import dash_leaflet as dl

from datetime import datetime, timedelta
from folium.vector_layers import Circle

from dash.dependencies import State 
import os

map_app_instance = dash.Dash(__name__, suppress_callback_exceptions=True)

map_app_instance.layout = html.Div([
    dcc.Location(id='url-map', refresh=False),
    html.Div(id="map-page-content", style={'font-family': 'Arial, sans-serif'}),
])

server = map_app_instance.server

# Load and process data for all months
def load_and_process_data_all():
    df_coord = pd.read_csv('data/coordenadas.csv', delimiter=';')

    all_files = [f for f in os.listdir('data') if f.startswith('resultados_INCA_')]
    
    df_merged = pd.DataFrame()
    for file in all_files:
        df_result_sheet = pd.read_excel(os.path.join('data', file), sheet_name=None)
        for sheet_name, sheet_data in df_result_sheet.items():
            merged_sheet = pd.merge(df_coord, sheet_data, on='Dispositivo')
            merged_sheet['Date'] = pd.to_datetime(sheet_name)
            df_merged = pd.concat([df_merged, merged_sheet])

    df_merged.reset_index(drop=True, inplace=True)

    return df_merged


def load_and_process_data_filters(map_type):
    df_merged = pd.DataFrame()

    if map_type == 'disaggregated':
        #all_files = [f for f in os.listdir('data') if f.startswith('resultados_INCA_')]
        all_files = ['resultados_INCA_MAYO23.xlsx']
        df_coord = pd.read_csv('data/coordenadas.csv', delimiter=';')
    elif map_type == 'aggregated':
        #all_files = [f for f in os.listdir('data') if f.startswith('Integracion_a_nivel_indice')]
        all_files = ['Integracion_a_nivel_indice_MAYO23.xlsx']
        df_coord = pd.read_csv('data/coordenadas_areas.csv', delimiter=';')
    elif map_type == 'aggregated_concentration':
        #all_files = [f for f in os.listdir('data') if f.startswith('Integracion_a_nivel_concentracion')]
        all_files = ['Integracion_a_nivel_concentraciones_MAYO23.xlsx']
        df_coord = pd.read_csv('data/coordenadas_areas.csv', delimiter=';')

    else:
        raise ValueError(f"Invalid map type: {map_type}")
            
    for file in all_files:
        df_result_sheet = pd.read_excel(os.path.join('data', file), sheet_name=None)
        for sheet_name, sheet_data in df_result_sheet.items():
            try:
                if map_type == 'disaggregated':
                    merged_sheet = pd.merge(df_coord, sheet_data, on='Dispositivo')
                elif map_type == 'aggregated':
                    merged_sheet = pd.merge(df_coord, sheet_data, on='Area')
                elif map_type == 'aggregated_concentration':
                    merged_sheet = pd.merge(df_coord, sheet_data, on='Area')
            
                merged_sheet['Date'] = pd.to_datetime(sheet_name)
            
                df_merged = pd.concat([df_merged, merged_sheet])
            except ValueError as e:
                print(f"Error processing sheet '{sheet_name}' from file '{file}': {e}")

    df_merged.reset_index(drop=True, inplace=True)

    return df_coord, df_merged


# Define color mapping
color_mapping = {
    'BUENA': 'blue',
    'RAZONABLEMENTE BUENA': 'green',
    'REGULAR': 'yellow',
    'DESFAVORABLE': 'red',
    'MUY DESFAVORABLE': 'darkred',
    'EXTREMADAMENTE DESFAVORABLE': 'purple',
    'SIN DATOS': 'grey',
}

# Create a base map on the Almería Port area
base_map = folium.Map(location=[36.831665, -2.478708], zoom_start=15)

# Use the load_and_process_data function to get the data
df_merged = load_and_process_data_all()

# Update the marks for the hour slider
hour_slider_marks = {i: str(i) for i in range(24)}

# Dash app initialization
#map_app = dash.Dash(__name__, suppress_callback_exceptions=True)


# Add the hidden div for storing the start_date
hidden_start_date = dcc.Store(id='hidden-start-date', data=None)


# Update the layout to use the new hour_slider_marks and entire date range of the data

map_app_instance.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=2 * 1000,  # in milliseconds, update every 2 seconds
        n_intervals=0
    ),
    
    # Filters
    html.Div([

        dcc.Link(html.Button("Volver"), href="/main"),

        html.H1("Visualización del mapa del área de estudio", style={'color': 'white'}),
        html.H2("Selecciona en el siguiente calendario la fecha inicial y final del periodo del que quieres visualizar los resultados obtenidos. Ten en cuenta que se cargarán desde las 00:00:00 de la primera fecha hasta las 00:00:00 de la segunda fecha.", style={'color': 'white'}),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=df_merged['Datetime'].min(),
            end_date=df_merged['Datetime'].max(),
            #start_date=df_merged['Date'].min(),
            #end_date=df_merged['Date'].max(),
            display_format='YYYY-MM-DDTHH:mm:ss',
        ),
        html.H2("A continuación, selecciona en el menú desplegable el tipo de agregación que quieres visualizar y haz click en 'Actualizar Mapa'", style={'color': 'white'}),
        dcc.Dropdown(
            id='map-type-dropdown',
            options=[
                {'label': 'Mapa integrado a nivel índice', 'value': 'aggregated'},
                {'label': 'Mapa integrado a nivel concentraciones', 'value': 'aggregated_concentration'},
                {'label': 'Mapa desagregado', 'value': 'disaggregated'},
            ],
            value='disaggregated',  # Default value
            style={'width': '50%', 'margin': '10px auto'},
        ),
        html.Button('Actualizar mapa', id='update-map-button', n_clicks=0, style={'margin': '10px', 'color': 'white'}),
    ], style={'margin': '10px'}),
    
    # Map
    html.Iframe(id='map', width='100%', height='600px'),
    html.Div(id='info-display', style={'text-align': 'center', 'margin-top': '10px'}),

    # Add the hidden div for storing start_date
    hidden_start_date,
], style={'margin': '100px', 'max-width': 'auto'})

# Update the callback to handle the entire date range
@map_app_instance.callback(
    Output('info-display', 'children'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_info_display(start_date, end_date):
    day_info = f"Desde el {start_date} hasta el {end_date}"
    return f"Mapa mostrado: {day_info}"

@map_app_instance.callback(
    Output('map', 'srcDoc'),
    [Input('interval-component', 'n_intervals'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('map-type-dropdown', 'value'),
     Input('update-map-button', 'n_clicks')  # click the button to generate the map
    ]
)


def update_map(n_intervals, start_date, end_date, map_type, n_clicks):
    print("Button clicked!")
    try:
        print("Button clicked!")

        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)

        if not start_date or n_clicks is None:
            raise PreventUpdate

        ctx = dash.callback_context

        # Determine which input triggered the callback
        if ctx.triggered_id is None:
            # If ctx.triggered_id is None, it means no input triggered the callback (initial load)
            triggered_input = None
        else:
            triggered_input = ctx.triggered_id.split('.')[0]

        # Reset time part to 00:00:00 if the start_date changes or the button is clicked
        if triggered_input in ['date-picker-range', 'update-map-button']:
            n_intervals = 0 if triggered_input == 'update-map-button' else 1
            current_hour = 0
            current_datetime = pd.to_datetime(start_date)
            if triggered_input == 'update-map-button':
                hidden_start_date.children = start_date  # Store the start_date for future comparison
        else:
            current_hour = (n_intervals % 24)
            current_datetime = pd.to_datetime(start_date) + timedelta(hours=current_hour)

        # Only update the map when the button is clicked
        print(f"n_clicks: {n_clicks}")

        if n_clicks is None or n_clicks == 0:
            return dash.no_update

        if triggered_input == 'update-map-button':
            return dash.no_update  # We want to update the map only after the button click

        # Load the appropriate data based on map_type
        #if map_type == 'disaggregated':
        df_coord, df_merged = load_and_process_data_filters(map_type=map_type)
        # elif map_type == 'aggregated':
        #     df_coord, df_merged = load_and_process_data_filters(map_type=map_type)
        # elif map_type == 'aggregated_concentration':
        #     df_coord, df_merged = load_and_process_data_filters(map_type=map_type)
        

        df_merged.reset_index(drop=True, inplace=True)

        # Print the columns to check for the presence of 'Banda'
        #print(df_merged.columns)

        filtered_df = df_merged[
            (df_merged['Date'] >= pd.to_datetime(start_date)) & (df_merged['Date'] <= pd.to_datetime(end_date))
            & (df_merged['Hour'] == current_hour)
        ]

        if filtered_df.empty:
            return "No data available for the selected range."

        # Create a new map for each update
        updated_map = folium.Map(location=[36.831665, -2.478708], zoom_start=15)

        # Add the current date and hour to the map title
        title_html = f"<h3 style='text-align:center;'>Fecha y hora: {current_datetime}</h3>"
        updated_map.get_root().html.add_child(folium.Element(title_html))

        # Add data to the map based on map_type
        if map_type == 'disaggregated':
            # Add data for the current hour (disaggregated)
            for index, row in filtered_df.iterrows():
                dispositivo = row['Dispositivo']
                latitud, longitud = float(row['Latitud'].replace(',', '.')), float(row['Longitud'].replace(',', '.'))
                coordinates = [latitud, longitud]

                if pd.notnull(latitud) and pd.notnull(longitud):
                    banda_color = row['Banda']
                    color = color_mapping.get(banda_color, 'black')

                    popup_content = f"{dispositivo}<br>Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}<br>Hour: {current_hour}"

                    folium.CircleMarker(
                        location=coordinates,
                        radius=15,
                        color=color,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.7,
                        popup=popup_content,
                    ).add_to(updated_map)

        elif map_type == 'aggregated':
            df_coord['Area'] = df_coord['Area'].str.strip()

            for area in df_coord['Area']:
                # Filter data for the current area and hour
                area_data = filtered_df[filtered_df['Area'] == area]

                if not area_data.empty:
                    # Use the first row to get the location information (assuming it's the same for all rows in the area)
                    latitud, longitud = float(area_data['Latitud'].iloc[0].replace(',', '.')), float(area_data['Longitud'].iloc[0].replace(',', '.'))
                    coordinates = [latitud, longitud]

                    # Use the mode of 'Banda' as the color for the area
                    banda_color = area_data['Banda'].mode().iloc[0]
                    color = color_mapping.get(banda_color, 'black')

                    popup_content = f"Area: {area}<br>Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}<br>Hour: {current_hour}"

                    folium.CircleMarker(
                        location=coordinates,
                        radius=30,
                        color=color,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.7,
                        popup=popup_content,
                    ).add_to(updated_map)

        elif map_type == 'aggregated_concentration':
            df_coord['Area'] = df_coord['Area'].str.strip()

            for area in df_coord['Area']:
                # Filter data for the current area and hour
                area_data = filtered_df[filtered_df['Area'] == area]

                if not area_data.empty:
                    # Use the first row to get the location information (assuming it's the same for all rows in the area)
                    latitud, longitud = float(area_data['Latitud'].iloc[0].replace(',', '.')), float(area_data['Longitud'].iloc[0].replace(',', '.'))
                    coordinates = [latitud, longitud]

                    # Use the mode of 'Banda' as the color for the area
                    banda_color = area_data['Banda'].mode().iloc[0]
                    color = color_mapping.get(banda_color, 'black')

                    popup_content = f"Area: {area}<br>Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}<br>Hour: {current_hour}"

                    folium.CircleMarker(
                        location=coordinates,
                        radius=30,
                        color=color,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.7,
                        popup=popup_content,
                    ).add_to(updated_map)

        # Convert the updated map to HTML and return it
        map_html = updated_map.get_root().render()
        return map_html

                
    except Exception as e:
        print(f"Error in update_map callback: {str(e)}")
        return dash.no_update

def update_map_on_page_load(n_intervals, start_date, end_date, map_type, n_clicks, current_map):
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)

    if not start_date or n_clicks is None:
        raise PreventUpdate

    ctx = dash.callback_context

    # Determine which input triggered the callback
    if ctx.triggered_id is None:
        # If ctx.triggered_id is None, it means no input triggered the callback (initial load)
        triggered_input = None
    else:
        triggered_input = ctx.triggered_id.split('.')[0]

    # Reset time part to 00:00:00 if the start_date changes or the button is clicked
    if triggered_input in ['date-picker-range', 'update-map-button']:
        n_intervals = 0 if triggered_input == 'update-map-button' else 1
        current_hour = 0
        current_datetime = pd.to_datetime(start_date)
        if triggered_input == 'update-map-button':
            hidden_start_date.children = start_date  # Store the start_date for future comparison
    else:
        current_hour = (n_intervals % 24)
        current_datetime = pd.to_datetime(start_date) + timedelta(hours=current_hour)

    # Only update the map when the button is clicked
    if n_clicks is None or n_clicks == 0:
        return dash.no_update

    if triggered_input == 'update-map-button':
        return dash.no_update  # We want to update the map only after the button click

    df_coord, df_merged = load_and_process_data_filters(map_type=map_type)

    

    df_merged.reset_index(drop=True, inplace=True)

    filtered_df = df_merged[
        (df_merged['Date'] >= pd.to_datetime(start_date)) & (df_merged['Date'] <= pd.to_datetime(end_date))
        & (df_merged['Hour'] == current_hour)
    ]

    if filtered_df.empty:
        return "No data available for the selected range."

    # Create a new map for each update
    updated_map = folium.Map(location=[36.831665, -2.478708], zoom_start=15)

    # Add the current date and hour to the map title
    title_html = f"<h3 style='text-align:center;'>Fecha y hora: {current_datetime}</h3>"
    updated_map.get_root().html.add_child(folium.Element(title_html))

    # Add data to the map based on map_type
    if map_type == 'disaggregated':
        # Add data for the current hour (disaggregated)
        for index, row in filtered_df.iterrows():
            dispositivo = row['Dispositivo']
            latitud, longitud = float(row['Latitud'].replace(',', '.')), float(row['Longitud'].replace(',', '.'))
            coordinates = [latitud, longitud]

            if pd.notnull(latitud) and pd.notnull(longitud):
                banda_color = row['Banda']
                color = color_mapping.get(banda_color, 'black')

                popup_content = f"{dispositivo}<br>Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}<br>Hour: {current_hour}"

                folium.CircleMarker(
                    location=coordinates,
                    radius=15,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7,
                    popup=popup_content,
                ).add_to(updated_map)

    elif map_type == 'aggregated':
        df_coord['Area'] = df_coord['Area'].str.strip()

        for area in df_coord['Area']:
            # Filter data for the current area and hour
            area_data = filtered_df[filtered_df['Area'] == area]

            if not area_data.empty:
                # Use the first row to get the location information (assuming it's the same for all rows in the area)
                latitud, longitud = float(area_data['Latitud'].iloc[0].replace(',', '.')), float(area_data['Longitud'].iloc[0].replace(',', '.'))
                coordinates = [latitud, longitud]

                # Use the mode of 'Banda' as the color for the area
                banda_color = area_data['Banda'].mode().iloc[0]
                color = color_mapping.get(banda_color, 'black')

                popup_content = f"Area: {area}<br>Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}<br>Hour: {current_hour}"

                folium.CircleMarker(
                    location=coordinates,
                    radius=30,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7,
                    popup=popup_content,
                ).add_to(updated_map)

    elif map_type == 'aggregated_concentration':
        df_coord['Area'] = df_coord['Area'].str.strip()

        for area in df_coord['Area']:
            # Filter data for the current area and hour
            area_data = filtered_df[filtered_df['Area'] == area]

            if not area_data.empty:
                # Use the first row to get the location information (assuming it's the same for all rows in the area)
                latitud, longitud = float(area_data['Latitud'].iloc[0].replace(',', '.')), float(area_data['Longitud'].iloc[0].replace(',', '.'))
                coordinates = [latitud, longitud]

                # Use the mode of 'Banda' as the color for the area
                banda_color = area_data['Banda'].mode().iloc[0]
                color = color_mapping.get(banda_color, 'black')

                popup_content = f"Area: {area}<br>Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}<br>Hour: {current_hour}"

                folium.CircleMarker(
                    location=coordinates,
                    radius=30,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7,
                    popup=popup_content,
                ).add_to(updated_map)

    # Convert the updated map to HTML and return it
    map_html = updated_map.get_root().render()    
    print("Mapa actualizado al cargar la página")
    return map_html



server = map_app_instance.server  # in case you run with Gunicorn
def map_app_instance_callbacks(app):
    
    @app.callback(
        Output('info-display', 'children'),
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_info_display(start_date, end_date):
        # Lógica para actualizar el contenido de 'info-display'
        day_info = f"Desde el {start_date} hasta el {end_date}"
        return f"Mapa mostrado: {day_info}"

    @app.callback(
        Output('map', 'srcDoc'),
        [Input('interval-component', 'n_intervals'),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date'),
         Input('map-type-dropdown', 'value'),
         Input('update-map-button', 'n_clicks')]
    )
    def update_map(n_intervals, start_date, end_date, map_type, n_clicks):
        print("Button clicked!")
        try:
            print("Button clicked!")

            start_datetime = pd.to_datetime(start_date)
            end_datetime = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)

            if not start_date or n_clicks is None:
                raise PreventUpdate

            ctx = dash.callback_context

            # Determine which input triggered the callback
            if ctx.triggered_id is None:
                # If ctx.triggered_id is None, it means no input triggered the callback (initial load)
                triggered_input = None
            else:
                triggered_input = ctx.triggered_id.split('.')[0]

            # Reset time part to 00:00:00 if the start_date changes or the button is clicked
            if triggered_input in ['date-picker-range', 'update-map-button']:
                n_intervals = 0 if triggered_input == 'update-map-button' else 1
                current_hour = 0
                current_datetime = pd.to_datetime(start_date)
                if triggered_input == 'update-map-button':
                    hidden_start_date.children = start_date  # Store the start_date for future comparison
            else:
                current_hour = (n_intervals % 24)
                current_datetime = pd.to_datetime(start_date) + timedelta(hours=current_hour)

            # Only update the map when the button is clicked
            print(f"n_clicks: {n_clicks}")

            if n_clicks is None or n_clicks == 0:
                return dash.no_update

            if triggered_input == 'update-map-button':
                return dash.no_update  # We want to update the map only after the button click

            # Load the appropriate data based on map_type
            #if map_type == 'disaggregated':
            df_coord, df_merged = load_and_process_data_filters(map_type=map_type)
            # elif map_type == 'aggregated':
            #     df_coord, df_merged = load_and_process_data_filters(map_type=map_type)
            # elif map_type == 'aggregated_concentration':
            #     df_coord, df_merged = load_and_process_data_filters(map_type=map_type)
            

            df_merged.reset_index(drop=True, inplace=True)

            # Print the columns to check for the presence of 'Banda'
            #print(df_merged.columns)

            filtered_df = df_merged[
                (df_merged['Date'] >= pd.to_datetime(start_date)) & (df_merged['Date'] <= pd.to_datetime(end_date))
                & (df_merged['Hour'] == current_hour)
            ]

            if filtered_df.empty:
                return "No data available for the selected range."

            # Create a new map for each update
            updated_map = folium.Map(location=[36.831665, -2.478708], zoom_start=15)

            # Add the current date and hour to the map title
            title_html = f"<h3 style='text-align:center;'>Fecha y hora: {current_datetime}</h3>"
            updated_map.get_root().html.add_child(folium.Element(title_html))

            # Add data to the map based on map_type
            if map_type == 'disaggregated':
                # Add data for the current hour (disaggregated)
                for index, row in filtered_df.iterrows():
                    dispositivo = row['Dispositivo']
                    latitud, longitud = float(row['Latitud'].replace(',', '.')), float(row['Longitud'].replace(',', '.'))
                    coordinates = [latitud, longitud]

                    if pd.notnull(latitud) and pd.notnull(longitud):
                        banda_color = row['Banda']
                        color = color_mapping.get(banda_color, 'black')

                        popup_content = f"{dispositivo}<br>Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}<br>Hour: {current_hour}"

                        folium.CircleMarker(
                            location=coordinates,
                            radius=15,
                            color=color,
                            fill=True,
                            fill_color=color,
                            fill_opacity=0.7,
                            popup=popup_content,
                        ).add_to(updated_map)

            elif map_type == 'aggregated':
                df_coord['Area'] = df_coord['Area'].str.strip()

                for area in df_coord['Area']:
                    # Filter data for the current area and hour
                    area_data = filtered_df[filtered_df['Area'] == area]

                    if not area_data.empty:
                        # Use the first row to get the location information (assuming it's the same for all rows in the area)
                        latitud, longitud = float(area_data['Latitud'].iloc[0].replace(',', '.')), float(area_data['Longitud'].iloc[0].replace(',', '.'))
                        coordinates = [latitud, longitud]

                        # Use the mode of 'Banda' as the color for the area
                        banda_color = area_data['Banda'].mode().iloc[0]
                        color = color_mapping.get(banda_color, 'black')

                        popup_content = f"Area: {area}<br>Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}<br>Hour: {current_hour}"

                        folium.CircleMarker(
                            location=coordinates,
                            radius=30,
                            color=color,
                            fill=True,
                            fill_color=color,
                            fill_opacity=0.7,
                            popup=popup_content,
                        ).add_to(updated_map)

            elif map_type == 'aggregated_concentration':
                df_coord['Area'] = df_coord['Area'].str.strip()

                for area in df_coord['Area']:
                    # Filter data for the current area and hour
                    area_data = filtered_df[filtered_df['Area'] == area]

                    if not area_data.empty:
                        # Use the first row to get the location information (assuming it's the same for all rows in the area)
                        latitud, longitud = float(area_data['Latitud'].iloc[0].replace(',', '.')), float(area_data['Longitud'].iloc[0].replace(',', '.'))
                        coordinates = [latitud, longitud]

                        # Use the mode of 'Banda' as the color for the area
                        banda_color = area_data['Banda'].mode().iloc[0]
                        color = color_mapping.get(banda_color, 'black')

                        popup_content = f"Area: {area}<br>Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}<br>Hour: {current_hour}"

                        folium.CircleMarker(
                            location=coordinates,
                            radius=30,
                            color=color,
                            fill=True,
                            fill_color=color,
                            fill_opacity=0.7,
                            popup=popup_content,
                        ).add_to(updated_map)

            # Convert the updated map to HTML and return it
            map_html = updated_map.get_root().render()
            return map_html
                    
        except Exception as e:
            print(f"Error in update_map callback: {str(e)}")
            return dash.no_update
     

    # @app.callback(
    #     Output('map', 'srcDoc'),
    #     [Input('date-picker-range', 'start_date'),
    #      Input('date-picker-range', 'end_date'),
    #      Input('map-type-dropdown', 'value'),
    #      Input('update-map-button', 'n_clicks')]
    # )
    def update_map_on_page_load(start_date, end_date, map_type, n_clicks):
        # Lógica para actualizar el contenido de 'map' al cargar la página
        try:
            start_datetime = pd.to_datetime(start_date)
            end_datetime = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)

            if not start_date or n_clicks is None:
                raise PreventUpdate

            ctx = dash.callback_context

            # Determine which input triggered the callback
            if ctx.triggered_id is None:
                # If ctx.triggered_id is None, it means no input triggered the callback (initial load)
                triggered_input = None
            else:
                triggered_input = ctx.triggered_id.split('.')[0]

            # Reset time part to 00:00:00 if the start_date changes or the button is clicked
            if triggered_input in ['date-picker-range', 'update-map-button']:
                n_intervals = 0 if triggered_input == 'update-map-button' else 1
                current_hour = 0
                current_datetime = pd.to_datetime(start_date)
                if triggered_input == 'update-map-button':
                    hidden_start_date.children = start_date  # Store the start_date for future comparison
            else:
                current_hour = (n_intervals % 24)
                current_datetime = pd.to_datetime(start_date) + timedelta(hours=current_hour)

            # Only update the map when the button is clicked
            if n_clicks is None or n_clicks == 0:
                return dash.no_update

            if triggered_input == 'update-map-button':
                return dash.no_update  # We want to update the map only after the button click

            df_coord, df_merged = load_and_process_data_filters(map_type=map_type)

            

            df_merged.reset_index(drop=True, inplace=True)

            filtered_df = df_merged[
                (df_merged['Date'] >= pd.to_datetime(start_date)) & (df_merged['Date'] <= pd.to_datetime(end_date))
                & (df_merged['Hour'] == current_hour)
            ]

            if filtered_df.empty:
                return "No data available for the selected range."

            # Create a new map for each update
            updated_map = folium.Map(location=[36.831665, -2.478708], zoom_start=15)

            # Add the current date and hour to the map title
            title_html = f"<h3 style='text-align:center;'>Fecha y hora: {current_datetime}</h3>"
            updated_map.get_root().html.add_child(folium.Element(title_html))

            # Add data to the map based on map_type
            if map_type == 'disaggregated':
                # Add data for the current hour (disaggregated)
                for index, row in filtered_df.iterrows():
                    dispositivo = row['Dispositivo']
                    latitud, longitud = float(row['Latitud'].replace(',', '.')), float(row['Longitud'].replace(',', '.'))
                    coordinates = [latitud, longitud]

                    if pd.notnull(latitud) and pd.notnull(longitud):
                        banda_color = row['Banda']
                        color = color_mapping.get(banda_color, 'black')

                        popup_content = f"{dispositivo}<br>Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}<br>Hour: {current_hour}"

                        folium.CircleMarker(
                            location=coordinates,
                            radius=15,
                            color=color,
                            fill=True,
                            fill_color=color,
                            fill_opacity=0.7,
                            popup=popup_content,
                        ).add_to(updated_map)

            elif map_type == 'aggregated':
                df_coord['Area'] = df_coord['Area'].str.strip()

                for area in df_coord['Area']:
                    # Filter data for the current area and hour
                    area_data = filtered_df[filtered_df['Area'] == area]

                    if not area_data.empty:
                        # Use the first row to get the location information (assuming it's the same for all rows in the area)
                        latitud, longitud = float(area_data['Latitud'].iloc[0].replace(',', '.')), float(area_data['Longitud'].iloc[0].replace(',', '.'))
                        coordinates = [latitud, longitud]

                        # Use the mode of 'Banda' as the color for the area
                        banda_color = area_data['Banda'].mode().iloc[0]
                        color = color_mapping.get(banda_color, 'black')

                        popup_content = f"Area: {area}<br>Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}<br>Hour: {current_hour}"

                        folium.CircleMarker(
                            location=coordinates,
                            radius=30,
                            color=color,
                            fill=True,
                            fill_color=color,
                            fill_opacity=0.7,
                            popup=popup_content,
                        ).add_to(updated_map)

            elif map_type == 'aggregated_concentration':
                df_coord['Area'] = df_coord['Area'].str.strip()

                for area in df_coord['Area']:
                    # Filter data for the current area and hour
                    area_data = filtered_df[filtered_df['Area'] == area]

                    if not area_data.empty:
                        # Use the first row to get the location information (assuming it's the same for all rows in the area)
                        latitud, longitud = float(area_data['Latitud'].iloc[0].replace(',', '.')), float(area_data['Longitud'].iloc[0].replace(',', '.'))
                        coordinates = [latitud, longitud]

                        # Use the mode of 'Banda' as the color for the area
                        banda_color = area_data['Banda'].mode().iloc[0]
                        color = color_mapping.get(banda_color, 'black')

                        popup_content = f"Area: {area}<br>Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}<br>Hour: {current_hour}"

                        folium.CircleMarker(
                            location=coordinates,
                            radius=30,
                            color=color,
                            fill=True,
                            fill_color=color,
                            fill_opacity=0.7,
                            popup=popup_content,
                        ).add_to(updated_map)

            # Convert the updated map to HTML and return it
            map_html = updated_map.get_root().render()    
            print("Mapa actualizado al cargar la página")
            return map_html
        except Exception as e:
            print(f"Error in update_map_on_page_load callback: {str(e)}")
            return dash.no_update

# # Run the app
if __name__ == '__main__':
    map_app_instance.run_server(debug=True)